"""
Configuration file for the Trading Bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MT5 Configuration
    MT5_LOGIN = int(os.getenv('MT5_LOGIN', '0'))
    MT5_PASSWORD = os.getenv('MT5_PASSWORD', '')
    MT5_SERVER = os.getenv('MT5_SERVER', '')
    MT5_PATH = os.getenv('MT5_PATH', 'C:\\Program Files\\MetaTrader 5\\terminal64.exe')
    
    # Trading Configuration
    SYMBOL = os.getenv('SYMBOL', 'EURUSD')
    TIMEFRAME = os.getenv('TIMEFRAME', 'M15')
    LOT_SIZE = float(os.getenv('LOT_SIZE', '0.01'))
    MAX_POSITIONS = int(os.getenv('MAX_POSITIONS', '3'))
    STOP_LOSS_PIPS = int(os.getenv('STOP_LOSS_PIPS', '50'))
    TAKE_PROFIT_PIPS = int(os.getenv('TAKE_PROFIT_PIPS', '100'))
    
    # AI Configuration
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/')
    RETRAIN_INTERVAL = int(os.getenv('RETRAIN_INTERVAL', '24'))  # hours
    
    # Risk Management
    MAX_DAILY_LOSS = float(os.getenv('MAX_DAILY_LOSS', '100.0'))
    MAX_DAILY_PROFIT = float(os.getenv('MAX_DAILY_PROFIT', '500.0'))
    
    # Mobile Interface
    MOBILE_PORT = int(os.getenv('MOBILE_PORT', '5000'))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'