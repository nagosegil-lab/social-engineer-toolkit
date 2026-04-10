#!/usr/bin/env python3
"""Simple desktop GUI for historical number scorer."""

from __future__ import annotations

from pathlib import Path
from typing import List

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, scrolledtext, ttk

    TK_AVAILABLE = True
    TK_IMPORT_ERROR: Exception | None = None
except ModuleNotFoundError as exc:
    tk = None  # type: ignore[assignment]
    filedialog = messagebox = scrolledtext = ttk = None  # type: ignore[assignment]
    TK_AVAILABLE = False
    TK_IMPORT_ERROR = exc

from historical_number_scorer import (
    ScoredCombination,
    ScoredValue,
    load_draws_from_csv,
    score_combinations,
    score_values,
)


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Historical Number Scorer")
        self.root.geometry("980x680")

        self.csv_path_var = tk.StringVar()
        self.columns_var = tk.StringVar()
        self.exclude_columns_var = tk.StringVar(value="datetime,draw_id")
        self.weights_var = tk.StringVar(value="0.6,0.25,0.15")
        self.recent_window_var = tk.StringVar(value="0.3")
        self.min_frequency_var = tk.StringVar(value="1")
        self.top_values_var = tk.StringVar(value="10")
        self.combo_size_var = tk.StringVar(value="0")
        self.top_combos_var = tk.StringVar(value="10")

        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill="both", expand=True)

        row = 0
        ttk.Label(frame, text="CSV file").grid(row=row, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.csv_path_var, width=90).grid(
            row=row, column=1, sticky="ew", padx=(8, 8)
        )
        ttk.Button(frame, text="Browse...", command=self.browse_file).grid(row=row, column=2, sticky="e")

        row += 1
        ttk.Label(frame, text="Columns (optional, comma-separated)").grid(row=row, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.columns_var).grid(row=row, column=1, columnspan=2, sticky="ew", padx=(8, 0))

        row += 1
        ttk.Label(frame, text="Exclude columns (comma-separated)").grid(row=row, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.exclude_columns_var).grid(
            row=row, column=1, columnspan=2, sticky="ew", padx=(8, 0)
        )

        row += 1
        ttk.Label(frame, text="Weights freq,recency,trend").grid(row=row, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.weights_var).grid(row=row, column=1, sticky="ew", padx=(8, 8))
        ttk.Label(frame, text="Example: 0.6,0.25,0.15").grid(row=row, column=2, sticky="w")

        row += 1
        ttk.Label(frame, text="Recent window").grid(row=row, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.recent_window_var).grid(row=row, column=1, sticky="ew", padx=(8, 8))
        ttk.Label(frame, text="Integer draws or ratio (0.3)").grid(row=row, column=2, sticky="w")

        row += 1
        ttk.Label(frame, text="Min frequency").grid(row=row, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.min_frequency_var).grid(row=row, column=1, sticky="ew", padx=(8, 8))
        ttk.Label(frame, text="Top values").grid(row=row, column=2, sticky="w")
        ttk.Entry(frame, textvariable=self.top_values_var, width=10).grid(row=row, column=2, sticky="e")

        row += 1
        ttk.Separator(frame, orient="horizontal").grid(row=row, column=0, columnspan=3, sticky="ew", pady=10)

        row += 1
        ttk.Label(frame, text="Combination size (0 = off)").grid(row=row, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.combo_size_var).grid(row=row, column=1, sticky="ew", padx=(8, 8))
        ttk.Label(frame, text="Top combinations").grid(row=row, column=2, sticky="w")
        ttk.Entry(frame, textvariable=self.top_combos_var, width=10).grid(row=row, column=2, sticky="e")

        row += 1
        ttk.Button(frame, text="Run analysis", command=self.run_analysis).grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=(8, 10)
        )

        row += 1
        self.output = scrolledtext.ScrolledText(frame, wrap="word", height=22)
        self.output.grid(row=row, column=0, columnspan=3, sticky="nsew")

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(row, weight=1)

    def browse_file(self) -> None:
        selected = filedialog.askopenfilename(
            title="Choose history CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if selected:
            self.csv_path_var.set(selected)

    @staticmethod
    def _parse_csv_list(raw: str) -> List[str]:
        return [item.strip() for item in raw.split(",") if item.strip()]

    def _format_values(self, rows: List[ScoredValue], limit: int) -> str:
        lines = [
            "Top values:",
            "value\tscore\tfrequency\trecency\ttrend_ratio",
        ]
        for row in rows[:limit]:
            lines.append(
                f"{row.value}\t{row.score:.6f}\t{row.frequency}\t"
                f"{row.recency_score:.6f}\t{row.trend_ratio:.6f}"
            )
        return "\n".join(lines)

    def _format_combos(self, rows: List[ScoredCombination], limit: int, combo_size: int) -> str:
        lines = [
            f"Top combinations (size={combo_size}):",
            "values\tscore\tfrequency\trecency\ttrend_ratio",
        ]
        for row in rows[:limit]:
            lines.append(
                f"{row.values}\t{row.score:.6f}\t{row.frequency}\t"
                f"{row.recency_score:.6f}\t{row.trend_ratio:.6f}"
            )
        if len(lines) == 2:
            lines.append("No combinations found for current filters.")
        return "\n".join(lines)

    def run_analysis(self) -> None:
        try:
            csv_path = Path(self.csv_path_var.get().strip())
            if not csv_path.exists():
                raise ValueError("CSV file does not exist.")

            columns = self._parse_csv_list(self.columns_var.get())
            exclude_columns = self._parse_csv_list(self.exclude_columns_var.get())

            weights_list = self._parse_csv_list(self.weights_var.get())
            if len(weights_list) != 3:
                raise ValueError("Weights must include exactly 3 comma-separated values.")
            weights = [float(value) for value in weights_list]

            recent_window = self.recent_window_var.get().strip()
            min_frequency = int(self.min_frequency_var.get().strip())
            top_values = int(self.top_values_var.get().strip())
            combo_size = int(self.combo_size_var.get().strip())
            top_combos = int(self.top_combos_var.get().strip())

            draws, chosen_columns = load_draws_from_csv(
                csv_path=csv_path,
                columns=columns or None,
                exclude_columns=exclude_columns or None,
            )
            scored_values = score_values(
                draws=draws,
                weights=weights,
                recent_window=recent_window,
                min_frequency=min_frequency,
            )

            sections = [
                f"Loaded {len(draws)} draws from {csv_path}",
                f"Using columns: {', '.join(chosen_columns)}",
                f"Scored distinct values: {len(scored_values)}",
                "",
                self._format_values(scored_values, top_values),
            ]

            if combo_size >= 2:
                combos = score_combinations(
                    draws=draws,
                    combo_size=combo_size,
                    weights=weights,
                    recent_window=recent_window,
                    min_frequency=min_frequency,
                )
                sections.extend(["", self._format_combos(combos, top_combos, combo_size)])

            self.output.delete("1.0", "end")
            self.output.insert("1.0", "\n".join(sections))
        except Exception as exc:  # noqa: BLE001 - GUI should show user-readable errors.
            messagebox.showerror("Analysis failed", str(exc))


def main() -> int:
    if not TK_AVAILABLE:
        print(
            "Tkinter is not installed in this environment. "
            "Install python3-tk (Linux) and run again."
        )
        if TK_IMPORT_ERROR:
            print(f"Details: {TK_IMPORT_ERROR}")
        return 1

    assert tk is not None
    root = tk.Tk()
    App(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
