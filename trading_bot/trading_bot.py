"""
Main Trading Bot Class
"""
import logging
import time
import schedule
from datetime import datetime, timedelta
import pandas as pd
from mt5_connector import MT5Connector
from ai_analyzer import AIAnalyzer
from risk_manager import RiskManager
from config import Config

class TradingBot:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.mt5 = MT5Connector()
        self.ai = AIAnalyzer()
        self.risk_manager = RiskManager()
        self.running = False
        self.last_analysis_time = None
        
        # Setup logging
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('trading_bot.log'),
                logging.StreamHandler()
            ]
        )
    
    def start(self):
        """Start the trading bot"""
        try:
            self.logger.info("Starting Trading Bot...")
            
            # Connect to MT5
            if not self.mt5.connect():
                self.logger.error("Failed to connect to MT5")
                return False
            
            # Load AI model
            if not self.ai.load_model():
                self.logger.warning("No trained model found, will train with historical data")
                self.train_ai_model()
            
            # Setup trading schedule
            self.setup_schedule()
            
            self.running = True
            self.logger.info("Trading Bot started successfully")
            
            # Run initial analysis
            self.analyze_and_trade()
            
            # Keep running
            while self.running:
                schedule.run_pending()
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.logger.info("Bot stopped by user")
            self.stop()
        except Exception as e:
            self.logger.error(f"Error in trading bot: {e}")
            self.stop()
    
    def stop(self):
        """Stop the trading bot"""
        self.running = False
        self.mt5.disconnect()
        self.logger.info("Trading Bot stopped")
    
    def setup_schedule(self):
        """Setup trading schedule"""
        # Analyze market every 15 minutes
        schedule.every(15).minutes.do(self.analyze_and_trade)
        
        # Retrain AI model daily at 2 AM
        schedule.every().day.at("02:00").do(self.retrain_ai_model)
        
        # Daily risk reset
        schedule.every().day.at("00:00").do(self.risk_manager.reset_daily_stats)
        
        self.logger.info("Trading schedule setup complete")
    
    def train_ai_model(self):
        """Train AI model with historical data"""
        try:
            self.logger.info("Training AI model...")
            
            # Get historical data
            df = self.mt5.get_historical_data(Config.SYMBOL, Config.TIMEFRAME, 2000)
            if df is None:
                self.logger.error("Failed to get historical data for training")
                return False
            
            # Train model
            if self.ai.train_model(df):
                self.logger.info("AI model trained successfully")
                return True
            else:
                self.logger.error("Failed to train AI model")
                return False
                
        except Exception as e:
            self.logger.error(f"Error training AI model: {e}")
            return False
    
    def retrain_ai_model(self):
        """Retrain AI model with latest data"""
        try:
            self.logger.info("Retraining AI model...")
            self.train_ai_model()
        except Exception as e:
            self.logger.error(f"Error retraining AI model: {e}")
    
    def analyze_and_trade(self):
        """Main trading analysis and execution"""
        try:
            self.logger.info("Starting market analysis...")
            
            # Get current account info
            account_info = self.mt5.get_account_info()
            if not account_info:
                self.logger.error("Failed to get account info")
                return
            
            # Get current positions
            positions = self.mt5.get_positions()
            
            # Get historical data for analysis
            df = self.mt5.get_historical_data(Config.SYMBOL, Config.TIMEFRAME, 500)
            if df is None:
                self.logger.error("Failed to get historical data")
                return
            
            # AI prediction
            prediction = self.ai.predict(df)
            if not prediction:
                self.logger.warning("No AI prediction available")
                return
            
            # Market sentiment analysis
            sentiment = self.ai.get_market_sentiment(df)
            if not sentiment:
                self.logger.warning("No market sentiment analysis available")
                return
            
            self.logger.info(f"AI Prediction: {prediction['prediction']} (Confidence: {prediction['confidence']:.2f})")
            self.logger.info(f"Market Sentiment: {sentiment['overall_sentiment']}")
            
            # Check existing positions
            self.manage_existing_positions(positions, df)
            
            # Make new trading decisions
            if prediction['prediction'] != 0 and prediction['confidence'] > 0.6:
                self.execute_trade_decision(prediction, account_info, positions, df)
            
            self.last_analysis_time = datetime.now()
            
        except Exception as e:
            self.logger.error(f"Error in analyze_and_trade: {e}")
    
    def manage_existing_positions(self, positions, df):
        """Manage existing positions"""
        try:
            current_price = self.mt5.get_current_price(Config.SYMBOL)
            if not current_price:
                return
            
            for position in positions:
                if position['symbol'] == Config.SYMBOL:
                    # Check if position should be closed
                    should_close, reason = self.risk_manager.should_close_position(
                        position, current_price['bid']
                    )
                    
                    if should_close:
                        self.logger.info(f"Closing position {position['ticket']}: {reason}")
                        self.mt5.close_position(position['ticket'])
                        
                        # Update daily P&L
                        pnl = position['profit']
                        self.risk_manager.update_daily_pnl(pnl)
                    
        except Exception as e:
            self.logger.error(f"Error managing existing positions: {e}")
    
    def execute_trade_decision(self, prediction, account_info, positions, df):
        """Execute trading decision based on AI prediction"""
        try:
            symbol = Config.SYMBOL
            current_price = self.mt5.get_current_price(symbol)
            if not current_price:
                return
            
            # Check if we can open a position
            can_trade, reason = self.risk_manager.can_open_position(
                account_info['balance'], positions, symbol
            )
            
            if not can_trade:
                self.logger.warning(f"Cannot open position: {reason}")
                return
            
            # Determine order type
            if prediction['prediction'] == 1:  # Buy signal
                order_type = 0  # Buy order
                price = current_price['ask']
            elif prediction['prediction'] == -1:  # Sell signal
                order_type = 1  # Sell order
                price = current_price['bid']
            else:
                return
            
            # Calculate position size
            position_size = self.risk_manager.calculate_position_size(
                account_info['balance']
            )
            
            # Calculate stop loss and take profit
            atr = df['atr'].iloc[-1] if 'atr' in df.columns else None
            stop_loss = self.risk_manager.calculate_stop_loss(price, order_type, atr)
            take_profit = self.risk_manager.calculate_take_profit(price, order_type, stop_loss)
            
            # Place order
            result = self.mt5.place_order(
                symbol=symbol,
                order_type=order_type,
                volume=position_size,
                price=price,
                sl=stop_loss,
                tp=take_profit,
                comment=f"AI Bot - Confidence: {prediction['confidence']:.2f}"
            )
            
            if result:
                self.logger.info(f"Order placed successfully: {result.order}")
                self.risk_manager.update_daily_trades()
            else:
                self.logger.error("Failed to place order")
                
        except Exception as e:
            self.logger.error(f"Error executing trade decision: {e}")
    
    def get_bot_status(self):
        """Get current bot status"""
        try:
            account_info = self.mt5.get_account_info()
            positions = self.mt5.get_positions()
            risk_summary = self.risk_manager.get_risk_summary()
            
            return {
                'running': self.running,
                'last_analysis': self.last_analysis_time.isoformat() if self.last_analysis_time else None,
                'account': account_info,
                'positions': positions,
                'risk': risk_summary,
                'symbol': Config.SYMBOL,
                'timeframe': Config.TIMEFRAME
            }
            
        except Exception as e:
            self.logger.error(f"Error getting bot status: {e}")
            return None
    
    def get_performance_stats(self):
        """Get trading performance statistics"""
        try:
            # This would typically query a database for historical performance
            # For now, return basic stats
            positions = self.mt5.get_positions()
            
            total_positions = len(positions)
            profitable_positions = sum(1 for pos in positions if pos['profit'] > 0)
            total_profit = sum(pos['profit'] for pos in positions)
            
            win_rate = (profitable_positions / total_positions * 100) if total_positions > 0 else 0
            
            return {
                'total_positions': total_positions,
                'profitable_positions': profitable_positions,
                'win_rate': win_rate,
                'total_profit': total_profit,
                'average_profit': total_profit / total_positions if total_positions > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error getting performance stats: {e}")
            return None