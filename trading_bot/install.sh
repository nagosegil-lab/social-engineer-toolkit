#!/bin/bash

# MT5 AI Trading Bot Installation Script

echo "========================================"
echo "  MT5 AI Trading Bot - Installation"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then 
    echo "❌ Python version must be 3.8 or higher. Found: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python version is compatible"
echo ""

# Create virtual environment (optional but recommended)
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ $? -eq 0 ]; then
    echo "✅ Virtual environment created"
    
    # Activate virtual environment
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        echo "✅ Virtual environment activated"
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
        echo "✅ Virtual environment activated"
    fi
else
    echo "⚠️  Could not create virtual environment. Continuing with system Python..."
fi

echo ""

# Install requirements
echo "📥 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ All packages installed successfully"
else
    echo "❌ Failed to install packages"
    exit 1
fi

echo ""

# Create models directory
echo "📁 Creating directories..."
mkdir -p models
mkdir -p logs

echo "✅ Directories created"
echo ""

# Copy env example
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your MT5 credentials."
else
    echo "⚠️  .env file already exists. Skipping..."
fi

echo ""
echo "========================================"
echo "  Installation Complete! 🎉"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit config.py with your MT5 account details"
echo "2. Run: python main.py"
echo "3. Open your phone browser and go to: http://YOUR_IP:5000"
echo ""
echo "For detailed instructions, see README.md or QUICK_START.md"
echo ""
echo "Happy Trading! 📈💰"
