"""
Main Trading Bot Class
"""
import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

from ..mt5.connector import MT5Connector
from ..ai.engine import AIEngine
from ..risk.manager import RiskManager
from ..notifications.notifier import NotificationManager
from ..config.settings import TRADING_CONFIG, RISK_CONFIG, AI_CONFIG

logger = logging.getLogger(__name__)

class TradingBot:
    """
    Main trading bot class that orchestrates all components
    """
    
    def __init__(self):
        self.mt5 = MT5Connector()
        self.ai_engine = AIEngine()
        self.risk_manager = RiskManager()
        self.notifier = NotificationManager()
        
        self.is_running = False
        self.positions = {}
        self.daily_pnl = 0.0
        self.trade_count = 0
        
        # Trading state
        self.symbols = TRADING_CONFIG['symbols']
        self.active_signals = {}
        self.last_analysis_time = {}
        
    async def start(self):
        """Start the trading bot"""
        try:
            logger.info("Starting Trading Bot...")
            
            # Initialize MT5 connection
            if not await self.mt5.connect():
                raise Exception("Failed to connect to MT5")
            
            # Initialize AI engine
            await self.ai_engine.initialize()
            
            # Start main trading loop
            self.is_running = True
            await self.notifier.send_message("🤖 Trading Bot Started Successfully!")
            
            # Main trading loop
            while self.is_running:
                try:
                    await self._trading_cycle()
                    await asyncio.sleep(60)  # Wait 1 minute between cycles
                except Exception as e:
                    logger.error(f"Error in trading cycle: {e}")
                    await asyncio.sleep(30)  # Wait 30 seconds on error
                    
        except Exception as e:
            logger.error(f"Failed to start trading bot: {e}")
            await self.notifier.send_message(f"❌ Bot Start Failed: {e}")
            
    async def stop(self):
        """Stop the trading bot"""
        logger.info("Stopping Trading Bot...")
        self.is_running = False
        
        # Close all open positions if requested
        await self._close_all_positions()
        
        # Disconnect from MT5
        await self.mt5.disconnect()
        
        await self.notifier.send_message("🛑 Trading Bot Stopped")
        
    async def _trading_cycle(self):
        """Main trading cycle"""
        try:
            # Update account info and positions
            await self._update_account_info()
            
            # Check risk limits
            if not self.risk_manager.check_daily_limits(self.daily_pnl):
                logger.warning("Daily risk limits exceeded, skipping trading")
                return
                
            # Analyze each symbol
            for symbol in self.symbols:
                try:
                    await self._analyze_symbol(symbol)
                except Exception as e:
                    logger.error(f"Error analyzing {symbol}: {e}")
                    
            # Monitor existing positions
            await self._monitor_positions()
            
        except Exception as e:
            logger.error(f"Error in trading cycle: {e}")
            
    async def _analyze_symbol(self, symbol: str):
        """Analyze a specific symbol for trading opportunities"""
        try:
            # Get market data
            data = await self.mt5.get_rates(symbol, 'H1', 100)
            if data is None or len(data) == 0:
                return
                
            # Get AI prediction
            prediction = await self.ai_engine.predict(symbol, data)
            if prediction is None:
                return
                
            # Check if we should trade
            signal = self._generate_signal(symbol, prediction, data)
            if signal:
                await self._execute_trade(symbol, signal)
                
        except Exception as e:
            logger.error(f"Error analyzing symbol {symbol}: {e}")
            
    def _generate_signal(self, symbol: str, prediction: Dict, data: List) -> Optional[Dict]:
        """Generate trading signal based on AI prediction"""
        try:
            confidence = prediction.get('confidence', 0)
            direction = prediction.get('direction', 'hold')
            
            # Check confidence threshold
            if confidence < AI_CONFIG['confidence_threshold']:
                return None
                
            # Check if we already have a position for this symbol
            if symbol in self.positions:
                return None
                
            # Generate signal
            if direction == 'buy' and confidence > AI_CONFIG['confidence_threshold']:
                return {
                    'action': 'buy',
                    'symbol': symbol,
                    'confidence': confidence,
                    'entry_price': data[-1]['close'],
                    'stop_loss': data[-1]['close'] - (RISK_CONFIG['stop_loss_pips'] * 0.0001),
                    'take_profit': data[-1]['close'] + (RISK_CONFIG['take_profit_pips'] * 0.0001)
                }
            elif direction == 'sell' and confidence > AI_CONFIG['confidence_threshold']:
                return {
                    'action': 'sell',
                    'symbol': symbol,
                    'confidence': confidence,
                    'entry_price': data[-1]['close'],
                    'stop_loss': data[-1]['close'] + (RISK_CONFIG['stop_loss_pips'] * 0.0001),
                    'take_profit': data[-1]['close'] - (RISK_CONFIG['take_profit_pips'] * 0.0001)
                }
                
            return None
            
        except Exception as e:
            logger.error(f"Error generating signal for {symbol}: {e}")
            return None
            
    async def _execute_trade(self, symbol: str, signal: Dict):
        """Execute a trade based on the signal"""
        try:
            # Calculate position size
            account_balance = await self.mt5.get_account_balance()
            position_size = self.risk_manager.calculate_position_size(
                account_balance, 
                signal['entry_price'], 
                signal['stop_loss']
            )
            
            if position_size <= 0:
                logger.warning(f"Position size too small for {symbol}")
                return
                
            # Place order
            order_result = await self.mt5.place_order(
                symbol=symbol,
                action=signal['action'],
                volume=position_size,
                price=signal['entry_price'],
                stop_loss=signal['stop_loss'],
                take_profit=signal['take_profit']
            )
            
            if order_result and order_result.get('retcode') == 10009:  # TRADE_RETCODE_DONE
                # Store position info
                self.positions[symbol] = {
                    'ticket': order_result.get('order'),
                    'action': signal['action'],
                    'volume': position_size,
                    'entry_price': signal['entry_price'],
                    'stop_loss': signal['stop_loss'],
                    'take_profit': signal['take_profit'],
                    'confidence': signal['confidence'],
                    'timestamp': datetime.now()
                }
                
                self.trade_count += 1
                
                # Send notification
                message = f"📈 New {signal['action'].upper()} position opened:\n"
                message += f"Symbol: {symbol}\n"
                message += f"Size: {position_size}\n"
                message += f"Entry: {signal['entry_price']:.5f}\n"
                message += f"Confidence: {signal['confidence']:.2%}"
                
                await self.notifier.send_message(message)
                logger.info(f"Trade executed: {symbol} {signal['action']} {position_size}")
                
            else:
                error_msg = f"Failed to execute trade for {symbol}: {order_result}"
                logger.error(error_msg)
                await self.notifier.send_message(f"❌ Trade Failed: {error_msg}")
                
        except Exception as e:
            logger.error(f"Error executing trade for {symbol}: {e}")
            await self.notifier.send_message(f"❌ Trade Execution Error: {e}")
            
    async def _monitor_positions(self):
        """Monitor existing positions"""
        try:
            # Get current positions from MT5
            current_positions = await self.mt5.get_positions()
            
            # Update our position tracking
            active_symbols = set()
            for pos in current_positions:
                symbol = pos.get('symbol')
                if symbol:
                    active_symbols.add(symbol)
                    
            # Remove closed positions from our tracking
            closed_symbols = set(self.positions.keys()) - active_symbols
            for symbol in closed_symbols:
                pos_info = self.positions.pop(symbol)
                logger.info(f"Position closed: {symbol}")
                
                # Calculate P&L and send notification
                # This would need actual P&L calculation from MT5
                await self.notifier.send_message(f"📊 Position closed: {symbol}")
                
        except Exception as e:
            logger.error(f"Error monitoring positions: {e}")
            
    async def _update_account_info(self):
        """Update account information"""
        try:
            account_info = await self.mt5.get_account_info()
            if account_info:
                self.daily_pnl = account_info.get('profit', 0.0)
                
        except Exception as e:
            logger.error(f"Error updating account info: {e}")
            
    async def _close_all_positions(self):
        """Close all open positions"""
        try:
            positions = await self.mt5.get_positions()
            for pos in positions:
                await self.mt5.close_position(pos.get('ticket'))
                
        except Exception as e:
            logger.error(f"Error closing positions: {e}")
            
    async def get_status(self) -> Dict:
        """Get bot status for web interface"""
        try:
            account_info = await self.mt5.get_account_info()
            positions = await self.mt5.get_positions()
            
            return {
                'is_running': self.is_running,
                'account_balance': account_info.get('balance', 0) if account_info else 0,
                'account_equity': account_info.get('equity', 0) if account_info else 0,
                'daily_pnl': self.daily_pnl,
                'open_positions': len(positions) if positions else 0,
                'trade_count': self.trade_count,
                'positions': self.positions,
                'last_update': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return {
                'is_running': self.is_running,
                'error': str(e),
                'last_update': datetime.now().isoformat()
            }