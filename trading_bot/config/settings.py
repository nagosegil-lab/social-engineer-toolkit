"""
Trading Bot Configuration Settings
"""
import os
from typing import Dict, Any

# MT5 Configuration
MT5_CONFIG = {
    'server': os.getenv('MT5_SERVER', 'demo-server'),
    'login': int(os.getenv('MT5_LOGIN', '0')),
    'password': os.getenv('MT5_PASSWORD', ''),
    'timeout': int(os.getenv('MT5_TIMEOUT', '60000')),
    'portable': False
}

# AI Configuration
AI_CONFIG = {
    'model_type': os.getenv('AI_MODEL_TYPE', 'lstm'),
    'lookback_period': int(os.getenv('AI_LOOKBACK_PERIOD', '60')),
    'prediction_horizon': int(os.getenv('AI_PREDICTION_HORIZON', '5')),
    'confidence_threshold': float(os.getenv('AI_CONFIDENCE_THRESHOLD', '0.7')),
    'retrain_interval': int(os.getenv('AI_RETRAIN_INTERVAL', '24'))  # hours
}

# Risk Management
RISK_CONFIG = {
    'max_risk_per_trade': float(os.getenv('MAX_RISK_PER_TRADE', '0.02')),  # 2%
    'max_daily_loss': float(os.getenv('MAX_DAILY_LOSS', '0.05')),  # 5%
    'max_open_positions': int(os.getenv('MAX_OPEN_POSITIONS', '5')),
    'stop_loss_pips': int(os.getenv('STOP_LOSS_PIPS', '50')),
    'take_profit_pips': int(os.getenv('TAKE_PROFIT_PIPS', '100'))
}

# Trading Configuration
TRADING_CONFIG = {
    'symbols': os.getenv('TRADING_SYMBOLS', 'EURUSD,GBPUSD,USDJPY,AUDUSD').split(','),
    'timeframes': ['M1', 'M5', 'M15', 'H1', 'H4', 'D1'],
    'min_spread': float(os.getenv('MIN_SPREAD', '2.0')),
    'max_slippage': int(os.getenv('MAX_SLIPPAGE', '3'))
}

# Web Interface Configuration
WEB_CONFIG = {
    'host': os.getenv('WEB_HOST', '0.0.0.0'),
    'port': int(os.getenv('WEB_PORT', '8080')),
    'debug': os.getenv('WEB_DEBUG', 'False').lower() == 'true',
    'secret_key': os.getenv('SECRET_KEY', 'your-secret-key-here')
}

# Database Configuration
DATABASE_CONFIG = {
    'url': os.getenv('DATABASE_URL', 'sqlite:///trading_bot.db'),
    'echo': os.getenv('DATABASE_ECHO', 'False').lower() == 'true'
}

# Notification Configuration
NOTIFICATION_CONFIG = {
    'telegram_token': os.getenv('TELEGRAM_TOKEN', ''),
    'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID', ''),
    'email_smtp_server': os.getenv('EMAIL_SMTP_SERVER', ''),
    'email_port': int(os.getenv('EMAIL_PORT', '587')),
    'email_username': os.getenv('EMAIL_USERNAME', ''),
    'email_password': os.getenv('EMAIL_PASSWORD', ''),
    'email_to': os.getenv('EMAIL_TO', '')
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': os.getenv('LOG_FILE', 'trading_bot.log'),
    'max_bytes': int(os.getenv('LOG_MAX_BYTES', '10485760')),  # 10MB
    'backup_count': int(os.getenv('LOG_BACKUP_COUNT', '5'))
}