FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p models logs

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=mobile_app.py

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "main.py", "--mobile"]