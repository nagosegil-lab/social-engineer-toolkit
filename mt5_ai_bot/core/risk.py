from __future__ import annotations

import datetime as dt
import json
import os
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class BotState:
    date: str
    trades_today: int
    realized_pnl_today: float
    last_executed_bar_iso: str | None

    @staticmethod
    def default(today: dt.date) -> "BotState":
        return BotState(date=today.isoformat(), trades_today=0, realized_pnl_today=0.0, last_executed_bar_iso=None)


class StateStore:
    def __init__(self, path: str) -> None:
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def load(self) -> BotState:
        today = dt.date.today()
        if not os.path.exists(self.path):
            return BotState.default(today)
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            state = BotState(**data)
        except Exception:
            return BotState.default(today)

        # daily reset
        if state.date != today.isoformat():
            return BotState.default(today)
        return state

    def save(self, state: BotState) -> None:
        tmp_path = self.path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(asdict(state), f)
        os.replace(tmp_path, self.path)


@dataclass
class RiskConfig:
    max_trades_per_day: int = 20
    max_daily_loss: float = 0.0  # in account currency; 0 = disabled
    max_exposure_lots: float = 0.0  # 0 = disabled


class RiskManager:
    def __init__(self, cfg: RiskConfig, state_store: StateStore) -> None:
        self.cfg = cfg
        self.state_store = state_store

    def can_trade(self, state: BotState, current_exposure_lots: float) -> tuple[bool, str]:
        if self.cfg.max_trades_per_day and state.trades_today >= self.cfg.max_trades_per_day:
            return False, "max_trades_per_day_reached"
        if self.cfg.max_daily_loss and state.realized_pnl_today <= -abs(self.cfg.max_daily_loss):
            return False, "max_daily_loss_reached"
        if self.cfg.max_exposure_lots and abs(current_exposure_lots) >= abs(self.cfg.max_exposure_lots):
            return False, "max_exposure_reached"
        return True, "ok"

    def on_order_filled(self, state: BotState, realized_pnl_change: float = 0.0) -> BotState:
        state.trades_today += 1
        state.realized_pnl_today += realized_pnl_change
        self.state_store.save(state)
        return state
