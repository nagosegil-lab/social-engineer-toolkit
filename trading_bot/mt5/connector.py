"""
MetaTrader 5 Connector for Trading Operations
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import MetaTrader5 as mt5
import pandas as pd

from ..config.settings import MT5_CONFIG, TRADING_CONFIG

logger = logging.getLogger(__name__)

class MT5Connector:
    """
    MetaTrader 5 connector for trading operations
    """
    
    def __init__(self):
        self.connected = False
        self.account_info = None
        
    async def connect(self) -> bool:
        """Connect to MetaTrader 5"""
        try:
            # Initialize MT5
            if not mt5.initialize():
                logger.error("MT5 initialization failed")
                return False
                
            # Login to account
            if MT5_CONFIG['login'] and MT5_CONFIG['password']:
                login_result = mt5.login(
                    login=MT5_CONFIG['login'],
                    password=MT5_CONFIG['password'],
                    server=MT5_CONFIG['server']
                )
                
                if not login_result:
                    logger.error(f"MT5 login failed: {mt5.last_error()}")
                    return False
                    
            # Verify connection
            account_info = mt5.account_info()
            if account_info is None:
                logger.error("Failed to get account info")
                return False
                
            self.account_info = account_info._asdict()
            self.connected = True
            
            logger.info(f"Connected to MT5 account: {self.account_info.get('login')}")
            logger.info(f"Account balance: {self.account_info.get('balance')}")
            
            return True
            
        except Exception as e:
            logger.error(f"MT5 connection error: {e}")
            return False
            
    async def disconnect(self):
        """Disconnect from MetaTrader 5"""
        try:
            mt5.shutdown()
            self.connected = False
            logger.info("Disconnected from MT5")
            
        except Exception as e:
            logger.error(f"MT5 disconnection error: {e}")
            
    async def get_account_info(self) -> Optional[Dict]:
        """Get account information"""
        try:
            if not self.connected:
                return None
                
            account_info = mt5.account_info()
            if account_info is None:
                return None
                
            return account_info._asdict()
            
        except Exception as e:
            logger.error(f"Error getting account info: {e}")
            return None
            
    async def get_account_balance(self) -> float:
        """Get account balance"""
        try:
            account_info = await self.get_account_info()
            return account_info.get('balance', 0.0) if account_info else 0.0
            
        except Exception as e:
            logger.error(f"Error getting account balance: {e}")
            return 0.0
            
    async def get_rates(self, symbol: str, timeframe: str, count: int = 100) -> Optional[List[Dict]]:
        """Get historical rates for a symbol"""
        try:
            if not self.connected:
                return None
                
            # Convert timeframe string to MT5 constant
            tf_map = {
                'M1': mt5.TIMEFRAME_M1,
                'M5': mt5.TIMEFRAME_M5,
                'M15': mt5.TIMEFRAME_M15,
                'M30': mt5.TIMEFRAME_M30,
                'H1': mt5.TIMEFRAME_H1,
                'H4': mt5.TIMEFRAME_H4,
                'D1': mt5.TIMEFRAME_D1
            }
            
            mt5_timeframe = tf_map.get(timeframe, mt5.TIMEFRAME_H1)
            
            # Get rates
            rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, count)
            if rates is None or len(rates) == 0:
                logger.warning(f"No rates data for {symbol}")
                return None
                
            # Convert to list of dictionaries
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            
            return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error getting rates for {symbol}: {e}")
            return None
            
    async def get_symbol_info(self, symbol: str) -> Optional[Dict]:
        """Get symbol information"""
        try:
            if not self.connected:
                return None
                
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                return None
                
            return symbol_info._asdict()
            
        except Exception as e:
            logger.error(f"Error getting symbol info for {symbol}: {e}")
            return None
            
    async def get_tick(self, symbol: str) -> Optional[Dict]:
        """Get current tick for symbol"""
        try:
            if not self.connected:
                return None
                
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                return None
                
            return tick._asdict()
            
        except Exception as e:
            logger.error(f"Error getting tick for {symbol}: {e}")
            return None
            
    async def place_order(self, symbol: str, action: str, volume: float, 
                         price: Optional[float] = None, stop_loss: Optional[float] = None,
                         take_profit: Optional[float] = None, 
                         order_type: str = 'market') -> Optional[Dict]:
        """Place a trading order"""
        try:
            if not self.connected:
                return None
                
            # Get symbol info for lot size calculation
            symbol_info = await self.get_symbol_info(symbol)
            if not symbol_info:
                logger.error(f"Could not get symbol info for {symbol}")
                return None
                
            # Prepare order request
            if action.lower() == 'buy':
                order_type_mt5 = mt5.ORDER_TYPE_BUY if order_type == 'market' else mt5.ORDER_TYPE_BUY_LIMIT
                if price is None:
                    tick = await self.get_tick(symbol)
                    price = tick['ask'] if tick else None
            else:  # sell
                order_type_mt5 = mt5.ORDER_TYPE_SELL if order_type == 'market' else mt5.ORDER_TYPE_SELL_LIMIT
                if price is None:
                    tick = await self.get_tick(symbol)
                    price = tick['bid'] if tick else None
                    
            if price is None:
                logger.error(f"Could not get price for {symbol}")
                return None
                
            # Round volume to symbol's volume step
            volume_step = symbol_info.get('volume_step', 0.01)
            volume = round(volume / volume_step) * volume_step
            
            # Prepare request
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type_mt5,
                "price": price,
                "deviation": TRADING_CONFIG.get('max_slippage', 3),
                "magic": 234000,
                "comment": "Trading Bot",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # Add stop loss and take profit if provided
            if stop_loss:
                request["sl"] = stop_loss
            if take_profit:
                request["tp"] = take_profit
                
            # Send order
            result = mt5.order_send(request)
            
            if result is None:
                logger.error(f"Order send failed: {mt5.last_error()}")
                return None
                
            result_dict = result._asdict()
            
            if result_dict.get('retcode') != mt5.TRADE_RETCODE_DONE:
                logger.error(f"Order failed: {result_dict}")
                return result_dict
                
            logger.info(f"Order placed successfully: {symbol} {action} {volume}")
            return result_dict
            
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return None
            
    async def get_positions(self) -> Optional[List[Dict]]:
        """Get all open positions"""
        try:
            if not self.connected:
                return None
                
            positions = mt5.positions_get()
            if positions is None:
                return []
                
            return [pos._asdict() for pos in positions]
            
        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            return None
            
    async def get_position(self, symbol: str) -> Optional[Dict]:
        """Get position for specific symbol"""
        try:
            if not self.connected:
                return None
                
            positions = mt5.positions_get(symbol=symbol)
            if positions is None or len(positions) == 0:
                return None
                
            return positions[0]._asdict()
            
        except Exception as e:
            logger.error(f"Error getting position for {symbol}: {e}")
            return None
            
    async def close_position(self, ticket: int) -> Optional[Dict]:
        """Close a position by ticket"""
        try:
            if not self.connected:
                return None
                
            # Get position info
            positions = mt5.positions_get(ticket=ticket)
            if not positions:
                logger.error(f"Position {ticket} not found")
                return None
                
            position = positions[0]
            
            # Prepare close request
            if position.type == mt5.POSITION_TYPE_BUY:
                order_type = mt5.ORDER_TYPE_SELL
                price = mt5.symbol_info_tick(position.symbol).bid
            else:
                order_type = mt5.ORDER_TYPE_BUY
                price = mt5.symbol_info_tick(position.symbol).ask
                
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": order_type,
                "position": ticket,
                "price": price,
                "deviation": TRADING_CONFIG.get('max_slippage', 3),
                "magic": 234000,
                "comment": "Trading Bot Close",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # Send close order
            result = mt5.order_send(request)
            
            if result is None:
                logger.error(f"Close order failed: {mt5.last_error()}")
                return None
                
            result_dict = result._asdict()
            
            if result_dict.get('retcode') != mt5.TRADE_RETCODE_DONE:
                logger.error(f"Close order failed: {result_dict}")
                return result_dict
                
            logger.info(f"Position {ticket} closed successfully")
            return result_dict
            
        except Exception as e:
            logger.error(f"Error closing position {ticket}: {e}")
            return None
            
    async def get_history_deals(self, days: int = 7) -> Optional[List[Dict]]:
        """Get trading history"""
        try:
            if not self.connected:
                return None
                
            # Get deals from last N days
            from_date = datetime.now() - timedelta(days=days)
            to_date = datetime.now()
            
            deals = mt5.history_deals_get(from_date, to_date)
            if deals is None:
                return []
                
            return [deal._asdict() for deal in deals]
            
        except Exception as e:
            logger.error(f"Error getting history deals: {e}")
            return None
            
    async def check_market_hours(self, symbol: str) -> bool:
        """Check if market is open for trading"""
        try:
            symbol_info = await self.get_symbol_info(symbol)
            if not symbol_info:
                return False
                
            # Check if symbol is available for trading
            return symbol_info.get('trade_mode') == mt5.SYMBOL_TRADE_MODE_FULL
            
        except Exception as e:
            logger.error(f"Error checking market hours for {symbol}: {e}")
            return False