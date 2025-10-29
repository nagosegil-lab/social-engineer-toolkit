#!/bin/bash
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
