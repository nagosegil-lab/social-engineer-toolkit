"""
Risk Management System for Trading Bot
"""
import logging
from datetime import datetime, timedelta
from config import Config

class RiskManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.daily_pnl = 0.0
        self.daily_trades = 0
        self.max_daily_trades = 50
        self.last_reset_date = datetime.now().date()
        
    def reset_daily_stats(self):
        """Reset daily statistics"""
        current_date = datetime.now().date()
        if current_date != self.last_reset_date:
            self.daily_pnl = 0.0
            self.daily_trades = 0
            self.last_reset_date = current_date
            self.logger.info("Daily statistics reset")
    
    def can_open_position(self, account_balance, current_positions, symbol):
        """Check if we can open a new position"""
        self.reset_daily_stats()
        
        # Check daily loss limit
        if self.daily_pnl <= -Config.MAX_DAILY_LOSS:
            self.logger.warning(f"Daily loss limit reached: {self.daily_pnl}")
            return False, "Daily loss limit reached"
        
        # Check daily profit limit
        if self.daily_pnl >= Config.MAX_DAILY_PROFIT:
            self.logger.warning(f"Daily profit limit reached: {self.daily_pnl}")
            return False, "Daily profit limit reached"
        
        # Check maximum positions
        if len(current_positions) >= Config.MAX_POSITIONS:
            self.logger.warning(f"Maximum positions limit reached: {len(current_positions)}")
            return False, "Maximum positions limit reached"
        
        # Check daily trade limit
        if self.daily_trades >= self.max_daily_trades:
            self.logger.warning(f"Daily trade limit reached: {self.daily_trades}")
            return False, "Daily trade limit reached"
        
        # Check if position already exists for this symbol
        for pos in current_positions:
            if pos['symbol'] == symbol:
                self.logger.warning(f"Position already exists for {symbol}")
                return False, "Position already exists for this symbol"
        
        return True, "OK"
    
    def calculate_position_size(self, account_balance, risk_percent=2.0, stop_loss_pips=None):
        """Calculate position size based on risk management"""
        try:
            if stop_loss_pips is None:
                stop_loss_pips = Config.STOP_LOSS_PIPS
            
            # Calculate risk amount
            risk_amount = account_balance * (risk_percent / 100)
            
            # Calculate position size based on stop loss
            # Assuming 1 pip = 0.0001 for most pairs
            pip_value = 0.0001
            position_size = risk_amount / (stop_loss_pips * pip_value)
            
            # Apply maximum lot size limit
            max_lot_size = min(position_size, Config.LOT_SIZE * 10)  # Max 10x default lot size
            
            # Ensure minimum lot size
            min_lot_size = Config.LOT_SIZE
            
            final_size = max(min_lot_size, min(max_lot_size, position_size))
            
            self.logger.info(f"Calculated position size: {final_size:.2f} lots")
            return final_size
            
        except Exception as e:
            self.logger.error(f"Error calculating position size: {e}")
            return Config.LOT_SIZE
    
    def calculate_stop_loss(self, entry_price, order_type, atr=None):
        """Calculate stop loss level"""
        try:
            if atr is None:
                # Default stop loss based on pips
                stop_loss_pips = Config.STOP_LOSS_PIPS
                pip_value = 0.0001
                
                if order_type == 0:  # Buy order
                    sl = entry_price - (stop_loss_pips * pip_value)
                else:  # Sell order
                    sl = entry_price + (stop_loss_pips * pip_value)
            else:
                # ATR-based stop loss (2x ATR)
                atr_multiplier = 2.0
                
                if order_type == 0:  # Buy order
                    sl = entry_price - (atr * atr_multiplier)
                else:  # Sell order
                    sl = entry_price + (atr * atr_multiplier)
            
            return sl
            
        except Exception as e:
            self.logger.error(f"Error calculating stop loss: {e}")
            return None
    
    def calculate_take_profit(self, entry_price, order_type, stop_loss=None):
        """Calculate take profit level"""
        try:
            if stop_loss is None:
                # Default take profit based on pips
                take_profit_pips = Config.TAKE_PROFIT_PIPS
                pip_value = 0.0001
                
                if order_type == 0:  # Buy order
                    tp = entry_price + (take_profit_pips * pip_value)
                else:  # Sell order
                    tp = entry_price - (take_profit_pips * pip_value)
            else:
                # Risk-reward ratio of 1:2
                risk_reward_ratio = 2.0
                risk = abs(entry_price - stop_loss)
                
                if order_type == 0:  # Buy order
                    tp = entry_price + (risk * risk_reward_ratio)
                else:  # Sell order
                    tp = entry_price - (risk * risk_reward_ratio)
            
            return tp
            
        except Exception as e:
            self.logger.error(f"Error calculating take profit: {e}")
            return None
    
    def update_daily_pnl(self, pnl_change):
        """Update daily P&L"""
        self.daily_pnl += pnl_change
        self.logger.info(f"Daily P&L updated: {self.daily_pnl:.2f}")
    
    def update_daily_trades(self):
        """Update daily trade count"""
        self.daily_trades += 1
        self.logger.info(f"Daily trades count: {self.daily_trades}")
    
    def get_risk_summary(self):
        """Get current risk summary"""
        self.reset_daily_stats()
        
        return {
            'daily_pnl': self.daily_pnl,
            'daily_trades': self.daily_trades,
            'max_daily_loss': Config.MAX_DAILY_LOSS,
            'max_daily_profit': Config.MAX_DAILY_PROFIT,
            'max_positions': Config.MAX_POSITIONS,
            'max_daily_trades': self.max_daily_trades,
            'risk_status': self._get_risk_status()
        }
    
    def _get_risk_status(self):
        """Get current risk status"""
        if self.daily_pnl <= -Config.MAX_DAILY_LOSS:
            return "HIGH_RISK - Daily loss limit reached"
        elif self.daily_pnl >= Config.MAX_DAILY_PROFIT:
            return "PROFIT_LIMIT - Daily profit limit reached"
        elif self.daily_trades >= self.max_daily_trades:
            return "TRADE_LIMIT - Daily trade limit reached"
        else:
            return "NORMAL"
    
    def should_close_position(self, position, current_price):
        """Check if position should be closed based on risk rules"""
        try:
            # Calculate current P&L
            if position['type'] == 0:  # Buy position
                pnl = (current_price - position['price_open']) * position['volume'] * 100000
            else:  # Sell position
                pnl = (position['price_open'] - current_price) * position['volume'] * 100000
            
            # Close if daily loss limit would be exceeded
            if self.daily_pnl + pnl <= -Config.MAX_DAILY_LOSS:
                return True, "Daily loss limit protection"
            
            # Close if position is very profitable (trailing stop)
            if pnl > 100:  # $100 profit
                return True, "Profit taking"
            
            return False, "Hold"
            
        except Exception as e:
            self.logger.error(f"Error checking position close: {e}")
            return False, "Error"
    
    def get_position_risk_score(self, position, current_price):
        """Calculate risk score for a position (0-100)"""
        try:
            if position['type'] == 0:  # Buy position
                pnl = (current_price - position['price_open']) * position['volume'] * 100000
            else:  # Sell position
                pnl = (position['price_open'] - current_price) * position['volume'] * 100000
            
            # Calculate risk score based on P&L relative to account balance
            # This is a simplified calculation
            risk_score = min(100, max(0, abs(pnl) / 10))  # Scale to 0-100
            
            return risk_score
            
        except Exception as e:
            self.logger.error(f"Error calculating risk score: {e}")
            return 50  # Default medium risk