from __future__ import annotations

import argparse
import sys
import os
import time
import datetime as dt
from typing import Literal, Optional

import pandas as pd

from .config import get_settings, Settings
from .core.features import build_features
from .core.model import StrategyModel
from .notify.telegram import send_message
from .core.risk import BotState, StateStore, RiskConfig, RiskManager
from .core.logging_utils import setup_logger, append_csv_row
from zoneinfo import ZoneInfo

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


def _within_trading_hours(settings: Settings, now: dt.datetime) -> bool:
    hours = (settings.trading_hours or "").strip()
    if not hours:
        return True
    try:
        start_s, end_s = [h.strip() for h in hours.split("-")]
        start_h, start_m = [int(x) for x in start_s.split(":")]
        end_h, end_m = [int(x) for x in end_s.split(":")]
        start_t = dt.time(hour=start_h, minute=start_m)
        end_t = dt.time(hour=end_h, minute=end_m)
        t = now.timetz()
        if end_t > start_t:
            return start_t <= t < end_t
        # overnight window
        return not (end_t <= t < start_t)
    except Exception:
        return True


def _net_exposure_lots(positions: list[dict[str, object]]) -> float:
    exposure = 0.0
    for p in positions:
        typ = int(p.get("type", 0))  # 0=BUY,1=SELL
        vol = float(p.get("volume", 0.0))
        exposure += vol if typ == 0 else -vol
    return exposure


def trade_once(settings: Settings) -> None:
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    logger = setup_logger(os.path.join(data_dir, "logs.log"))
    state_store = StateStore(os.path.join(data_dir, "bot_state.json"))
    state = state_store.load()

    client = _get_client(settings)
    try:
        candles: pd.DataFrame = client.get_candles(settings.symbol, settings.timeframe, count=400)
        if candles is None or candles.empty:
            _notify(settings, f"No candles for {settings.symbol} {settings.timeframe}")
            logger.warning("No data; skipping.")
            return

        feats = build_features(candles)
        if feats.empty:
            logger.info("Not enough data for features yet; skipping.")
            return

        model = StrategyModel(settings.model_path)
        prob_up = float(model.predict_proba(feats))
        signal = _decide_signal(prob_up)

        last_bar_time = feats.iloc[-1]["time"]
        if not isinstance(last_bar_time, dt.datetime):
            last_bar_time = pd.to_datetime(last_bar_time)
        last_bar_iso = last_bar_time.replace(tzinfo=dt.timezone.utc).isoformat() if last_bar_time.tzinfo is None else last_bar_time.isoformat()

        append_csv_row(os.path.join(data_dir, "signals.csv"), {
            "ts": dt.datetime.utcnow().isoformat(),
            "symbol": settings.symbol,
            "timeframe": settings.timeframe,
            "prob_up": round(prob_up, 6),
            "signal": signal,
        })
        logger.info(f"Signal {settings.symbol} {settings.timeframe}: {signal} (p_up={prob_up:.3f})")
        _notify(settings, f"Signal {settings.symbol} {settings.timeframe}: {signal} (p_up={prob_up:.3f})")

        if signal == "FLAT":
            return

        now_local = dt.datetime.now(ZoneInfo(settings.timezone or "UTC"))
        if not _within_trading_hours(settings, now_local):
            logger.info("Outside trading hours; skipping trade")
            return

        if state.last_executed_bar_iso == last_bar_iso:
            logger.info("Already traded this bar; skipping")
            return

        # Exposure and risk checks
        try:
            positions = client.get_positions(settings.symbol)  # type: ignore[attr-defined]
        except Exception:
            positions = []
        exposure = _net_exposure_lots(positions)

        risk = RiskManager(
            RiskConfig(
                max_trades_per_day=settings.max_trades_per_day,
                max_daily_loss=settings.max_daily_loss,
                max_exposure_lots=settings.max_exposure_lots,
            ),
            state_store,
        )
        allowed, reason = risk.can_trade(state, exposure)
        if not allowed:
            logger.warning(f"Risk block: {reason}")
            _notify(settings, f"Risk block: {reason}")
            return

        if settings.trade_mode.lower() == "paper":
            append_csv_row(os.path.join(data_dir, "paper_trades.csv"), {
                "ts": dt.datetime.utcnow().isoformat(),
                "symbol": settings.symbol,
                "side": signal,
                "volume": settings.lot,
                "sl_points": settings.sl_points or 0,
                "tp_points": settings.tp_points or 0,
                "bar_iso": last_bar_iso,
            })
            state.last_executed_bar_iso = last_bar_iso
            state = risk.on_order_filled(state)
            logger.info(f"Paper trade: {signal} {settings.symbol} {settings.lot}")
            _notify(settings, f"Paper trade: {signal} {settings.symbol} {settings.lot}")
            return

        # Live order
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
        state.last_executed_bar_iso = last_bar_iso
        state = risk.on_order_filled(state)
        append_csv_row(os.path.join(data_dir, "trades.csv"), {
            "ts": dt.datetime.utcnow().isoformat(),
            "symbol": settings.symbol,
            "side": signal,
            "volume": settings.lot,
            "sl_points": settings.sl_points or 0,
            "tp_points": settings.tp_points or 0,
            "result": str(result),
            "bar_iso": last_bar_iso,
        })
        logger.info(f"Order result: {result}")
        _notify(settings, f"Order result: {result}")
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
    parser.add_argument("--paper", action="store_true", help="Run in paper (no-order) mode")
    parser.add_argument("--hours", type=str, help="Trading hours window, e.g. 08:00-22:00")
    args = parser.parse_args(argv)

    settings = get_settings()
    if args.connector:
        settings.connector = args.connector
    if args.paper:
        settings.trade_mode = "paper"
    if args.hours:
        settings.trading_hours = args.hours

    if args.once:
        trade_once(settings)
        return 0

    print(f"Starting loop: symbol={settings.symbol} tf={settings.timeframe} connector={settings.connector} mode={settings.trade_mode}")
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
