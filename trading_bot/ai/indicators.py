"""
Technical Indicators for Market Analysis
"""
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class TechnicalIndicators:
    """
    Technical indicators for market analysis
    """
    
    def __init__(self):
        pass
        
    def add_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add all technical indicators to the dataframe"""
        try:
            # Make a copy to avoid modifying original
            df_copy = df.copy()
            
            # Moving Averages
            df_copy = self.add_moving_averages(df_copy)
            
            # RSI
            df_copy = self.add_rsi(df_copy)
            
            # MACD
            df_copy = self.add_macd(df_copy)
            
            # Bollinger Bands
            df_copy = self.add_bollinger_bands(df_copy)
            
            # ATR
            df_copy = self.add_atr(df_copy)
            
            # Stochastic
            df_copy = self.add_stochastic(df_copy)
            
            # Volume indicators
            df_copy = self.add_volume_indicators(df_copy)
            
            return df_copy
            
        except Exception as e:
            logger.error(f"Error adding indicators: {e}")
            return df
            
    def add_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add moving averages"""
        try:
            # Simple Moving Averages
            df['sma_5'] = df['close'].rolling(window=5).mean()
            df['sma_10'] = df['close'].rolling(window=10).mean()
            df['sma_20'] = df['close'].rolling(window=20).mean()
            df['sma_50'] = df['close'].rolling(window=50).mean()
            df['sma_200'] = df['close'].rolling(window=200).mean()
            
            # Exponential Moving Averages
            df['ema_12'] = df['close'].ewm(span=12).mean()
            df['ema_26'] = df['close'].ewm(span=26).mean()
            df['ema_50'] = df['close'].ewm(span=50).mean()
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding moving averages: {e}")
            return df
            
    def add_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """Add RSI indicator"""
        try:
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding RSI: {e}")
            return df
            
    def add_macd(self, df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """Add MACD indicator"""
        try:
            ema_fast = df['close'].ewm(span=fast).mean()
            ema_slow = df['close'].ewm(span=slow).mean()
            
            df['macd'] = ema_fast - ema_slow
            df['macd_signal'] = df['macd'].ewm(span=signal).mean()
            df['macd_histogram'] = df['macd'] - df['macd_signal']
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding MACD: {e}")
            return df
            
    def add_bollinger_bands(self, df: pd.DataFrame, period: int = 20, std: float = 2) -> pd.DataFrame:
        """Add Bollinger Bands"""
        try:
            sma = df['close'].rolling(window=period).mean()
            std_dev = df['close'].rolling(window=period).std()
            
            df['bb_upper'] = sma + (std_dev * std)
            df['bb_middle'] = sma
            df['bb_lower'] = sma - (std_dev * std)
            
            # Bollinger Band Width and %B
            df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']
            df['bb_percent'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding Bollinger Bands: {e}")
            return df
            
    def add_atr(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """Add Average True Range"""
        try:
            high_low = df['high'] - df['low']
            high_close = np.abs(df['high'] - df['close'].shift())
            low_close = np.abs(df['low'] - df['close'].shift())
            
            true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            df['atr'] = true_range.rolling(window=period).mean()
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding ATR: {e}")
            return df
            
    def add_stochastic(self, df: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> pd.DataFrame:
        """Add Stochastic Oscillator"""
        try:
            lowest_low = df['low'].rolling(window=k_period).min()
            highest_high = df['high'].rolling(window=k_period).max()
            
            df['stoch_k'] = 100 * ((df['close'] - lowest_low) / (highest_high - lowest_low))
            df['stoch_d'] = df['stoch_k'].rolling(window=d_period).mean()
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding Stochastic: {e}")
            return df
            
    def add_volume_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add volume-based indicators"""
        try:
            if 'tick_volume' in df.columns:
                # Volume Moving Average
                df['volume_sma'] = df['tick_volume'].rolling(window=20).mean()
                
                # On Balance Volume (OBV)
                df['obv'] = (np.sign(df['close'].diff()) * df['tick_volume']).fillna(0).cumsum()
                
                # Volume Rate of Change
                df['volume_roc'] = df['tick_volume'].pct_change(periods=10)
                
            return df
            
        except Exception as e:
            logger.error(f"Error adding volume indicators: {e}")
            return df
            
    def add_momentum_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add momentum indicators"""
        try:
            # Rate of Change
            df['roc_5'] = df['close'].pct_change(periods=5) * 100
            df['roc_10'] = df['close'].pct_change(periods=10) * 100
            
            # Momentum
            df['momentum'] = df['close'] - df['close'].shift(10)
            
            # Williams %R
            highest_high = df['high'].rolling(window=14).max()
            lowest_low = df['low'].rolling(window=14).min()
            df['williams_r'] = -100 * (highest_high - df['close']) / (highest_high - lowest_low)
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding momentum indicators: {e}")
            return df
            
    def add_volatility_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add volatility indicators"""
        try:
            # Historical Volatility
            returns = df['close'].pct_change()
            df['volatility_10'] = returns.rolling(window=10).std() * np.sqrt(252)
            df['volatility_20'] = returns.rolling(window=20).std() * np.sqrt(252)
            
            # Keltner Channels
            ema_20 = df['close'].ewm(span=20).mean()
            atr_10 = self._calculate_atr(df, 10)
            df['keltner_upper'] = ema_20 + (2 * atr_10)
            df['keltner_lower'] = ema_20 - (2 * atr_10)
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding volatility indicators: {e}")
            return df
            
    def _calculate_atr(self, df: pd.DataFrame, period: int) -> pd.Series:
        """Helper function to calculate ATR"""
        try:
            high_low = df['high'] - df['low']
            high_close = np.abs(df['high'] - df['close'].shift())
            low_close = np.abs(df['low'] - df['close'].shift())
            
            true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            return true_range.rolling(window=period).mean()
            
        except Exception as e:
            logger.error(f"Error calculating ATR: {e}")
            return pd.Series(index=df.index, data=0)
            
    def get_signal_strength(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate overall signal strength"""
        try:
            signals = pd.DataFrame(index=df.index)
            
            # RSI signals
            signals['rsi_oversold'] = (df['rsi'] < 30).astype(int)
            signals['rsi_overbought'] = (df['rsi'] > 70).astype(int)
            
            # MACD signals
            signals['macd_bullish'] = (df['macd'] > df['macd_signal']).astype(int)
            signals['macd_bearish'] = (df['macd'] < df['macd_signal']).astype(int)
            
            # Moving average signals
            signals['ma_bullish'] = (df['close'] > df['sma_20']).astype(int)
            signals['ma_bearish'] = (df['close'] < df['sma_20']).astype(int)
            
            # Bollinger Band signals
            signals['bb_oversold'] = (df['close'] < df['bb_lower']).astype(int)
            signals['bb_overbought'] = (df['close'] > df['bb_upper']).astype(int)
            
            # Overall bullish/bearish strength
            bullish_signals = ['rsi_oversold', 'macd_bullish', 'ma_bullish', 'bb_oversold']
            bearish_signals = ['rsi_overbought', 'macd_bearish', 'ma_bearish', 'bb_overbought']
            
            df['bullish_strength'] = signals[bullish_signals].sum(axis=1) / len(bullish_signals)
            df['bearish_strength'] = signals[bearish_signals].sum(axis=1) / len(bearish_signals)
            
            return df
            
        except Exception as e:
            logger.error(f"Error calculating signal strength: {e}")
            return df