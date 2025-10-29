#!/bin/bash
# Complete installation and run script for Trading Bot

echo "🤖 Trading Bot MT5 + AI - Complete Setup"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv trading_bot_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source trading_bot_env/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing requirements..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your MT5 credentials before running the bot."
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p models logs static/css static/js templates

echo ""
echo "🎉 Installation completed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your MT5 credentials"
echo "2. Run: python start_bot.py"
echo "3. Open browser: http://localhost:5000"
echo ""
echo "🚀 Starting the bot now..."

# Start the bot
python start_bot.py