"""
Risk Management System for Trading Bot
"""
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np

from ..config.settings import RISK_CONFIG

logger = logging.getLogger(__name__)

class RiskManager:
    """
    Risk management system for controlling trading risks
    """
    
    def __init__(self):
        self.max_risk_per_trade = RISK_CONFIG['max_risk_per_trade']
        self.max_daily_loss = RISK_CONFIG['max_daily_loss']
        self.max_open_positions = RISK_CONFIG['max_open_positions']
        self.stop_loss_pips = RISK_CONFIG['stop_loss_pips']
        self.take_profit_pips = RISK_CONFIG['take_profit_pips']
        
        # Track daily statistics
        self.daily_trades = 0
        self.daily_pnl = 0.0
        self.daily_start_balance = 0.0
        self.last_reset_date = datetime.now().date()
        
    def check_daily_limits(self, current_pnl: float, account_balance: float = None) -> bool:
        """Check if daily risk limits are exceeded"""
        try:
            # Reset daily counters if new day
            current_date = datetime.now().date()
            if current_date != self.last_reset_date:
                self._reset_daily_counters(account_balance)
                
            # Update daily P&L
            self.daily_pnl = current_pnl
            
            # Check daily loss limit
            if account_balance and self.daily_start_balance > 0:
                daily_loss_pct = abs(current_pnl) / self.daily_start_balance
                if current_pnl < 0 and daily_loss_pct > self.max_daily_loss:
                    logger.warning(f"Daily loss limit exceeded: {daily_loss_pct:.2%} > {self.max_daily_loss:.2%}")
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(f"Error checking daily limits: {e}")
            return False
            
    def _reset_daily_counters(self, account_balance: float = None):
        """Reset daily counters for new trading day"""
        try:
            self.daily_trades = 0
            self.daily_pnl = 0.0
            if account_balance:
                self.daily_start_balance = account_balance
            self.last_reset_date = datetime.now().date()
            
            logger.info("Daily risk counters reset")
            
        except Exception as e:
            logger.error(f"Error resetting daily counters: {e}")
            
    def calculate_position_size(self, account_balance: float, entry_price: float, 
                              stop_loss: float, symbol_info: Dict = None) -> float:
        """Calculate optimal position size based on risk parameters"""
        try:
            if account_balance <= 0 or entry_price <= 0:
                return 0.0
                
            # Calculate risk amount in account currency
            risk_amount = account_balance * self.max_risk_per_trade
            
            # Calculate price difference (risk per unit)
            price_diff = abs(entry_price - stop_loss)
            if price_diff <= 0:
                logger.warning("Invalid stop loss price")
                return 0.0
                
            # Calculate position size
            position_size = risk_amount / price_diff
            
            # Apply symbol-specific constraints if available
            if symbol_info:
                min_volume = symbol_info.get('volume_min', 0.01)
                max_volume = symbol_info.get('volume_max', 100.0)
                volume_step = symbol_info.get('volume_step', 0.01)
                
                # Round to volume step
                position_size = round(position_size / volume_step) * volume_step
                
                # Apply min/max constraints
                position_size = max(min_volume, min(position_size, max_volume))
                
            # Ensure minimum position size
            if position_size < 0.01:
                position_size = 0.01
                
            # Maximum position size safety check (10% of balance)
            max_safe_size = account_balance * 0.1 / entry_price
            position_size = min(position_size, max_safe_size)
            
            logger.debug(f"Calculated position size: {position_size} for risk: {risk_amount}")
            
            return round(position_size, 2)
            
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return 0.0
            
    def validate_trade(self, symbol: str, action: str, volume: float, 
                      entry_price: float, stop_loss: float, take_profit: float,
                      current_positions: List[Dict] = None) -> Tuple[bool, str]:
        """Validate if a trade meets risk management criteria"""
        try:
            # Check position count limit
            if current_positions and len(current_positions) >= self.max_open_positions:
                return False, f"Maximum positions limit reached: {len(current_positions)}/{self.max_open_positions}"
                
            # Check if already have position in this symbol
            if current_positions:
                for pos in current_positions:
                    if pos.get('symbol') == symbol:
                        return False, f"Already have position in {symbol}"
                        
            # Validate volume
            if volume <= 0:
                return False, "Invalid volume"
                
            # Validate prices
            if entry_price <= 0 or stop_loss <= 0:
                return False, "Invalid entry or stop loss price"
                
            # Check stop loss distance
            stop_loss_distance = abs(entry_price - stop_loss) / entry_price
            if stop_loss_distance > 0.1:  # 10% maximum stop loss
                return False, f"Stop loss too far: {stop_loss_distance:.2%}"
                
            if stop_loss_distance < 0.001:  # 0.1% minimum stop loss
                return False, f"Stop loss too close: {stop_loss_distance:.2%}"
                
            # Check take profit if provided
            if take_profit > 0:
                if action.lower() == 'buy':
                    if take_profit <= entry_price:
                        return False, "Take profit must be above entry price for buy orders"
                else:  # sell
                    if take_profit >= entry_price:
                        return False, "Take profit must be below entry price for sell orders"
                        
            # Check risk-reward ratio
            if take_profit > 0:
                risk = abs(entry_price - stop_loss)
                reward = abs(take_profit - entry_price)
                risk_reward_ratio = reward / risk if risk > 0 else 0
                
                if risk_reward_ratio < 1.0:  # Minimum 1:1 risk-reward
                    return False, f"Poor risk-reward ratio: {risk_reward_ratio:.2f}"
                    
            return True, "Trade validation passed"
            
        except Exception as e:
            logger.error(f"Error validating trade: {e}")
            return False, f"Validation error: {e}"
            
    def calculate_stop_loss(self, entry_price: float, action: str, 
                           atr: float = None, volatility: float = None) -> float:
        """Calculate dynamic stop loss based on market conditions"""
        try:
            # Base stop loss in pips
            base_stop_pips = self.stop_loss_pips
            
            # Adjust based on ATR if available
            if atr and atr > 0:
                # Use 2x ATR as stop loss
                atr_stop = atr * 2
                # Convert to pips (assuming 4-digit quotes)
                atr_stop_pips = atr_stop * 10000
                
                # Use larger of base stop or ATR stop
                stop_pips = max(base_stop_pips, atr_stop_pips)
            else:
                stop_pips = base_stop_pips
                
            # Adjust based on volatility
            if volatility and volatility > 0.02:  # High volatility
                stop_pips *= 1.5
            elif volatility and volatility < 0.005:  # Low volatility
                stop_pips *= 0.8
                
            # Calculate stop loss price
            pip_value = 0.0001  # For most forex pairs
            
            if action.lower() == 'buy':
                stop_loss = entry_price - (stop_pips * pip_value)
            else:  # sell
                stop_loss = entry_price + (stop_pips * pip_value)
                
            return round(stop_loss, 5)
            
        except Exception as e:
            logger.error(f"Error calculating stop loss: {e}")
            # Fallback to fixed percentage
            if action.lower() == 'buy':
                return entry_price * 0.98  # 2% stop loss
            else:
                return entry_price * 1.02
                
    def calculate_take_profit(self, entry_price: float, stop_loss: float, 
                             action: str, risk_reward_ratio: float = 2.0) -> float:
        """Calculate take profit based on risk-reward ratio"""
        try:
            # Calculate risk (distance to stop loss)
            risk = abs(entry_price - stop_loss)
            
            # Calculate reward based on risk-reward ratio
            reward = risk * risk_reward_ratio
            
            # Calculate take profit price
            if action.lower() == 'buy':
                take_profit = entry_price + reward
            else:  # sell
                take_profit = entry_price - reward
                
            return round(take_profit, 5)
            
        except Exception as e:
            logger.error(f"Error calculating take profit: {e}")
            # Fallback to fixed percentage
            if action.lower() == 'buy':
                return entry_price * 1.04  # 4% take profit
            else:
                return entry_price * 0.96
                
    def should_close_position(self, position: Dict, current_price: float, 
                             market_data: Dict = None) -> Tuple[bool, str]:
        """Determine if a position should be closed based on risk rules"""
        try:
            entry_price = position.get('entry_price', 0)
            action = position.get('action', '').lower()
            
            if not entry_price or not action:
                return False, "Invalid position data"
                
            # Calculate current P&L percentage
            if action == 'buy':
                pnl_pct = (current_price - entry_price) / entry_price
            else:  # sell
                pnl_pct = (entry_price - current_price) / entry_price
                
            # Check for large losses (emergency stop)
            if pnl_pct < -0.15:  # 15% loss
                return True, f"Emergency stop: Large loss {pnl_pct:.2%}"
                
            # Check for trailing stop if position is profitable
            if pnl_pct > 0.05:  # 5% profit
                # Implement trailing stop logic here
                # This is a simplified version
                trailing_stop_pct = 0.02  # 2% trailing stop
                
                if action == 'buy':
                    trailing_price = current_price * (1 - trailing_stop_pct)
                    if entry_price > trailing_price:
                        return True, f"Trailing stop triggered at {trailing_stop_pct:.2%}"
                else:  # sell
                    trailing_price = current_price * (1 + trailing_stop_pct)
                    if entry_price < trailing_price:
                        return True, f"Trailing stop triggered at {trailing_stop_pct:.2%}"
                        
            return False, "Position within risk parameters"
            
        except Exception as e:
            logger.error(f"Error checking position close conditions: {e}")
            return False, f"Error: {e}"
            
    def get_risk_metrics(self) -> Dict:
        """Get current risk metrics and statistics"""
        try:
            return {
                'max_risk_per_trade': self.max_risk_per_trade,
                'max_daily_loss': self.max_daily_loss,
                'max_open_positions': self.max_open_positions,
                'daily_trades': self.daily_trades,
                'daily_pnl': self.daily_pnl,
                'daily_start_balance': self.daily_start_balance,
                'last_reset_date': self.last_reset_date.isoformat(),
                'stop_loss_pips': self.stop_loss_pips,
                'take_profit_pips': self.take_profit_pips
            }
            
        except Exception as e:
            logger.error(f"Error getting risk metrics: {e}")
            return {}
            
    def update_risk_parameters(self, new_params: Dict):
        """Update risk management parameters"""
        try:
            if 'max_risk_per_trade' in new_params:
                self.max_risk_per_trade = float(new_params['max_risk_per_trade'])
                
            if 'max_daily_loss' in new_params:
                self.max_daily_loss = float(new_params['max_daily_loss'])
                
            if 'max_open_positions' in new_params:
                self.max_open_positions = int(new_params['max_open_positions'])
                
            if 'stop_loss_pips' in new_params:
                self.stop_loss_pips = int(new_params['stop_loss_pips'])
                
            if 'take_profit_pips' in new_params:
                self.take_profit_pips = int(new_params['take_profit_pips'])
                
            logger.info("Risk parameters updated successfully")
            
        except Exception as e:
            logger.error(f"Error updating risk parameters: {e}")