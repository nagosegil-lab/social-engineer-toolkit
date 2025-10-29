import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    connector: str = os.getenv("CONNECTOR", "mt5")  # mt5 | metaapi
    symbol: str = os.getenv("SYMBOL", "EURUSD")
    timeframe: str = os.getenv("TIMEFRAME", "M5")

    # Order sizing and risk config
    lot: float = float(os.getenv("LOT", "0.10"))
    risk_per_trade: float = float(os.getenv("RISK_PER_TRADE", "0.0"))  # optional

    # Optional SL/TP in points (e.g., 100 = 10 pips on 5-digit pairs)
    sl_points: int | None = int(os.getenv("SL_POINTS", "100")) if os.getenv("SL_POINTS", "") != "" else None
    tp_points: int | None = int(os.getenv("TP_POINTS", "100")) if os.getenv("TP_POINTS", "") != "" else None
    deviation: int = int(os.getenv("SLIPPAGE", "20"))

    # Trading controls
    trade_mode: str = os.getenv("TRADE_MODE", "live")  # live | paper
    max_trades_per_day: int = int(os.getenv("MAX_TRADES_PER_DAY", "20"))
    max_daily_loss: float = float(os.getenv("MAX_DAILY_LOSS", "0.0"))  # 0 disables
    max_exposure_lots: float = float(os.getenv("MAX_EXPOSURE_LOTS", "0.0"))  # 0 disables
    trading_hours: str = os.getenv("TRADING_HOURS", "")  # e.g. "08:00-22:00" (local time)
    timezone: str = os.getenv("TIMEZONE", "UTC")

    # MT5 terminal credentials (VPS/Windows with MT5 installed)
    mt5_login: int = int(os.getenv("MT5_LOGIN", "0") or 0)
    mt5_password: str = os.getenv("MT5_PASSWORD", "")
    mt5_server: str = os.getenv("MT5_SERVER", "")

    # MetaApi Cloud (optional)
    metaapi_token: str = os.getenv("METAAPI_TOKEN", "")
    metaapi_account_id: str = os.getenv("METAAPI_ACCOUNT_ID", "")

    # Notifications
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")

    # Model
    model_path: str = os.getenv(
        "MODEL_PATH",
        os.path.join(os.path.dirname(__file__), "models", "model.joblib"),
    )


def get_settings() -> Settings:
    return Settings()
