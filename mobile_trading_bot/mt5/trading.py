"""
MT5 Trading Operations
פעולות מסחר ב-MT5
"""

import MetaTrader5 as mt5
from typing import Optional, Dict, Any
from enum import Enum
from mobile_trading_bot.core.logger import setup_logger
from mobile_trading_bot.mt5.connection import mt5_connection
from mobile_trading_bot.core.config import settings

logger = setup_logger(__name__)


class OrderType(Enum):
    """Order type enumeration"""
    BUY = mt5.ORDER_TYPE_BUY
    SELL = mt5.ORDER_TYPE_SELL
    BUY_LIMIT = mt5.ORDER_TYPE_BUY_LIMIT
    SELL_LIMIT = mt5.ORDER_TYPE_SELL_LIMIT
    BUY_STOP = mt5.ORDER_TYPE_BUY_STOP
    SELL_STOP = mt5.ORDER_TYPE_SELL_STOP


class MT5Trading:
    """Handles trading operations"""
    
    def __init__(self):
        self.connection = mt5_connection
    
    def place_order(
        self,
        symbol: str,
        order_type: OrderType,
        volume: float,
        price: Optional[float] = None,
        sl: Optional[float] = None,
        tp: Optional[float] = None,
        comment: str = "Mobile Trading Bot"
    ) -> Optional[Dict[str, Any]]:
        """
        Place a trading order
        ביצוע עסקה
        
        Args:
            symbol: Trading symbol
            order_type: Type of order (BUY/SELL)
            volume: Lot size
            price: Price (for limit/stop orders)
            sl: Stop Loss price
            tp: Take Profit price
            comment: Order comment
            
        Returns:
            Order result dictionary or None
        """
        if not self.connection.is_connected():
            logger.error("Not connected to MT5")
            return None
        
        try:
            # Get symbol info
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                logger.error(f"Symbol {symbol} not found")
                return None
            
            # Normalize symbol
            symbol = symbol_info.name
            
            # For market orders, get current price
            if order_type in [OrderType.BUY, OrderType.SELL] and price is None:
                tick = mt5.symbol_info_tick(symbol)
                if order_type == OrderType.BUY:
                    price = mt5.symbol_info_tick(symbol).ask
                else:
                    price = mt5.symbol_info_tick(symbol).bid
            
            # Prepare order request
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type.value,
                "price": price,
                "deviation": 20,
                "magic": 234000,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # Add SL and TP if provided
            if sl:
                request["sl"] = sl
            if tp:
                request["tp"] = tp
            
            # Send order
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                logger.error(f"Order failed: {result.retcode} - {result.comment}")
                return {
                    "success": False,
                    "retcode": result.retcode,
                    "comment": result.comment
                }
            
            logger.info(f"✅ Order placed successfully: {symbol} {order_type.name} {volume} lots")
            return {
                "success": True,
                "order_id": result.order,
                "volume": result.volume,
                "price": result.price,
                "retcode": result.retcode,
                "comment": result.comment
            }
            
        except Exception as e:
            logger.error(f"Error placing order: {str(e)}")
            return None
    
    def close_position(self, ticket: int) -> Optional[Dict[str, Any]]:
        """
        Close a position
        סגירת פוזיציה
        
        Args:
            ticket: Position ticket
            
        Returns:
            Close result dictionary or None
        """
        if not self.connection.is_connected():
            logger.error("Not connected to MT5")
            return None
        
        try:
            # Get position
            position = mt5.positions_get(ticket=ticket)
            if position is None or len(position) == 0:
                logger.error(f"Position {ticket} not found")
                return None
            
            position = position[0]
            
            # Prepare close request
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
                "position": ticket,
                "deviation": 20,
                "magic": 234000,
                "comment": "Close position",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                logger.error(f"Close position failed: {result.retcode} - {result.comment}")
                return {
                    "success": False,
                    "retcode": result.retcode,
                    "comment": result.comment
                }
            
            logger.info(f"✅ Position {ticket} closed successfully")
            return {
                "success": True,
                "retcode": result.retcode,
                "comment": result.comment
            }
            
        except Exception as e:
            logger.error(f"Error closing position: {str(e)}")
            return None
    
    def modify_order(
        self,
        ticket: int,
        sl: Optional[float] = None,
        tp: Optional[float] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Modify an order or position
        שינוי הזמנה או פוזיציה
        
        Args:
            ticket: Order/Position ticket
            sl: New Stop Loss
            tp: New Take Profit
            
        Returns:
            Modify result dictionary or None
        """
        if not self.connection.is_connected():
            logger.error("Not connected to MT5")
            return None
        
        try:
            request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "position": ticket,
            }
            
            if sl:
                request["sl"] = sl
            if tp:
                request["tp"] = tp
            
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                logger.error(f"Modify order failed: {result.retcode}")
                return {
                    "success": False,
                    "retcode": result.retcode
                }
            
            logger.info(f"✅ Order {ticket} modified successfully")
            return {
                "success": True,
                "retcode": result.retcode
            }
            
        except Exception as e:
            logger.error(f"Error modifying order: {str(e)}")
            return None
