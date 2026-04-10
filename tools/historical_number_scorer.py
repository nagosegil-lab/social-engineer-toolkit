#!/usr/bin/env python3
"""Score values based on historical draw data.

The script reads a CSV file where each row represents one historical draw.
It then scores each value using a weighted blend of:
1) frequency
2) recency
3) trend (recent-vs-old appearance rate)
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


DEFAULT_IGNORE_COLUMN_KEYWORDS = (
    "id",
    "draw_id",
    "draw number",
    "date",
    "time",
    "datetime",
    "timestamp",
    "#",
    "תאריך",
    "שעה",
    "זמן",
    "מספר הגרלה",
)


@dataclass(frozen=True)
class ScoredValue:
    value: str
    score: float
    frequency: int
    frequency_ratio: float
    recency_score: float
    trend_ratio: float
    last_seen_draw: int
    draws_since_last_seen: int


def _normalize_token(raw: str) -> str:
    return raw.strip().upper()


def _is_probably_datetime(value: str) -> bool:
    value = value.strip()
    if not value:
        return False
    return ("/" in value or "-" in value) and ":" in value


def infer_value_columns(fieldnames: Sequence[str], rows: Sequence[Dict[str, str]]) -> List[str]:
    """Pick likely value columns if the user did not provide them."""
    selected: List[str] = []
    for field in fieldnames:
        normalized = field.strip().lower()
        if any(keyword in normalized for keyword in DEFAULT_IGNORE_COLUMN_KEYWORDS):
            continue

        values = [row.get(field, "").strip() for row in rows]
        non_empty = [v for v in values if v]
        if not non_empty:
            continue

        datetime_ratio = sum(_is_probably_datetime(v) for v in non_empty) / len(non_empty)
        if datetime_ratio > 0.8:
            continue

        distinct_ratio = len(set(non_empty)) / len(non_empty)
        numeric_ratio = sum(v.isdigit() for v in non_empty) / len(non_empty)
        avg_len = sum(len(v) for v in non_empty) / len(non_empty)
        # Heuristic for identifier-like columns (usually monotonically increasing IDs).
        if distinct_ratio > 0.9 and numeric_ratio > 0.9 and avg_len >= 4:
            continue

        selected.append(field)

    if not selected:
        raise ValueError(
            "Could not infer value columns. Pass explicit columns using --columns col1 col2 ..."
        )
    return selected


def load_draws_from_csv(
    csv_path: Path,
    columns: Sequence[str] | None = None,
    exclude_columns: Sequence[str] | None = None,
) -> Tuple[List[List[str]], List[str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    if not fieldnames:
        raise ValueError("CSV has no header row.")
    if not rows:
        raise ValueError("CSV has no data rows.")

    chosen_columns = list(columns) if columns else infer_value_columns(fieldnames, rows)
    excluded = {column.strip().lower() for column in (exclude_columns or [])}
    chosen_columns = [column for column in chosen_columns if column.strip().lower() not in excluded]

    missing = [column for column in chosen_columns if column not in fieldnames]
    if missing:
        raise ValueError(f"Columns not found in CSV header: {missing}")
    if not chosen_columns:
        raise ValueError("No usable columns remain after exclusions.")

    draws: List[List[str]] = []
    for row in rows:
        values: List[str] = []
        for column in chosen_columns:
            token = _normalize_token(row.get(column, ""))
            if token:
                values.append(token)
        if values:
            draws.append(values)

    if not draws:
        raise ValueError("No values were extracted from the selected columns.")
    return draws, chosen_columns


def normalize_weights(weights: Sequence[float]) -> Tuple[float, float, float]:
    if len(weights) != 3:
        raise ValueError("Weights must include exactly 3 numbers: frequency recency trend.")
    if any(weight < 0 for weight in weights):
        raise ValueError("Weights cannot be negative.")

    total = sum(weights)
    if total == 0:
        raise ValueError("At least one weight must be greater than 0.")

    return tuple(weight / total for weight in weights)  # type: ignore[return-value]


def _resolve_recent_window(recent_window: str, total_draws: int) -> int:
    """Resolve recent-window input.

    Supports:
    - Integer draws (e.g., "20")
    - Fraction of history in (0, 1], e.g. "0.3"
    """
    recent_window = recent_window.strip()
    if not recent_window:
        raise ValueError("recent-window cannot be empty.")

    if "." in recent_window:
        ratio = float(recent_window)
        if not (0 < ratio <= 1):
            raise ValueError("Fractional recent-window must be in (0, 1].")
        return max(1, math.ceil(total_draws * ratio))

    draws = int(recent_window)
    if draws <= 0:
        raise ValueError("Integer recent-window must be > 0.")
    return min(draws, total_draws)


def score_values(
    draws: Sequence[Sequence[str]],
    weights: Sequence[float] = (0.6, 0.25, 0.15),
    recent_window: str = "0.3",
    min_frequency: int = 1,
) -> List[ScoredValue]:
    if not draws:
        return []

    freq_weight, recency_weight, trend_weight = normalize_weights(weights)
    total_draws = len(draws)
    recent_draw_count = _resolve_recent_window(recent_window, total_draws)
    recent_start_index = total_draws - recent_draw_count

    frequency: Dict[str, int] = {}
    last_seen: Dict[str, int] = {}
    recent_frequency: Dict[str, int] = {}

    for draw_idx, draw_values in enumerate(draws):
        for value in draw_values:
            frequency[value] = frequency.get(value, 0) + 1
            last_seen[value] = draw_idx
            if draw_idx >= recent_start_index:
                recent_frequency[value] = recent_frequency.get(value, 0) + 1

    frequency = {value: count for value, count in frequency.items() if count >= min_frequency}
    if not frequency:
        return []

    old_draw_count = max(1, total_draws - recent_draw_count)
    max_frequency = max(frequency.values())

    trend_raw: Dict[str, float] = {}
    for value, count in frequency.items():
        recent_count = recent_frequency.get(value, 0)
        old_count = count - recent_count

        recent_rate = recent_count / recent_draw_count
        old_rate = old_count / old_draw_count
        if old_rate == 0:
            trend_raw[value] = 2.0 if recent_rate > 0 else 1.0
        else:
            trend_raw[value] = recent_rate / old_rate

    trend_values = list(trend_raw.values())
    min_trend = min(trend_values)
    max_trend = max(trend_values)
    trend_span = max(max_trend - min_trend, 1e-9)

    scored: List[ScoredValue] = []
    for value, count in frequency.items():
        freq_norm = count / max_frequency
        age = (total_draws - 1) - last_seen[value]
        recency = 1.0 if total_draws == 1 else 1 - (age / (total_draws - 1))
        trend_norm = (trend_raw[value] - min_trend) / trend_span

        score = (
            freq_weight * freq_norm
            + recency_weight * recency
            + trend_weight * trend_norm
        )

        scored.append(
            ScoredValue(
                value=value,
                score=round(score, 6),
                frequency=count,
                frequency_ratio=round(count / sum(frequency.values()), 6),
                recency_score=round(recency, 6),
                trend_ratio=round(trend_raw[value], 6),
                last_seen_draw=last_seen[value],
                draws_since_last_seen=age,
            )
        )

    scored.sort(key=lambda row: (row.score, row.frequency, -row.draws_since_last_seen), reverse=True)
    return scored


def write_scores_csv(path: Path, scored_values: Iterable[ScoredValue]) -> None:
    items = list(scored_values)
    if not items:
        return

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(items[0]).keys()))
        writer.writeheader()
        for item in items:
            writer.writerow(asdict(item))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Score values based on historical CSV data.",
    )
    parser.add_argument("--input", required=True, help="Path to history CSV file.")
    parser.add_argument(
        "--columns",
        nargs="+",
        default=None,
        help="Value columns to include. If omitted, columns are auto-detected.",
    )
    parser.add_argument(
        "--exclude-columns",
        nargs="+",
        default=[],
        help="Columns to exclude from analysis.",
    )
    parser.add_argument(
        "--weights",
        nargs=3,
        type=float,
        default=[0.6, 0.25, 0.15],
        metavar=("FREQUENCY", "RECENCY", "TREND"),
        help="Weight triplet for frequency, recency, trend.",
    )
    parser.add_argument(
        "--recent-window",
        default="0.3",
        help='Recent window: integer draw count (e.g. "20") or fraction (e.g. "0.3").',
    )
    parser.add_argument("--top", type=int, default=10, help="How many top values to print.")
    parser.add_argument(
        "--min-frequency",
        type=int,
        default=1,
        help="Filter values that appeared fewer than this number of times.",
    )
    parser.add_argument(
        "--output-csv",
        default=None,
        help="Optional output path to save full scored table as CSV.",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    csv_path = Path(args.input)
    draws, chosen_columns = load_draws_from_csv(
        csv_path=csv_path,
        columns=args.columns,
        exclude_columns=args.exclude_columns,
    )

    scored = score_values(
        draws=draws,
        weights=args.weights,
        recent_window=args.recent_window,
        min_frequency=args.min_frequency,
    )

    print(f"Loaded {len(draws)} draws from {csv_path}")
    print(f"Using columns: {', '.join(chosen_columns)}")
    print(f"Scored distinct values: {len(scored)}")
    print()
    print("Top values:")
    print("value\tscore\tfrequency\trecency\ttrend_ratio")
    for row in scored[: args.top]:
        print(
            f"{row.value}\t{row.score:.6f}\t{row.frequency}\t"
            f"{row.recency_score:.6f}\t{row.trend_ratio:.6f}"
        )

    if args.output_csv:
        out_path = Path(args.output_csv)
        write_scores_csv(out_path, scored)
        print(f"\nSaved full score table to: {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
