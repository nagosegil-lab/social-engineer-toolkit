"""
Trading Bot Configuration
Configure your MT5 account and trading parameters here
"""

# MT5 Configuration
MT5_CONFIG = {
    'login': 0,  # Your MT5 account number
    'password': '',  # Your MT5 password
    'server': '',  # Your broker's server (e.g., 'MetaQuotes-Demo')
    'timeout': 60000,
    'portable': False
}

# Trading Parameters
TRADING_CONFIG = {
    'symbol': 'EURUSD',
    'lot_size': 0.01,
    'max_positions': 3,
    'stop_loss_pips': 50,
    'take_profit_pips': 100,
    'trailing_stop': True,
    'trailing_stop_pips': 30,
    'risk_per_trade': 0.02,  # 2% of account balance
}

# AI Model Configuration
AI_CONFIG = {
    'model_type': 'lstm',  # or 'random_forest', 'gradient_boosting'
    'lookback_period': 60,  # number of candles to analyze
    'prediction_threshold': 0.6,  # confidence threshold for trades
    'retrain_interval': 24,  # hours between model retraining
    'features': [
        'close', 'high', 'low', 'open', 'volume',
        'rsi', 'macd', 'bollinger_bands', 'ema', 'sma'
    ]
}

# Mobile API Configuration
API_CONFIG = {
    'host': '0.0.0.0',  # Listen on all interfaces
    'port': 5000,
    'secret_key': 'change-this-to-a-random-secret-key',
    'enable_cors': True,
    'auth_token': 'your-secure-token-here'  # Change this!
}

# Risk Management
RISK_CONFIG = {
    'max_daily_loss': 0.05,  # 5% max daily loss
    'max_drawdown': 0.15,  # 15% max drawdown
    'daily_profit_target': 0.03,  # 3% daily profit target
    'enable_trading_hours': True,
    'trading_hours': {
        'start': '08:00',
        'end': '22:00',
        'timezone': 'UTC'
    }
}

# Notification Settings
NOTIFICATION_CONFIG = {
    'enable_notifications': True,
    'telegram_bot_token': '',  # Optional: Telegram bot token
    'telegram_chat_id': '',  # Optional: Your Telegram chat ID
    'email_notifications': False,
    'email_settings': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'sender_email': '',
        'sender_password': '',
        'recipient_email': ''
    }
}
