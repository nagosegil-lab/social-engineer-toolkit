#!/usr/bin/env python3
"""
Demo script for Trading Bot
Shows the bot capabilities without requiring MT5 connection
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.utils
import json

def generate_demo_data():
    """Generate demo trading data"""
    print("📊 Generating demo data...")
    
    # Generate 1000 data points
    dates = pd.date_range(start='2024-01-01', periods=1000, freq='15min')
    
    # Generate realistic price data with trend and volatility
    np.random.seed(42)
    base_price = 1.1000
    trend = np.linspace(0, 0.05, 1000)  # Upward trend
    noise = np.random.normal(0, 0.001, 1000)  # Random noise
    
    prices = base_price + trend + noise
    
    # Create OHLC data
    data = []
    for i, (date, price) in enumerate(zip(dates, prices)):
        # Generate realistic OHLC from base price
        volatility = np.random.uniform(0.0001, 0.0005)
        high = price + volatility * np.random.uniform(0.5, 1.0)
        low = price - volatility * np.random.uniform(0.5, 1.0)
        open_price = price + np.random.uniform(-volatility/2, volatility/2)
        close_price = price + np.random.uniform(-volatility/2, volatility/2)
        volume = np.random.randint(100, 1000)
        
        data.append({
            'time': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close_price,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('time', inplace=True)
    
    print(f"✅ Generated {len(df)} data points")
    return df

def create_demo_chart(df):
    """Create demo chart"""
    print("📈 Creating demo chart...")
    
    # Create candlestick chart
    candlestick = go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='EUR/USD'
    )
    
    # Add moving averages
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    
    sma20 = go.Scatter(
        x=df.index,
        y=df['sma_20'],
        name='SMA 20',
        line=dict(color='orange', width=1)
    )
    
    sma50 = go.Scatter(
        x=df.index,
        y=df['sma_50'],
        name='SMA 50',
        line=dict(color='blue', width=1)
    )
    
    # Create layout
    layout = go.Layout(
        title='EUR/USD - 15 Minute Chart (Demo)',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Price'),
        template='plotly_dark',
        height=400
    )
    
    # Create figure
    fig = go.Figure(data=[candlestick, sma20, sma50], layout=layout)
    
    return fig

def demo_technical_analysis(df):
    """Demo technical analysis"""
    print("🔍 Running technical analysis...")
    
    # Calculate technical indicators
    df['rsi'] = calculate_rsi(df['close'], 14)
    df['macd'] = calculate_macd(df['close'])
    df['bb_upper'] = calculate_bollinger_upper(df['close'], 20)
    df['bb_lower'] = calculate_bollinger_lower(df['close'], 20)
    
    # Get latest values
    latest = df.iloc[-1]
    
    analysis = {
        'rsi': {
            'value': latest['rsi'],
            'signal': 'overbought' if latest['rsi'] > 70 else 'oversold' if latest['rsi'] < 30 else 'neutral'
        },
        'macd': {
            'value': latest['macd'],
            'signal': 'bullish' if latest['macd'] > 0 else 'bearish'
        },
        'bollinger': {
            'position': 'above' if latest['close'] > latest['bb_upper'] else 'below' if latest['close'] < latest['bb_lower'] else 'middle'
        },
        'trend': {
            'sma_signal': 'bullish' if latest['sma_20'] > latest['sma_50'] else 'bearish'
        }
    }
    
    return analysis

def calculate_rsi(prices, window=14):
    """Calculate RSI"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD"""
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    macd = ema_fast - ema_slow
    return macd

def calculate_bollinger_upper(prices, window=20, std_dev=2):
    """Calculate Bollinger Bands upper"""
    sma = prices.rolling(window=window).mean()
    std = prices.rolling(window=window).std()
    return sma + (std * std_dev)

def calculate_bollinger_lower(prices, window=20, std_dev=2):
    """Calculate Bollinger Bands lower"""
    sma = prices.rolling(window=window).mean()
    std = prices.rolling(window=window).std()
    return sma - (std * std_dev)

def demo_ai_prediction(df):
    """Demo AI prediction"""
    print("🤖 Running AI prediction...")
    
    # Simulate AI prediction
    np.random.seed(42)
    prediction = np.random.choice([-1, 0, 1], p=[0.3, 0.4, 0.3])
    confidence = np.random.uniform(0.6, 0.9)
    
    prediction_text = {
        -1: 'Sell',
        0: 'Hold',
        1: 'Buy'
    }
    
    return {
        'prediction': prediction,
        'prediction_text': prediction_text[prediction],
        'confidence': confidence
    }

def main():
    """Main demo function"""
    print("🚀 Trading Bot Demo")
    print("=" * 30)
    print("This demo shows the bot capabilities without requiring MT5 connection")
    print()
    
    # Generate demo data
    df = generate_demo_data()
    
    # Create chart
    fig = create_demo_chart(df)
    
    # Technical analysis
    analysis = demo_technical_analysis(df)
    
    # AI prediction
    prediction = demo_ai_prediction(df)
    
    # Display results
    print("\n📊 Demo Results:")
    print(f"📈 Data Points: {len(df)}")
    print(f"📅 Date Range: {df.index[0]} to {df.index[-1]}")
    print(f"💰 Price Range: {df['close'].min():.5f} - {df['close'].max():.5f}")
    
    print("\n🔍 Technical Analysis:")
    print(f"📊 RSI: {analysis['rsi']['value']:.2f} ({analysis['rsi']['signal']})")
    print(f"📊 MACD: {analysis['macd']['value']:.6f} ({analysis['macd']['signal']})")
    print(f"📊 Bollinger: {analysis['bollinger']['position']}")
    print(f"📊 Trend: {analysis['trend']['sma_signal']}")
    
    print("\n🤖 AI Prediction:")
    print(f"🎯 Signal: {prediction['prediction_text']}")
    print(f"🎯 Confidence: {prediction['confidence']:.2f}")
    
    print("\n📈 Chart created successfully!")
    print("💡 To see the interactive chart, run the mobile interface:")
    print("   python start_bot.py")
    
    # Save chart data for mobile interface
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    with open('demo_chart.json', 'w') as f:
        f.write(chart_json)
    
    print("\n✅ Demo completed! Chart data saved to demo_chart.json")

if __name__ == "__main__":
    main()