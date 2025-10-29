from __future__ import annotations

import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build simple price-based features on OHLCV dataframe.
    Expects columns: ['time','open','high','low','close','volume']
    """
    frame = df.copy()
    frame.sort_values("time", inplace=True)

    frame["ret"] = frame["close"].pct_change()
    frame["sma_fast"] = frame["close"].rolling(10).mean()
    frame["sma_slow"] = frame["close"].rolling(50).mean()
    frame["sma_diff"] = frame["sma_fast"] - frame["sma_slow"]

    # Forward-looking label for training (not used at inference time)
    frame["y"] = (frame["close"].shift(-1) > frame["close"]).astype(int)
    return frame.dropna()
