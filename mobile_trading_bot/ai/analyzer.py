"""
Market Analysis Module
מודול ניתוח שווקים
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from mobile_trading_bot.core.logger import setup_logger

logger = setup_logger(__name__)


class MarketAnalyzer:
    """Performs technical analysis on market data"""
    
    def __init__(self):
        pass
    
    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(
        self,
        df: pd.DataFrame,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> Dict[str, pd.Series]:
        """Calculate MACD indicator"""
        ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        
        return {
            'macd': macd,
            'signal': signal_line,
            'histogram': histogram
        }
    
    def calculate_bollinger_bands(
        self,
        df: pd.DataFrame,
        period: int = 20,
        std_dev: int = 2
    ) -> Dict[str, pd.Series]:
        """Calculate Bollinger Bands"""
        sma = df['close'].rolling(window=period).mean()
        std = df['close'].rolling(window=period).std()
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        return {
            'upper': upper_band,
            'middle': sma,
            'lower': lower_band
        }
    
    def analyze_market(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Comprehensive market analysis
        ניתוח שוק מקיף
        
        Args:
            df: Market data DataFrame
            
        Returns:
            Dictionary with analysis results
        """
        if len(df) < 50:
            return {"error": "Insufficient data for analysis"}
        
        try:
            # Calculate indicators
            rsi = self.calculate_rsi(df)
            macd = self.calculate_macd(df)
            bb = self.calculate_bollinger_bands(df)
            
            # Current values
            current_price = df['close'].iloc[-1]
            current_rsi = rsi.iloc[-1]
            current_macd = macd['macd'].iloc[-1]
            current_signal = macd['signal'].iloc[-1]
            
            # Trend analysis
            sma_20 = df['close'].rolling(window=20).mean().iloc[-1]
            sma_50 = df['close'].rolling(window=50).mean().iloc[-1]
            
            # Signals
            signals = []
            strength = 0
            
            # RSI signals
            if current_rsi > 70:
                signals.append("OVERSOLD")
                strength -= 1
            elif current_rsi < 30:
                signals.append("OVERSOLD")
                strength += 1
            
            # MACD signals
            if current_macd > current_signal:
                signals.append("BULLISH_MACD")
                strength += 1
            else:
                signals.append("BEARISH_MACD")
                strength -= 1
            
            # Bollinger Bands
            if current_price > bb['upper'].iloc[-1]:
                signals.append("ABOVE_UPPER_BB")
                strength -= 1
            elif current_price < bb['lower'].iloc[-1]:
                signals.append("BELOW_LOWER_BB")
                strength += 1
            
            # Overall trend
            if current_price > sma_20 > sma_50:
                trend = "UPTREND"
                strength += 1
            elif current_price < sma_20 < sma_50:
                trend = "DOWNTREND"
                strength -= 1
            else:
                trend = "SIDEWAYS"
            
            # Overall recommendation
            if strength >= 2:
                recommendation = "STRONG_BUY"
            elif strength >= 1:
                recommendation = "BUY"
            elif strength <= -2:
                recommendation = "STRONG_SELL"
            elif strength <= -1:
                recommendation = "SELL"
            else:
                recommendation = "HOLD"
            
            return {
                "current_price": float(current_price),
                "rsi": float(current_rsi),
                "macd": float(current_macd),
                "signal_line": float(current_signal),
                "bollinger_upper": float(bb['upper'].iloc[-1]),
                "bollinger_lower": float(bb['lower'].iloc[-1]),
                "sma_20": float(sma_20),
                "sma_50": float(sma_50),
                "trend": trend,
                "signals": signals,
                "strength": strength,
                "recommendation": recommendation
            }
            
        except Exception as e:
            logger.error(f"Error analyzing market: {str(e)}")
            return {"error": str(e)}
