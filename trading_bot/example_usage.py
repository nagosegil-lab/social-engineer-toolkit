#!/usr/bin/env python3
"""
Example usage of the Trading Bot
This script demonstrates how to use the bot programmatically
"""
import time
import logging
from trading_bot import TradingBot
from config import Config

def example_basic_usage():
    """Basic usage example"""
    print("🤖 Basic Trading Bot Usage Example")
    print("=" * 40)
    
    # Initialize bot
    bot = TradingBot()
    
    try:
        # Connect to MT5
        print("Connecting to MT5...")
        if not bot.mt5.connect():
            print("❌ Failed to connect to MT5")
            return
        
        print("✅ Connected to MT5")
        
        # Get account info
        account_info = bot.mt5.get_account_info()
        if account_info:
            print(f"💰 Account Balance: ${account_info['balance']:.2f}")
            print(f"💎 Equity: ${account_info['equity']:.2f}")
        
        # Get current price
        price = bot.mt5.get_current_price(Config.SYMBOL)
        if price:
            print(f"📊 Current {Config.SYMBOL} Price: {price['bid']:.5f}")
        
        # Get historical data
        print("📈 Getting historical data...")
        df = bot.mt5.get_historical_data(Config.SYMBOL, Config.TIMEFRAME, 100)
        if df is not None:
            print(f"✅ Got {len(df)} data points")
            print(f"📅 Date range: {df.index[0]} to {df.index[-1]}")
        
        # AI Analysis
        print("🧠 Running AI analysis...")
        if bot.ai.load_model():
            prediction = bot.ai.predict(df)
            if prediction:
                print(f"🎯 AI Prediction: {prediction['prediction']}")
                print(f"🎯 Confidence: {prediction['confidence']:.2f}")
        
        # Market sentiment
        sentiment = bot.ai.get_market_sentiment(df)
        if sentiment:
            print(f"📊 Market Sentiment: {sentiment['overall_sentiment']}")
            print(f"📊 RSI: {sentiment['rsi']['value']:.2f} ({sentiment['rsi']['sentiment']})")
        
        # Get positions
        positions = bot.mt5.get_positions()
        print(f"📋 Open Positions: {len(positions)}")
        
        for pos in positions:
            print(f"  - {pos['symbol']}: {pos['type']} {pos['volume']} lots, P&L: ${pos['profit']:.2f}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Disconnect
        bot.mt5.disconnect()
        print("👋 Disconnected from MT5")

def example_ai_training():
    """AI training example"""
    print("\n🧠 AI Training Example")
    print("=" * 40)
    
    bot = TradingBot()
    
    try:
        # Connect to MT5
        if not bot.mt5.connect():
            print("❌ Failed to connect to MT5")
            return
        
        # Get historical data for training
        print("📊 Getting historical data for training...")
        df = bot.mt5.get_historical_data(Config.SYMBOL, Config.TIMEFRAME, 2000)
        
        if df is None:
            print("❌ Failed to get historical data")
            return
        
        print(f"✅ Got {len(df)} data points for training")
        
        # Train AI model
        print("🤖 Training AI model...")
        if bot.ai.train_model(df):
            print("✅ AI model trained successfully")
        else:
            print("❌ Failed to train AI model")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        bot.mt5.disconnect()

def example_risk_management():
    """Risk management example"""
    print("\n🛡️ Risk Management Example")
    print("=" * 40)
    
    bot = TradingBot()
    
    try:
        # Connect to MT5
        if not bot.mt5.connect():
            print("❌ Failed to connect to MT5")
            return
        
        account_info = bot.mt5.get_account_info()
        positions = bot.mt5.get_positions()
        
        if account_info:
            print(f"💰 Account Balance: ${account_info['balance']:.2f}")
            
            # Check if we can open a position
            can_trade, reason = bot.risk_manager.can_open_position(
                account_info['balance'], positions, Config.SYMBOL
            )
            
            print(f"🔍 Can open position: {can_trade}")
            if not can_trade:
                print(f"❌ Reason: {reason}")
            else:
                # Calculate position size
                position_size = bot.risk_manager.calculate_position_size(
                    account_info['balance']
                )
                print(f"📊 Recommended position size: {position_size:.2f} lots")
                
                # Calculate stop loss and take profit
                current_price = bot.mt5.get_current_price(Config.SYMBOL)
                if current_price:
                    stop_loss = bot.risk_manager.calculate_stop_loss(
                        current_price['bid'], 0  # 0 = buy order
                    )
                    take_profit = bot.risk_manager.calculate_take_profit(
                        current_price['bid'], 0, stop_loss
                    )
                    
                    print(f"🛑 Stop Loss: {stop_loss:.5f}")
                    print(f"🎯 Take Profit: {take_profit:.5f}")
        
        # Risk summary
        risk_summary = bot.risk_manager.get_risk_summary()
        print(f"\n📊 Risk Summary:")
        print(f"  Daily P&L: ${risk_summary['daily_pnl']:.2f}")
        print(f"  Daily Trades: {risk_summary['daily_trades']}")
        print(f"  Risk Status: {risk_summary['risk_status']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        bot.mt5.disconnect()

def main():
    """Main example function"""
    print("🚀 Trading Bot Examples")
    print("=" * 50)
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Run examples
    example_basic_usage()
    example_ai_training()
    example_risk_management()
    
    print("\n✅ Examples completed!")
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()