"""
MT5 Data Retrieval
קבלת נתונים מ-MT5
"""

import MetaTrader5 as mt5
import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from mobile_trading_bot.core.logger import setup_logger
from mobile_trading_bot.mt5.connection import mt5_connection

logger = setup_logger(__name__)


class MT5Data:
    """Handles data retrieval from MT5"""
    
    def __init__(self):
        self.connection = mt5_connection
    
    def get_symbol_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get symbol information
        קבלת מידע על סמל מסחר
        
        Args:
            symbol: Trading symbol (e.g., 'EURUSD')
            
        Returns:
            Symbol information dictionary or None
        """
        if not self.connection.is_connected():
            logger.error("Not connected to MT5")
            return None
        
        try:
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                logger.error(f"Symbol {symbol} not found")
                return None
            
            return symbol_info._asdict()
        except Exception as e:
            logger.error(f"Error getting symbol info: {str(e)}")
            return None
    
    def get_rates(
        self,
        symbol: str,
        timeframe: int = mt5.TIMEFRAME_M15,
        count: int = 1000,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Optional[pd.DataFrame]:
        """
        Get historical rates
        קבלת נתוני מחיר היסטוריים
        
        Args:
            symbol: Trading symbol
            timeframe: Timeframe (MT5 constant)
            count: Number of bars to retrieve
            start_date: Start date (optional)
            end_date: End date (optional)
            
        Returns:
            DataFrame with OHLCV data
        """
        if not self.connection.is_connected():
            logger.error("Not connected to MT5")
            return None
        
        try:
            if start_date and end_date:
                rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)
            elif start_date:
                rates = mt5.copy_rates_from(symbol, timeframe, start_date, count)
            else:
                rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
            
            if rates is None or len(rates) == 0:
                logger.error(f"No rates data for {symbol}")
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Error getting rates: {str(e)}")
            return None
    
    def get_current_price(self, symbol: str) -> Optional[Dict[str, float]]:
        """
        Get current price
        קבלת מחיר נוכחי
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Dictionary with 'bid' and 'ask' prices
        """
        if not self.connection.is_connected():
            logger.error("Not connected to MT5")
            return None
        
        try:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                logger.error(f"Failed to get tick for {symbol}")
                return None
            
            return {
                'bid': tick.bid,
                'ask': tick.ask,
                'last': tick.last,
                'volume': tick.volume,
                'time': datetime.fromtimestamp(tick.time)
            }
        except Exception as e:
            logger.error(f"Error getting current price: {str(e)}")
            return None
    
    def get_positions(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get open positions
        קבלת פוזיציות פתוחות
        
        Args:
            symbol: Filter by symbol (optional)
            
        Returns:
            List of position dictionaries
        """
        if not self.connection.is_connected():
            logger.error("Not connected to MT5")
            return []
        
        try:
            if symbol:
                positions = mt5.positions_get(symbol=symbol)
            else:
                positions = mt5.positions_get()
            
            if positions is None:
                return []
            
            return [pos._asdict() for pos in positions]
        except Exception as e:
            logger.error(f"Error getting positions: {str(e)}")
            return []
    
    def get_orders(self) -> List[Dict[str, Any]]:
        """
        Get pending orders
        קבלת הזמנות ממתינות
        """
        if not self.connection.is_connected():
            logger.error("Not connected to MT5")
            return []
        
        try:
            orders = mt5.orders_get()
            if orders is None:
                return []
            
            return [order._asdict() for order in orders]
        except Exception as e:
            logger.error(f"Error getting orders: {str(e)}")
            return []
