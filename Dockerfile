FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
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
