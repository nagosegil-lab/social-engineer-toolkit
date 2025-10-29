#!/bin/bash
# Script to run the trading bot in mobile mode

echo "🚀 Starting Trading Bot Mobile Interface..."
echo "📱 Open your browser and go to: http://localhost:5000"
echo ""

# Activate virtual environment if it exists
if [ -d "trading_bot_env" ]; then
    echo "Activating virtual environment..."
    source trading_bot_env/bin/activate
fi

# Install requirements if needed
if [ ! -d "venv" ] && [ ! -d "trading_bot_env" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

# Run the mobile app
python main.py --mobile