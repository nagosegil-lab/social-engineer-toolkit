@echo off
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
