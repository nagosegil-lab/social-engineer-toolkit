from __future__ import annotations

import os
from dataclasses import dataclass

import pandas as pd

try:
    from joblib import load  # type: ignore
except Exception:  # joblib optional at runtime without a model
    load = None  # type: ignore


@dataclass
class StrategyModel:
    model_path: str

    def __post_init__(self) -> None:
        self._model = None
        if self.model_path and os.path.exists(self.model_path) and load is not None:
            try:
                self._model = load(self.model_path)
            except Exception:
                self._model = None

    def predict_proba(self, features_df: pd.DataFrame) -> float:
        """
        Return probability of upward move in next bar.
        If trained model unavailable, fall back to simple SMA rule.
        """
        if self._model is not None:
            last_row = features_df.iloc[-1:]
            X = last_row.drop(columns=[c for c in ["y"] if c in last_row.columns])
            try:
                proba = float(self._model.predict_proba(X)[0][1])
                return proba
            except Exception:
                # fall through to heuristic
                pass

        # Heuristic fallback: if fast SMA above slow -> bullish bias
        sma_diff = float(features_df.iloc[-1]["sma_diff"]) if "sma_diff" in features_df.columns else 0.0
        return 0.6 if sma_diff > 0 else 0.4
