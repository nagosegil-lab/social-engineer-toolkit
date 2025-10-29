from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, Optional, List

import pandas as pd


@dataclass
class MetaApiClient:
    token: str
    account_id: str

    def __post_init__(self) -> None:
        self._conn = None
        self._account = None
        self._sdk = None

    # --- lifecycle ---
    def initialize(self) -> None:
        try:
            # metaapi-cloud-sdk is async
            from metaapi_cloud_sdk import MetaApi  # type: ignore
        except Exception as exc:  # pragma: no cover - optional dep
            raise RuntimeError(
                "metaapi-cloud-sdk not installed. Install with: pip install metaapi-cloud-sdk"
            ) from exc

        async def _a_init() -> None:
            sdk = MetaApi(self.token)
            account = await sdk.metatrader_account_api.get_account(self.account_id)
            await account.reload()
            if account.state != 'DEPLOYED':
                await account.deploy()
            if account.connection_status != 'CONNECTED':
                await account.wait_connected()

            conn = await account.get_rpc_connection()
            await conn.connect()
            await conn.wait_synchronized()

            self._sdk = sdk
            self._account = account
            self._conn = conn

        asyncio.run(_a_init())

    def shutdown(self) -> None:
        async def _a_shutdown() -> None:
            if self._conn is not None:
                try:
                    await self._conn.close()
                except Exception:
                    pass
        try:
            asyncio.run(_a_shutdown())
        except RuntimeError:
            # already closed or loop context; ignore
            pass
        finally:
            self._conn = None
            self._account = None
            self._sdk = None

    def _require(self):
        if self._conn is None:
            raise RuntimeError("MetaApi not initialized. Call initialize() first.")
        return self._conn

    # --- utils ---
    @staticmethod
    def _map_timeframe(tf: str) -> str:
        tf_u = tf.upper()
        mapping = {"M1": "1m", "M5": "5m", "M15": "15m", "M30": "30m", "H1": "1h", "H4": "4h", "D1": "1d"}
        if tf_u not in mapping:
            raise ValueError(f"Unsupported timeframe: {tf}")
        return mapping[tf_u]

    # --- data ---
    def get_candles(self, symbol: str, timeframe: str, count: int = 300) -> pd.DataFrame:
        conn = self._require()
        tf_api = self._map_timeframe(timeframe)

        async def _a_get() -> pd.DataFrame:
            candles = await conn.get_candles(symbol, tf_api, count)
            if not candles:
                return pd.DataFrame(columns=["time", "open", "high", "low", "close", "volume"])
            frame = pd.DataFrame([{
                "time": c.time,
                "open": c.open,
                "high": c.high,
                "low": c.low,
                "close": c.close,
                "volume": c.tick_volume if hasattr(c, 'tick_volume') else c.volume,
            } for c in candles])
            frame["time"] = pd.to_datetime(frame["time"], utc=True)
            return frame[["time", "open", "high", "low", "close", "volume"]]

        return asyncio.run(_a_get())

    def get_tick(self, symbol: str) -> Dict[str, float]:
        conn = self._require()

        async def _a_tick() -> Dict[str, float]:
            price = await conn.get_symbol_price(symbol)
            return {"bid": float(price.bid), "ask": float(price.ask)}

        return asyncio.run(_a_tick())

    def get_positions(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = self._require()

        async def _a_positions() -> List[Dict[str, Any]]:
            pos = await conn.get_positions()
            result: List[Dict[str, Any]] = []
            for p in pos:
                if symbol and p.symbol != symbol:
                    continue
                result.append({
                    "id": p.id,
                    "symbol": p.symbol,
                    "type": 0 if p.type == 'POSITION_TYPE_BUY' else 1,
                    "volume": float(p.volume),
                    "price_open": float(p.price),
                    "sl": float(p.sl) if getattr(p, 'sl', None) else None,
                    "tp": float(p.tp) if getattr(p, 'tp', None) else None,
                    "profit": float(getattr(p, 'unrealizedProfit', 0.0)),
                    "magic": int(getattr(p, 'magic', 0) or 0),
                })
            return result

        return asyncio.run(_a_positions())

    # --- trading ---
    def place_market_order(
        self,
        symbol: str,
        side: str,
        volume: float,
        sl_points: Optional[int] = None,
        tp_points: Optional[int] = None,
        deviation: int = 20,  # unused in MetaApi
        magic: int = 234000,
        comment: str = "ai-bot",
    ) -> Any:
        conn = self._require()
        side_u = side.upper()
        if side_u not in ("BUY", "SELL"):
            raise ValueError("side must be BUY or SELL")

        async def _a_order() -> Any:
            # MetaApi uses price offsets in terms of absolute price or sl/tp as price
            # We'll convert points to price by using current tick and broker's pip scale
            price = await conn.get_symbol_price(symbol)
            tick_size = getattr(price, 'tickSize', None) or 0.00001  # heuristic fallback
            bid, ask = float(price.bid), float(price.ask)

            sl = None
            tp = None
            if sl_points and sl_points > 0:
                delta = sl_points * tick_size
                sl = (ask - delta) if side_u == 'BUY' else (bid + delta)
            if tp_points and tp_points > 0:
                delta = tp_points * tick_size
                tp = (ask + delta) if side_u == 'BUY' else (bid - delta)

            if side_u == 'BUY':
                return await conn.create_market_buy_order(symbol, volume, sl=sl, tp=tp, comment=comment, client_id=str(magic))
            else:
                return await conn.create_market_sell_order(symbol, volume, sl=sl, tp=tp, comment=comment, client_id=str(magic))

        return asyncio.run(_a_order())
