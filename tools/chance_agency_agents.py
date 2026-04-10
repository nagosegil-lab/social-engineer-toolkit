#!/usr/bin/env python3
"""Multi-agent analytics pipeline for Chance historical data.

This module orchestrates specialized "agents":
1) Data Collector Agent
2) Feature Analyst Agent
3) AI Predictor Agent
4) Backtest Agent
5) Portfolio Builder Agent
6) Report Agent
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from tools.historical_number_scorer import (
    ScoredAiLine,
    load_draws_from_csv,
    predict_ai_ordered_lines,
    score_values,
)


@dataclass(frozen=True)
class FeatureSummary:
    draw_count: int
    line_length: int
    top_values: List[str]
    position_leaders: List[List[Tuple[str, int]]]


@dataclass(frozen=True)
class BacktestSummary:
    evaluated_draws: int
    top_k: int
    exact_hit_rate: float
    avg_best_position_matches: float
    avg_best_symbol_overlap: float


@dataclass(frozen=True)
class PortfolioPlan:
    double_lines: List[str]
    backup_lines: List[str]


@dataclass(frozen=True)
class AgentProfile:
    role: str
    name: str
    description: str
    path: str


@dataclass(frozen=True)
class ProfileRegistry:
    loaded: List[AgentProfile]
    missing_roles: List[str]


def _line_to_tuple(values: str) -> Tuple[str, ...]:
    return tuple(values.split("|"))


def _line_overlap_count(left: Sequence[str], right: Sequence[str]) -> int:
    left_count = Counter(left)
    right_count = Counter(right)
    return sum(min(left_count[symbol], right_count[symbol]) for symbol in left_count)


def _parse_frontmatter(raw: str) -> Dict[str, str]:
    """Parse simple YAML-like frontmatter block from markdown."""
    lines = raw.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    out: Dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out


class AgencyProfileAgent:
    ROLE_TO_FILE = {
        "orchestrator": "specialized/agents-orchestrator.md",
        "analytics": "specialized/data-analytics-reporter.md",
        "project_shepherd": "project-management/project-management-project-shepherd.md",
    }

    def run(self, base_dir: Path, strict: bool = False) -> ProfileRegistry:
        loaded: List[AgentProfile] = []
        missing_roles: List[str] = []

        for role, relative_path in self.ROLE_TO_FILE.items():
            profile_path = base_dir / relative_path
            if not profile_path.exists():
                missing_roles.append(role)
                continue

            raw = profile_path.read_text(encoding="utf-8")
            frontmatter = _parse_frontmatter(raw)
            loaded.append(
                AgentProfile(
                    role=role,
                    name=frontmatter.get("name", role),
                    description=frontmatter.get("description", "N/A"),
                    path=str(profile_path),
                )
            )

        if strict and missing_roles:
            raise ValueError(
                f"Missing required agency profiles for roles: {', '.join(missing_roles)}"
            )
        return ProfileRegistry(loaded=loaded, missing_roles=missing_roles)


class DataCollectorAgent:
    def run(
        self,
        csv_path: Path,
        columns: Sequence[str] | None,
        exclude_columns: Sequence[str] | None,
    ) -> Tuple[List[List[str]], List[str]]:
        return load_draws_from_csv(csv_path, columns=columns, exclude_columns=exclude_columns)


class FeatureAnalystAgent:
    def run(self, draws: Sequence[Sequence[str]], recent_window: str) -> FeatureSummary:
        if not draws:
            raise ValueError("No draws available for analysis.")
        line_length = len(draws[0])
        top_values = [row.value for row in score_values(draws, recent_window=recent_window)[:8]]
        position_leaders: List[List[Tuple[str, int]]] = []
        for pos in range(line_length):
            counter = Counter(draw[pos] for draw in draws if len(draw) > pos)
            position_leaders.append(counter.most_common(4))
        return FeatureSummary(
            draw_count=len(draws),
            line_length=line_length,
            top_values=top_values,
            position_leaders=position_leaders,
        )


class AIPredictorAgent:
    def run(
        self,
        draws: Sequence[Sequence[str]],
        top_ai: int,
        ai_position_top_k: int,
        ai_half_life: float,
        ai_smoothing: float,
        ai_novelty_lookback: int,
        recent_window: str,
    ) -> List[ScoredAiLine]:
        return predict_ai_ordered_lines(
            draws=draws,
            top_lines=top_ai,
            position_top_k=ai_position_top_k,
            recent_window=recent_window,
            half_life=ai_half_life,
            smoothing=ai_smoothing,
            novelty_lookback=ai_novelty_lookback,
        )


class BacktestAgent:
    def run(
        self,
        draws: Sequence[Sequence[str]],
        evaluate_last: int,
        top_k: int,
        ai_position_top_k: int,
        ai_half_life: float,
        ai_smoothing: float,
        ai_novelty_lookback: int,
        recent_window: str,
    ) -> BacktestSummary:
        if len(draws) < 15:
            return BacktestSummary(0, top_k, 0.0, 0.0, 0.0)

        start_index = max(10, len(draws) - evaluate_last)
        exact_hits = 0
        total_best_position_matches = 0
        total_best_overlap = 0
        evaluated = 0

        for idx in range(start_index, len(draws)):
            train_draws = draws[:idx]
            actual = tuple(draws[idx])
            predictions = predict_ai_ordered_lines(
                draws=train_draws,
                top_lines=top_k,
                position_top_k=ai_position_top_k,
                recent_window=recent_window,
                half_life=ai_half_life,
                smoothing=ai_smoothing,
                novelty_lookback=ai_novelty_lookback,
            )
            if not predictions:
                continue

            predicted_lines = [_line_to_tuple(row.values) for row in predictions]
            if actual in predicted_lines:
                exact_hits += 1

            best_position_match = max(
                sum(1 for i, symbol in enumerate(predicted) if symbol == actual[i])
                for predicted in predicted_lines
            )
            best_overlap = max(_line_overlap_count(predicted, actual) for predicted in predicted_lines)

            total_best_position_matches += best_position_match
            total_best_overlap += best_overlap
            evaluated += 1

        if evaluated == 0:
            return BacktestSummary(0, top_k, 0.0, 0.0, 0.0)

        return BacktestSummary(
            evaluated_draws=evaluated,
            top_k=top_k,
            exact_hit_rate=round(exact_hits / evaluated, 4),
            avg_best_position_matches=round(total_best_position_matches / evaluated, 4),
            avg_best_symbol_overlap=round(total_best_overlap / evaluated, 4),
        )


class PortfolioBuilderAgent:
    def run(
        self,
        ai_lines: Sequence[ScoredAiLine],
        recent_draws: Sequence[Sequence[str]],
        double_count: int,
        backup_count: int,
    ) -> PortfolioPlan:
        if double_count < 0 or backup_count < 0:
            raise ValueError("double_count and backup_count must be >= 0.")

        recent_set = {tuple(draw) for draw in recent_draws}
        candidates = list(ai_lines)
        selected: List[ScoredAiLine] = []

        # Diversify by avoiding lines that are too similar to already selected lines.
        for row in candidates:
            line_tuple = _line_to_tuple(row.values)
            if line_tuple in recent_set:
                continue
            if any(
                sum(1 for i, symbol in enumerate(line_tuple) if symbol == prev[i]) >= 3
                for prev in [_line_to_tuple(item.values) for item in selected]
            ):
                continue
            selected.append(row)
            if len(selected) >= double_count + backup_count:
                break

        if len(selected) < double_count + backup_count:
            for row in candidates:
                if row in selected:
                    continue
                selected.append(row)
                if len(selected) >= double_count + backup_count:
                    break

        doubles = [row.values for row in selected[:double_count]]
        backups = [row.values for row in selected[double_count : double_count + backup_count]]
        return PortfolioPlan(double_lines=doubles, backup_lines=backups)


class ReportAgent:
    def render_text(
        self,
        columns: Sequence[str],
        profiles: ProfileRegistry,
        features: FeatureSummary,
        ai_lines: Sequence[ScoredAiLine],
        backtest: BacktestSummary,
        portfolio: PortfolioPlan,
    ) -> str:
        lines: List[str] = []
        lines.append("=== Chance Agency Agents Report ===")
        lines.append(f"Draws loaded: {features.draw_count}")
        lines.append(f"Columns used: {', '.join(columns)}")
        lines.append(f"Line length: {features.line_length}")
        lines.append("")
        lines.append("Agency profile mapping:")
        if profiles.loaded:
            for profile in profiles.loaded:
                lines.append(f"  {profile.role}: {profile.name} ({profile.path})")
        else:
            lines.append("  no external agency profiles loaded")
        if profiles.missing_roles:
            lines.append(f"  missing roles: {', '.join(profiles.missing_roles)}")
        lines.append("")
        lines.append("Top values:")
        lines.append(", ".join(features.top_values))
        lines.append("")
        lines.append("Position leaders:")
        for idx, leaders in enumerate(features.position_leaders, start=1):
            packed = ", ".join(f"{symbol}:{count}" for symbol, count in leaders)
            lines.append(f"  position {idx}: {packed}")
        lines.append("")
        lines.append("Backtest summary:")
        if backtest.evaluated_draws == 0:
            lines.append("  not enough history to evaluate")
        else:
            lines.append(
                f"  evaluated draws: {backtest.evaluated_draws} (top-{backtest.top_k} predictions each)"
            )
            lines.append(f"  exact hit rate: {backtest.exact_hit_rate:.2%}")
            lines.append(f"  avg best position matches: {backtest.avg_best_position_matches:.2f}/4")
            lines.append(f"  avg best symbol overlap: {backtest.avg_best_symbol_overlap:.2f}/4")
        lines.append("")
        lines.append("Top AI lines:")
        lines.append("values\tscore\tprobability\ttransition\trecency\tsynergy\tseen_before")
        for row in ai_lines:
            lines.append(
                f"{row.values}\t{row.score:.9f}\t{row.probability:.9f}\t"
                f"{row.transition_bonus:.6f}\t{row.recency_bonus:.6f}\t"
                f"{row.synergy_bonus:.6f}\t{row.seen_before}"
            )
        lines.append("")
        lines.append("Portfolio plan:")
        lines.append("  double lines:")
        for idx, line in enumerate(portfolio.double_lines, start=1):
            lines.append(f"    {idx}. {line}")
        lines.append("  backup lines:")
        for idx, line in enumerate(portfolio.backup_lines, start=1):
            lines.append(f"    {idx}. {line}")
        return "\n".join(lines)

    def render_json(
        self,
        columns: Sequence[str],
        profiles: ProfileRegistry,
        features: FeatureSummary,
        ai_lines: Sequence[ScoredAiLine],
        backtest: BacktestSummary,
        portfolio: PortfolioPlan,
    ) -> str:
        payload = {
            "columns": list(columns),
            "profiles": {
                "loaded": [asdict(profile) for profile in profiles.loaded],
                "missing_roles": profiles.missing_roles,
            },
            "features": asdict(features),
            "backtest": asdict(backtest),
            "ai_lines": [asdict(item) for item in ai_lines],
            "portfolio": asdict(portfolio),
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)


def _parse_csv_list(raw: str | None) -> List[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a multi-agent analytics and prediction pipeline for Chance history.",
    )
    parser.add_argument("--input", required=True, help="Path to history CSV file.")
    parser.add_argument(
        "--columns",
        default="",
        help="Optional comma-separated value columns. Empty = auto-detect.",
    )
    parser.add_argument(
        "--exclude-columns",
        default="",
        help="Comma-separated columns to exclude.",
    )
    parser.add_argument(
        "--recent-window",
        default="0.3",
        help='Recent window for momentum logic (e.g. "0.3" or "20").',
    )
    parser.add_argument("--top-ai", type=int, default=12, help="How many AI lines to produce.")
    parser.add_argument(
        "--ai-position-top-k",
        type=int,
        default=5,
        help="Candidate symbols kept per position.",
    )
    parser.add_argument(
        "--ai-half-life",
        type=float,
        default=16.0,
        help="Exponential decay half-life in draws.",
    )
    parser.add_argument(
        "--ai-smoothing",
        type=float,
        default=0.15,
        help="Laplace smoothing constant.",
    )
    parser.add_argument(
        "--ai-novelty-lookback",
        type=int,
        default=8,
        help="Recent draw lookback for repeat-penalty.",
    )
    parser.add_argument(
        "--backtest-last",
        type=int,
        default=20,
        help="How many most recent draws to evaluate in walk-forward backtest.",
    )
    parser.add_argument(
        "--backtest-top-k",
        type=int,
        default=7,
        help="How many predicted lines per step are considered in backtest.",
    )
    parser.add_argument(
        "--double-lines",
        type=int,
        default=3,
        help="How many top lines to mark as double.",
    )
    parser.add_argument(
        "--backup-lines",
        type=int,
        default=4,
        help="How many additional lines to mark as backup.",
    )
    parser.add_argument(
        "--output-json",
        default=None,
        help="Optional output path to save full report JSON.",
    )
    parser.add_argument(
        "--agency-profiles-dir",
        default="",
        help="Optional path to external agency-agents repository root.",
    )
    parser.add_argument(
        "--strict-profiles",
        action="store_true",
        help="Fail if required agency profiles are missing.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()

    collector = DataCollectorAgent()
    profile_loader = AgencyProfileAgent()
    analyst = FeatureAnalystAgent()
    predictor = AIPredictorAgent()
    backtester = BacktestAgent()
    portfolio_builder = PortfolioBuilderAgent()
    reporter = ReportAgent()

    columns = _parse_csv_list(args.columns)
    exclude_columns = _parse_csv_list(args.exclude_columns)

    draws, chosen_columns = collector.run(
        csv_path=Path(args.input),
        columns=columns or None,
        exclude_columns=exclude_columns or None,
    )
    profiles = ProfileRegistry(loaded=[], missing_roles=[])
    if args.agency_profiles_dir:
        profiles = profile_loader.run(Path(args.agency_profiles_dir), strict=args.strict_profiles)

    features = analyst.run(draws=draws, recent_window=args.recent_window)
    ai_lines = predictor.run(
        draws=draws,
        top_ai=args.top_ai,
        ai_position_top_k=args.ai_position_top_k,
        ai_half_life=args.ai_half_life,
        ai_smoothing=args.ai_smoothing,
        ai_novelty_lookback=args.ai_novelty_lookback,
        recent_window=args.recent_window,
    )
    backtest = backtester.run(
        draws=draws,
        evaluate_last=args.backtest_last,
        top_k=args.backtest_top_k,
        ai_position_top_k=args.ai_position_top_k,
        ai_half_life=args.ai_half_life,
        ai_smoothing=args.ai_smoothing,
        ai_novelty_lookback=args.ai_novelty_lookback,
        recent_window=args.recent_window,
    )
    portfolio = portfolio_builder.run(
        ai_lines=ai_lines,
        recent_draws=draws[-args.ai_novelty_lookback :],
        double_count=args.double_lines,
        backup_count=args.backup_lines,
    )

    text_report = reporter.render_text(
        columns=chosen_columns,
        profiles=profiles,
        features=features,
        ai_lines=ai_lines,
        backtest=backtest,
        portfolio=portfolio,
    )
    print(text_report)

    if args.output_json:
        output_path = Path(args.output_json)
        output_path.write_text(
            reporter.render_json(
                columns=chosen_columns,
                profiles=profiles,
                features=features,
                ai_lines=ai_lines,
                backtest=backtest,
                portfolio=portfolio,
            ),
            encoding="utf-8",
        )
        print(f"\nSaved JSON report to: {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
