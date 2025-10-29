"""
Configuration settings for Mobile Trading Bot
הגדרות תצורה לבוט מסחר נייד
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # MT5 Settings
    MT5_LOGIN: Optional[int] = None
    MT5_PASSWORD: Optional[str] = None
    MT5_SERVER: Optional[str] = None
    MT5_PATH: Optional[str] = None  # Path to MT5 terminal
    
    # AI/ML Settings
    AI_MODEL_PATH: str = str(Path(__file__).parent.parent / "models")
    USE_AI: bool = True
    AI_CONFIDENCE_THRESHOLD: float = 0.7
    
    # Trading Settings
    DEFAULT_LOT_SIZE: float = 0.01
    MAX_LOT_SIZE: float = 1.0
    STOP_LOSS_PIPS: int = 50
    TAKE_PROFIT_PIPS: int = 100
    RISK_PERCENTAGE: float = 1.0  # 1% risk per trade
    
    # Database
    DATABASE_URL: str = "sqlite:///./trading_bot.db"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-secret-key-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
