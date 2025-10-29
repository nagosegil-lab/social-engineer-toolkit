"""
MetaTrader 5 Connector for Trading Bot
"""
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import logging
from config import Config

class MT5Connector:
    def __init__(self):
        self.connected = False
        self.logger = logging.getLogger(__name__)
        
    def connect(self):
        """Connect to MetaTrader 5"""
        try:
            if not mt5.initialize(path=Config.MT5_PATH):
                self.logger.error(f"MT5 initialization failed: {mt5.last_error()}")
                return False
                
            if not mt5.login(Config.MT5_LOGIN, password=Config.MT5_PASSWORD, server=Config.MT5_SERVER):
                self.logger.error(f"MT5 login failed: {mt5.last_error()}")
                return False
                
            self.connected = True
            self.logger.info("Successfully connected to MT5")
            return True
            
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MetaTrader 5"""
        mt5.shutdown()
        self.connected = False
        self.logger.info("Disconnected from MT5")
    
    def get_account_info(self):
        """Get account information"""
        if not self.connected:
            return None
            
        account_info = mt5.account_info()
        if account_info is None:
            self.logger.error(f"Failed to get account info: {mt5.last_error()}")
            return None
            
        return {
            'balance': account_info.balance,
            'equity': account_info.equity,
            'margin': account_info.margin,
            'free_margin': account_info.margin_free,
            'margin_level': account_info.margin_level,
            'currency': account_info.currency,
            'leverage': account_info.leverage
        }
    
    def get_historical_data(self, symbol, timeframe, count=1000):
        """Get historical price data"""
        if not self.connected:
            return None
            
        try:
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
            
            tf = tf_map.get(timeframe, mt5.TIMEFRAME_M15)
            
            rates = mt5.copy_rates_from_pos(symbol, tf, 0, count)
            if rates is None:
                self.logger.error(f"Failed to get rates: {mt5.last_error()}")
                return None
                
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error getting historical data: {e}")
            return None
    
    def get_current_price(self, symbol):
        """Get current price for symbol"""
        if not self.connected:
            return None
            
        try:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                self.logger.error(f"Failed to get tick: {mt5.last_error()}")
                return None
                
            return {
                'bid': tick.bid,
                'ask': tick.ask,
                'last': tick.last,
                'volume': tick.volume,
                'time': datetime.fromtimestamp(tick.time)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting current price: {e}")
            return None
    
    def place_order(self, symbol, order_type, volume, price=None, sl=None, tp=None, comment="Trading Bot"):
        """Place a trading order"""
        if not self.connected:
            return None
            
        try:
            # Prepare order request
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "deviation": 20,
                "magic": 234000,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            if price is not None:
                request["price"] = price
            if sl is not None:
                request["sl"] = sl
            if tp is not None:
                request["tp"] = tp
            
            # Send order
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                self.logger.error(f"Order failed: {result.retcode} - {result.comment}")
                return None
                
            self.logger.info(f"Order placed successfully: {result.order}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error placing order: {e}")
            return None
    
    def get_positions(self, symbol=None):
        """Get open positions"""
        if not self.connected:
            return []
            
        try:
            if symbol:
                positions = mt5.positions_get(symbol=symbol)
            else:
                positions = mt5.positions_get()
                
            if positions is None:
                return []
                
            return [
                {
                    'ticket': pos.ticket,
                    'symbol': pos.symbol,
                    'type': pos.type,
                    'volume': pos.volume,
                    'price_open': pos.price_open,
                    'price_current': pos.price_current,
                    'sl': pos.sl,
                    'tp': pos.tp,
                    'profit': pos.profit,
                    'swap': pos.swap,
                    'time': datetime.fromtimestamp(pos.time)
                }
                for pos in positions
            ]
            
        except Exception as e:
            self.logger.error(f"Error getting positions: {e}")
            return []
    
    def close_position(self, ticket):
        """Close a position by ticket"""
        if not self.connected:
            return False
            
        try:
            position = mt5.positions_get(ticket=ticket)
            if not position:
                self.logger.error(f"Position {ticket} not found")
                return False
                
            position = position[0]
            
            # Determine close order type
            if position.type == mt5.ORDER_TYPE_BUY:
                order_type = mt5.ORDER_TYPE_SELL
            else:
                order_type = mt5.ORDER_TYPE_BUY
                
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": order_type,
                "position": ticket,
                "deviation": 20,
                "magic": 234000,
                "comment": "Close position",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                self.logger.error(f"Close order failed: {result.retcode} - {result.comment}")
                return False
                
            self.logger.info(f"Position {ticket} closed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error closing position: {e}")
            return False