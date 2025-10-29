#!/usr/bin/env python3
"""
Trading Bot Setup and Configuration Script
"""
import os
import sys
from pathlib import Path

def create_env_file():
    """Create environment configuration file"""
    env_content = """# Trading Bot Configuration
# Copy this file to .env and update with your settings

# MetaTrader 5 Configuration
MT5_SERVER=demo-server
MT5_LOGIN=your_login_number
MT5_PASSWORD=your_password
MT5_TIMEOUT=60000

# AI Configuration
AI_MODEL_TYPE=lstm
AI_LOOKBACK_PERIOD=60
AI_PREDICTION_HORIZON=5
AI_CONFIDENCE_THRESHOLD=0.7
AI_RETRAIN_INTERVAL=24

# Risk Management
MAX_RISK_PER_TRADE=0.02
MAX_DAILY_LOSS=0.05
MAX_OPEN_POSITIONS=5
STOP_LOSS_PIPS=50
TAKE_PROFIT_PIPS=100

# Trading Configuration
TRADING_SYMBOLS=EURUSD,GBPUSD,USDJPY,AUDUSD
MIN_SPREAD=2.0
MAX_SLIPPAGE=3

# Web Interface
WEB_HOST=0.0.0.0
WEB_PORT=8080
WEB_DEBUG=False
SECRET_KEY=change-this-secret-key-in-production

# Database
DATABASE_URL=sqlite:///trading_bot.db
DATABASE_ECHO=False

# Telegram Notifications
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Email Notifications
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_TO=alerts@yourdomain.com

# Logging
LOG_LEVEL=INFO
LOG_FILE=trading_bot.log
LOG_MAX_BYTES=10485760
LOG_BACKUP_COUNT=5
"""
    
    env_file = Path('.env.example')
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Created {env_file}")
    print("📝 Copy this file to .env and update with your settings")

def create_directories():
    """Create necessary directories"""
    directories = [
        'trading_bot/ai/saved_models',
        'trading_bot/web/templates',
        'trading_bot/web/static',
        'logs',
        'data',
        'backtest_results'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def create_startup_scripts():
    """Create startup scripts for different platforms"""
    
    # Linux/Mac startup script
    linux_script = """#!/bin/bash
# Trading Bot Startup Script for Linux/Mac

echo "🤖 Starting Mobile Trading Bot..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

# Install requirements
echo "📦 Installing requirements..."
pip3 install -r requirements_trading.txt

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Please copy .env.example to .env and configure it."
    echo "📝 cp .env.example .env"
    exit 1
fi

# Start the bot
echo "🚀 Starting Trading Bot..."
python3 main.py
"""
    
    with open('start_bot.sh', 'w') as f:
        f.write(linux_script)
    
    # Make it executable
    os.chmod('start_bot.sh', 0o755)
    
    # Windows startup script
    windows_script = """@echo off
REM Trading Bot Startup Script for Windows

echo 🤖 Starting Mobile Trading Bot...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Install requirements
echo 📦 Installing requirements...
pip install -r requirements_trading.txt

REM Check if .env file exists
if not exist .env (
    echo ⚠️  .env file not found. Please copy .env.example to .env and configure it.
    echo 📝 copy .env.example .env
    pause
    exit /b 1
)

REM Start the bot
echo 🚀 Starting Trading Bot...
python main.py

pause
"""
    
    with open('start_bot.bat', 'w') as f:
        f.write(windows_script)
    
    print("✅ Created startup scripts:")
    print("   • start_bot.sh (Linux/Mac)")
    print("   • start_bot.bat (Windows)")

def create_docker_files():
    """Create Docker configuration files"""
    
    dockerfile = """FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements_trading.txt .
RUN pip install --no-cache-dir -r requirements_trading.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p trading_bot/ai/saved_models logs data backtest_results

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "main.py"]
"""
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile)
    
    docker_compose = """version: '3.8'

services:
  trading-bot:
    build: .
    ports:
      - "8080:8080"
    environment:
      - WEB_HOST=0.0.0.0
      - WEB_PORT=8080
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
      - ./trading_bot/ai/saved_models:/app/trading_bot/ai/saved_models
    restart: unless-stopped
    
  # Optional: Add a database service
  # postgres:
  #   image: postgres:13
  #   environment:
  #     POSTGRES_DB: trading_bot
  #     POSTGRES_USER: trader
  #     POSTGRES_PASSWORD: your_password
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data
  #   ports:
  #     - "5432:5432"

# volumes:
#   postgres_data:
"""
    
    with open('docker-compose.yml', 'w') as f:
        f.write(docker_compose)
    
    print("✅ Created Docker files:")
    print("   • Dockerfile")
    print("   • docker-compose.yml")

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("🔧 MOBILE TRADING BOT SETUP")
    print("="*60)
    
    try:
        print("\n📁 Creating directories...")
        create_directories()
        
        print("\n⚙️  Creating configuration files...")
        create_env_file()
        
        print("\n🚀 Creating startup scripts...")
        create_startup_scripts()
        
        print("\n🐳 Creating Docker files...")
        create_docker_files()
        
        print("\n" + "="*60)
        print("✅ SETUP COMPLETE!")
        print("="*60)
        print("📋 Next Steps:")
        print("1. Copy .env.example to .env")
        print("2. Configure your MT5 credentials in .env")
        print("3. Set up Telegram bot token in .env")
        print("4. Configure email settings in .env")
        print("5. Run: ./start_bot.sh (Linux/Mac) or start_bot.bat (Windows)")
        print("   Or use Docker: docker-compose up")
        print("\n⚠️  IMPORTANT:")
        print("• Test with demo accounts first!")
        print("• Change the default password!")
        print("• This is for educational purposes only!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()