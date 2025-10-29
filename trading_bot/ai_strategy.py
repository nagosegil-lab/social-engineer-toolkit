"""
AI Trading Strategy Module
Implements machine learning models for trade predictions
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
from datetime import datetime
import logging
from typing import Tuple, Optional, Dict
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TechnicalIndicators:
    """Calculate technical indicators"""
    
    @staticmethod
    def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate MACD"""
        ema_fast = data.ewm(span=fast).mean()
        ema_slow = data.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal).mean()
        macd_hist = macd - macd_signal
        return macd, macd_signal, macd_hist
    
    @staticmethod
    def calculate_bollinger_bands(data: pd.Series, period: int = 20, std_dev: int = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate Bollinger Bands"""
        sma = data.rolling(window=period).mean()
        std = data.rolling(window=period).std()
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return upper_band, sma, lower_band
    
    @staticmethod
    def calculate_ema(data: pd.Series, period: int = 20) -> pd.Series:
        """Calculate Exponential Moving Average"""
        return data.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def calculate_sma(data: pd.Series, period: int = 20) -> pd.Series:
        """Calculate Simple Moving Average"""
        return data.rolling(window=period).mean()
    
    @staticmethod
    def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr


class AITradingStrategy:
    """AI-powered trading strategy"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = 'trading_bot/models/'
        self.indicators = TechnicalIndicators()
        
        # Create models directory if it doesn't exist
        os.makedirs(self.model_path, exist_ok=True)
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for the model"""
        features_df = df.copy()
        
        # Calculate technical indicators
        features_df['rsi'] = self.indicators.calculate_rsi(df['close'])
        
        macd, macd_signal, macd_hist = self.indicators.calculate_macd(df['close'])
        features_df['macd'] = macd
        features_df['macd_signal'] = macd_signal
        features_df['macd_hist'] = macd_hist
        
        bb_upper, bb_middle, bb_lower = self.indicators.calculate_bollinger_bands(df['close'])
        features_df['bb_upper'] = bb_upper
        features_df['bb_middle'] = bb_middle
        features_df['bb_lower'] = bb_lower
        features_df['bb_width'] = bb_upper - bb_lower
        
        features_df['ema_20'] = self.indicators.calculate_ema(df['close'], 20)
        features_df['ema_50'] = self.indicators.calculate_ema(df['close'], 50)
        features_df['sma_20'] = self.indicators.calculate_sma(df['close'], 20)
        features_df['sma_50'] = self.indicators.calculate_sma(df['close'], 50)
        
        features_df['atr'] = self.indicators.calculate_atr(df['high'], df['low'], df['close'])
        
        # Price-based features
        features_df['price_change'] = df['close'].pct_change()
        features_df['high_low_ratio'] = df['high'] / df['low']
        features_df['close_open_ratio'] = df['close'] / df['open']
        
        # Volume features (if available)
        if 'volume' in df.columns:
            features_df['volume_change'] = df['volume'].pct_change()
            features_df['volume_ma'] = df['volume'].rolling(window=20).mean()
        
        # Momentum
        features_df['momentum'] = df['close'] - df['close'].shift(4)
        
        # Remove rows with NaN values
        features_df = features_df.dropna()
        
        return features_df
    
    def create_labels(self, df: pd.DataFrame, forward_periods: int = 5) -> pd.Series:
        """Create labels for supervised learning (1 = BUY, 0 = HOLD, -1 = SELL)"""
        future_close = df['close'].shift(-forward_periods)
        price_change = (future_close - df['close']) / df['close']
        
        # Define thresholds for buy/sell signals
        buy_threshold = 0.002  # 0.2% gain
        sell_threshold = -0.002  # 0.2% loss
        
        labels = pd.Series(0, index=df.index)
        labels[price_change > buy_threshold] = 1  # BUY
        labels[price_change < sell_threshold] = -1  # SELL
        
        return labels
    
    def train_model(self, df: pd.DataFrame) -> Tuple[float, float]:
        """Train the AI model"""
        logger.info("Training AI model...")
        
        # Prepare features
        features_df = self.prepare_features(df)
        labels = self.create_labels(features_df)
        
        # Align features and labels
        common_index = features_df.index.intersection(labels.index)
        features_df = features_df.loc[common_index]
        labels = labels.loc[common_index]
        
        # Remove target-related columns
        feature_cols = [col for col in features_df.columns if col not in ['time', 'tick_volume', 'spread', 'real_volume']]
        X = features_df[feature_cols]
        y = labels
        
        # Remove any remaining NaN
        mask = ~(X.isna().any(axis=1) | y.isna())
        X = X[mask]
        y = y[mask]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model based on config
        if self.config.get('model_type') == 'gradient_boosting':
            self.model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        else:  # default to random forest
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        logger.info(f"Model trained. Train accuracy: {train_score:.3f}, Test accuracy: {test_score:.3f}")
        
        # Save model
        self.save_model()
        
        return train_score, test_score
    
    def predict(self, df: pd.DataFrame) -> Optional[Dict]:
        """Predict trading signal"""
        if self.model is None:
            logger.warning("Model not trained yet")
            return None
        
        # Prepare features
        features_df = self.prepare_features(df)
        
        if len(features_df) == 0:
            return None
        
        # Get last row
        feature_cols = [col for col in features_df.columns if col not in ['time', 'tick_volume', 'spread', 'real_volume']]
        X = features_df[feature_cols].iloc[-1:].values
        
        # Scale and predict
        X_scaled = self.scaler.transform(X)
        prediction = self.model.predict(X_scaled)[0]
        probabilities = self.model.predict_proba(X_scaled)[0]
        
        # Get confidence
        confidence = max(probabilities)
        
        signal_map = {-1: 'SELL', 0: 'HOLD', 1: 'BUY'}
        signal = signal_map.get(prediction, 'HOLD')
        
        # Only return signal if confidence is above threshold
        threshold = self.config.get('prediction_threshold', 0.6)
        if confidence < threshold:
            signal = 'HOLD'
        
        return {
            'signal': signal,
            'confidence': confidence,
            'prediction': int(prediction),
            'timestamp': datetime.now()
        }
    
    def save_model(self):
        """Save model and scaler"""
        model_file = os.path.join(self.model_path, 'model.pkl')
        scaler_file = os.path.join(self.model_path, 'scaler.pkl')
        
        joblib.dump(self.model, model_file)
        joblib.dump(self.scaler, scaler_file)
        logger.info(f"Model saved to {model_file}")
    
    def load_model(self) -> bool:
        """Load saved model and scaler"""
        model_file = os.path.join(self.model_path, 'model.pkl')
        scaler_file = os.path.join(self.model_path, 'scaler.pkl')
        
        if not os.path.exists(model_file) or not os.path.exists(scaler_file):
            logger.warning("Model files not found")
            return False
        
        try:
            self.model = joblib.load(model_file)
            self.scaler = joblib.load(scaler_file)
            logger.info("Model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
