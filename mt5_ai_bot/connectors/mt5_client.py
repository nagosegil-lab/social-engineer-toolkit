from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, List

import pandas as pd


@dataclass
class MT5Client:
    login: int
    password: str
    server: str

    def __post_init__(self) -> None:
        self._mt5 = None

    # --- lifecycle ---
    def initialize(self) -> None:
        try:
            import MetaTrader5 as mt5  # type: ignore
        except Exception as exc:  # pragma: no cover - optional dep
            raise RuntimeError(
                "MetaTrader5 package not installed. Install on Windows/VPS with MT5: pip install MetaTrader5"
            ) from exc

        if not mt5.initialize(login=self.login, server=self.server, password=self.password):
            raise RuntimeError("Failed to initialize MT5. Check credentials and terminal state.")
        self._mt5 = mt5

    def shutdown(self) -> None:
        if self._mt5 is not None:
            self._mt5.shutdown()
            self._mt5 = None

    # --- helpers ---
    def _require(self) -> Any:
        if self._mt5 is None:
            raise RuntimeError("MT5 not initialized. Call initialize() first.")
        return self._mt5

    def ensure_symbol(self, symbol: str) -> Any:
        mt5 = self._require()
        info = mt5.symbol_info(symbol)
        if info is None or not info.visible:
            if not mt5.symbol_select(symbol, True):
                raise RuntimeError(f"Unable to select symbol {symbol}")
            info = mt5.symbol_info(symbol)
        return info

    def _map_timeframe(self, timeframe: str) -> int:
        mt5 = self._require()
        tf = timeframe.upper()
        tf_map = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "M30": mt5.TIMEFRAME_M30,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1,
        }
        if tf not in tf_map:
            raise ValueError(f"Unsupported timeframe: {timeframe}")
        return tf_map[tf]

    # --- data ---
    def get_candles(self, symbol: str, timeframe: str, count: int = 300) -> pd.DataFrame:
        mt5 = self._require()
        self.ensure_symbol(symbol)
        tf = self._map_timeframe(timeframe)
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, count)
        frame = pd.DataFrame(rates)
        if frame.empty:
            return frame
        frame["time"] = pd.to_datetime(frame["time"], unit="s")
        frame.rename(columns={"tick_volume": "volume"}, inplace=True)
        return frame[["time", "open", "high", "low", "close", "volume"]]

    def get_tick(self, symbol: str) -> Dict[str, float]:
        mt5 = self._require()
        self.ensure_symbol(symbol)
        tick = mt5.symbol_info_tick(symbol)
        return {"bid": float(tick.bid), "ask": float(tick.ask)}

    def get_positions(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return open positions. If symbol provided, filter by symbol."""
        mt5 = self._require()
        if symbol:
            positions = mt5.positions_get(symbol=symbol)
        else:
            positions = mt5.positions_get()
        result: List[Dict[str, Any]] = []
        if positions is None:
            return result
        for p in positions:
            result.append({
                "ticket": int(p.ticket),
                "symbol": str(p.symbol),
                "type": int(p.type),  # 0=BUY,1=SELL
                "volume": float(p.volume),
                "price_open": float(p.price_open),
                "sl": float(p.sl) if p.sl else None,
                "tp": float(p.tp) if p.tp else None,
                "profit": float(p.profit),
                "magic": int(p.magic),
                "time": int(p.time),
            })
        return result

    # --- trading ---
    def place_market_order(
        self,
        symbol: str,
        side: str,
        volume: float,
        sl_points: Optional[int] = None,
        tp_points: Optional[int] = None,
        deviation: int = 20,
        magic: int = 234000,
        comment: str = "ai-bot",
    ) -> Any:
        mt5 = self._require()
        side_u = side.upper()
        if side_u not in ("BUY", "SELL"):
            raise ValueError("side must be BUY or SELL")

        info = self.ensure_symbol(symbol)
        point = float(info.point)
        tick = mt5.symbol_info_tick(symbol)
        price = float(tick.ask) if side_u == "BUY" else float(tick.bid)

        order_type = mt5.ORDER_TYPE_BUY if side_u == "BUY" else mt5.ORDER_TYPE_SELL

        sl_price = None
        tp_price = None
        if sl_points is not None and sl_points > 0:
            sl_price = price - sl_points * point if side_u == "BUY" else price + sl_points * point
        if tp_points is not None and tp_points > 0:
            tp_price = price + tp_points * point if side_u == "BUY" else price - tp_points * point

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(volume),
            "type": order_type,
            "price": price,
            "sl": sl_price,
            "tp": tp_price,
            "deviation": int(deviation),
            "magic": int(magic),
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        return mt5.order_send(request)
