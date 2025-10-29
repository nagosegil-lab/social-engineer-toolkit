from __future__ import annotations

import argparse
import sys
import time
from typing import Literal, Optional

import pandas as pd

from .config import get_settings, Settings
from .core.features import build_features
from .core.model import StrategyModel
from .notify.telegram import send_message

# Optional imports guarded at runtime
try:
    from .connectors.mt5_client import MT5Client  # type: ignore
except Exception:  # pragma: no cover
    MT5Client = None  # type: ignore

try:
    from .connectors.metaapi_client import MetaApiClient  # type: ignore
except Exception:  # pragma: no cover
    MetaApiClient = None  # type: ignore


def _notify(settings: Settings, text: str) -> None:
    if settings.telegram_bot_token and settings.telegram_chat_id:
        send_message(settings.telegram_bot_token, settings.telegram_chat_id, text)


def _get_client(settings: Settings):
    conn = settings.connector.lower()
    if conn == "mt5":
        if MT5Client is None:
            raise RuntimeError("MT5 connector unavailable. Install MetaTrader5 on a Windows/VPS environment.")
        client = MT5Client(settings.mt5_login, settings.mt5_password, settings.mt5_server)
        client.initialize()
        return client
    elif conn == "metaapi":
        if MetaApiClient is None:
            raise RuntimeError("MetaApi connector unavailable. Install metaapi-cloud-sdk.")
        client = MetaApiClient(settings.metaapi_token, settings.metaapi_account_id)
        client.initialize()
        return client
    else:
        raise ValueError(f"Unknown connector: {settings.connector}")


def _decide_signal(prob_up: float, buy_threshold: float = 0.55, sell_threshold: float = 0.45) -> Literal["BUY", "SELL", "FLAT"]:
    if prob_up >= buy_threshold:
        return "BUY"
    if prob_up <= sell_threshold:
        return "SELL"
    return "FLAT"


def trade_once(settings: Settings) -> None:
    client = _get_client(settings)
    try:
        candles: pd.DataFrame = client.get_candles(settings.symbol, settings.timeframe, count=400)
        if candles is None or candles.empty:
            _notify(settings, f"No candles for {settings.symbol} {settings.timeframe}")
            print("No data; skipping.")
            return

        feats = build_features(candles)
        if feats.empty:
            print("Not enough data for features yet; skipping.")
            return

        model = StrategyModel(settings.model_path)
        prob_up = float(model.predict_proba(feats))
        signal = _decide_signal(prob_up)

        _notify(settings, f"Signal {settings.symbol} {settings.timeframe}: {signal} (p_up={prob_up:.3f})")
        print(f"Signal: {signal} (p_up={prob_up:.3f})")

        if signal == "FLAT":
            return

        result = client.place_market_order(
            symbol=settings.symbol,
            side=signal,
            volume=settings.lot,
            sl_points=settings.sl_points,
            tp_points=settings.tp_points,
            deviation=settings.deviation,
            magic=234000,
            comment="ai-bot",
        )
        _notify(settings, f"Order result: {result}")
        print(f"Order result: {result}")
    finally:
        try:
            client.shutdown()
        except Exception:
            pass


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="MT5/MetaApi AI trading bot")
    parser.add_argument("--once", action="store_true", help="Run a single iteration and exit")
    parser.add_argument("--every", type=int, default=60, help="Interval seconds between runs in loop mode")
    parser.add_argument("--connector", type=str, choices=["mt5", "metaapi"], help="Override connector from env")
    args = parser.parse_args(argv)

    settings = get_settings()
    if args.connector:
        settings.connector = args.connector

    if args.once:
        trade_once(settings)
        return 0

    print(f"Starting loop: symbol={settings.symbol} tf={settings.timeframe} connector={settings.connector}")
    while True:
        try:
            trade_once(settings)
        except KeyboardInterrupt:
            print("Interrupted.")
            break
        except Exception as exc:
            _notify(settings, f"Run error: {exc}")
            print(f"Error: {exc}")
        time.sleep(max(5, int(args.every)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
