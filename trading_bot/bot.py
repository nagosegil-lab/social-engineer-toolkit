"""
Main Trading Bot
Orchestrates MT5 connection, AI predictions, and trade execution
"""

import time
import logging
from datetime import datetime, timedelta
from threading import Thread, Event
from typing import Dict, Optional
import json
import os

from mt5_connector import MT5Connector
from ai_strategy import AITradingStrategy
from config import MT5_CONFIG, TRADING_CONFIG, AI_CONFIG, RISK_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TradingBot:
    def __init__(self):
        self.mt5 = MT5Connector(MT5_CONFIG)
        self.ai_strategy = AITradingStrategy(AI_CONFIG)
        self.is_running = False
        self.stop_event = Event()
        self.trading_thread = None
        self.stats = {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_profit': 0,
            'start_balance': 0,
            'daily_trades': 0,
            'daily_profit': 0,
        }
        self.load_stats()
    
    def initialize(self) -> bool:
        """Initialize bot - connect to MT5 and load AI model"""
        logger.info("Initializing trading bot...")
        
        # Connect to MT5
        if not self.mt5.connect():
            logger.error("Failed to connect to MT5")
            return False
        
        # Get initial balance
        account_info = self.mt5.get_account_info()
        if account_info:
            self.stats['start_balance'] = account_info['balance']
        
        # Try to load existing model
        if not self.ai_strategy.load_model():
            logger.info("No existing model found. Training new model...")
            df = self.mt5.get_historical_data(
                symbol=TRADING_CONFIG['symbol'],
                timeframe='H1',
                bars=5000
            )
            if df is not None:
                self.ai_strategy.train_model(df)
            else:
                logger.error("Failed to get historical data for training")
                return False
        
        logger.info("Bot initialized successfully")
        return True
    
    def start(self):
        """Start the trading bot"""
        if self.is_running:
            logger.warning("Bot is already running")
            return
        
        self.is_running = True
        self.stop_event.clear()
        self.trading_thread = Thread(target=self._trading_loop)
        self.trading_thread.start()
        logger.info("Trading bot started")
    
    def stop(self):
        """Stop the trading bot"""
        if not self.is_running:
            logger.warning("Bot is not running")
            return
        
        self.is_running = False
        self.stop_event.set()
        
        if self.trading_thread:
            self.trading_thread.join(timeout=5)
        
        logger.info("Trading bot stopped")
    
    def _trading_loop(self):
        """Main trading loop"""
        last_retrain = datetime.now()
        
        while self.is_running and not self.stop_event.is_set():
            try:
                # Check if we should trade (trading hours, risk limits, etc.)
                if not self._can_trade():
                    time.sleep(60)
                    continue
                
                # Get market data
                df = self.mt5.get_historical_data(
                    symbol=TRADING_CONFIG['symbol'],
                    timeframe='H1',
                    bars=AI_CONFIG['lookback_period'] + 100
                )
                
                if df is None or len(df) == 0:
                    logger.warning("Failed to get market data")
                    time.sleep(60)
                    continue
                
                # Get AI prediction
                prediction = self.ai_strategy.predict(df)
                
                if prediction is None:
                    time.sleep(60)
                    continue
                
                logger.info(f"Prediction: {prediction['signal']} (confidence: {prediction['confidence']:.2f})")
                
                # Execute trades based on prediction
                if prediction['signal'] in ['BUY', 'SELL']:
                    self._execute_trade(prediction)
                
                # Check open positions and manage them
                self._manage_positions()
                
                # Retrain model periodically
                if (datetime.now() - last_retrain).total_seconds() > AI_CONFIG['retrain_interval'] * 3600:
                    logger.info("Retraining model...")
                    df_train = self.mt5.get_historical_data(
                        symbol=TRADING_CONFIG['symbol'],
                        timeframe='H1',
                        bars=5000
                    )
                    if df_train is not None:
                        self.ai_strategy.train_model(df_train)
                    last_retrain = datetime.now()
                
                # Wait before next iteration
                time.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error(f"Error in trading loop: {e}")
                time.sleep(60)
        
        logger.info("Trading loop ended")
    
    def _can_trade(self) -> bool:
        """Check if we can trade based on various conditions"""
        # Check if connected
        if not self.mt5.connected:
            return False
        
        # Check trading hours
        if RISK_CONFIG['enable_trading_hours']:
            now = datetime.now().time()
            start_time = datetime.strptime(RISK_CONFIG['trading_hours']['start'], '%H:%M').time()
            end_time = datetime.strptime(RISK_CONFIG['trading_hours']['end'], '%H:%M').time()
            
            if not (start_time <= now <= end_time):
                return False
        
        # Check daily loss limit
        if abs(self.stats['daily_profit']) >= self.stats['start_balance'] * RISK_CONFIG['max_daily_loss']:
            if self.stats['daily_profit'] < 0:
                logger.warning("Daily loss limit reached. Stopping trading for today.")
                return False
        
        # Check daily profit target
        if self.stats['daily_profit'] >= self.stats['start_balance'] * RISK_CONFIG['daily_profit_target']:
            logger.info("Daily profit target reached. Stopping trading for today.")
            return False
        
        # Check max positions
        open_positions = self.mt5.get_open_positions()
        if len(open_positions) >= TRADING_CONFIG['max_positions']:
            return False
        
        return True
    
    def _execute_trade(self, prediction: Dict):
        """Execute a trade based on prediction"""
        symbol = TRADING_CONFIG['symbol']
        lot_size = TRADING_CONFIG['lot_size']
        
        # Check if we already have a position in this direction
        open_positions = self.mt5.get_open_positions()
        for pos in open_positions:
            if pos['symbol'] == symbol and pos['type'] == prediction['signal']:
                logger.info(f"Already have a {prediction['signal']} position for {symbol}")
                return
        
        # Calculate stop loss and take profit
        symbol_info = self.mt5.get_symbol_info(symbol)
        if symbol_info is None:
            return
        
        point = symbol_info['point']
        
        if prediction['signal'] == 'BUY':
            price = symbol_info['ask']
            sl = price - TRADING_CONFIG['stop_loss_pips'] * 10 * point
            tp = price + TRADING_CONFIG['take_profit_pips'] * 10 * point
        else:  # SELL
            price = symbol_info['bid']
            sl = price + TRADING_CONFIG['stop_loss_pips'] * 10 * point
            tp = price - TRADING_CONFIG['take_profit_pips'] * 10 * point
        
        # Open position
        ticket = self.mt5.open_position(
            symbol=symbol,
            order_type=prediction['signal'],
            lot_size=lot_size,
            sl=sl,
            tp=tp,
            comment=f"AI Trade (conf: {prediction['confidence']:.2f})"
        )
        
        if ticket:
            self.stats['total_trades'] += 1
            self.stats['daily_trades'] += 1
            self.save_stats()
            logger.info(f"Trade executed: {prediction['signal']} {symbol} at {price}")
    
    def _manage_positions(self):
        """Manage open positions (trailing stop, etc.)"""
        open_positions = self.mt5.get_open_positions()
        
        for pos in open_positions:
            # Update statistics for closed positions
            if pos['profit'] != 0:
                if pos['profit'] > 0:
                    self.stats['winning_trades'] += 1
                else:
                    self.stats['losing_trades'] += 1
                
                self.stats['total_profit'] += pos['profit']
                self.stats['daily_profit'] += pos['profit']
            
            # Implement trailing stop
            if TRADING_CONFIG['trailing_stop']:
                self._apply_trailing_stop(pos)
        
        self.save_stats()
    
    def _apply_trailing_stop(self, position: Dict):
        """Apply trailing stop to a position"""
        symbol_info = self.mt5.get_symbol_info(position['symbol'])
        if symbol_info is None:
            return
        
        point = symbol_info['point']
        trailing_pips = TRADING_CONFIG['trailing_stop_pips']
        
        if position['type'] == 'BUY':
            current_price = symbol_info['bid']
            new_sl = current_price - trailing_pips * 10 * point
            
            # Only move SL if it's better than current
            if position['sl'] == 0 or new_sl > position['sl']:
                self.mt5.modify_position(position['ticket'], sl=new_sl)
        
        else:  # SELL
            current_price = symbol_info['ask']
            new_sl = current_price + trailing_pips * 10 * point
            
            # Only move SL if it's better than current
            if position['sl'] == 0 or new_sl < position['sl']:
                self.mt5.modify_position(position['ticket'], sl=new_sl)
    
    def get_status(self) -> Dict:
        """Get bot status"""
        account_info = self.mt5.get_account_info()
        open_positions = self.mt5.get_open_positions()
        
        return {
            'is_running': self.is_running,
            'connected': self.mt5.connected,
            'account': account_info,
            'open_positions': open_positions,
            'statistics': self.stats,
        }
    
    def save_stats(self):
        """Save statistics to file"""
        stats_file = 'trading_bot/stats.json'
        os.makedirs(os.path.dirname(stats_file), exist_ok=True)
        
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def load_stats(self):
        """Load statistics from file"""
        stats_file = 'trading_bot/stats.json'
        
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    self.stats.update(json.load(f))
            except Exception as e:
                logger.error(f"Error loading stats: {e}")
    
    def shutdown(self):
        """Shutdown bot and disconnect"""
        self.stop()
        self.save_stats()
        self.mt5.disconnect()
        logger.info("Bot shutdown complete")


if __name__ == "__main__":
    bot = TradingBot()
    
    if bot.initialize():
        try:
            bot.start()
            
            # Keep running
            while True:
                time.sleep(1)
        
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
        
        finally:
            bot.shutdown()
    else:
        logger.error("Failed to initialize bot")
