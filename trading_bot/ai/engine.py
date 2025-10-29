"""
AI Engine for Market Analysis and Trading Decisions
"""
import asyncio
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import joblib
import os

from .models import LSTMModel, CNNModel
from .indicators import TechnicalIndicators
from ..config.settings import AI_CONFIG

logger = logging.getLogger(__name__)

class AIEngine:
    """
    AI Engine for market analysis and trading predictions
    """
    
    def __init__(self):
        self.models = {}
        self.indicators = TechnicalIndicators()
        self.model_type = AI_CONFIG['model_type']
        self.lookback_period = AI_CONFIG['lookback_period']
        self.prediction_horizon = AI_CONFIG['prediction_horizon']
        self.confidence_threshold = AI_CONFIG['confidence_threshold']
        
        # Model paths
        self.model_dir = 'trading_bot/ai/saved_models'
        os.makedirs(self.model_dir, exist_ok=True)
        
    async def initialize(self):
        """Initialize AI models"""
        try:
            logger.info("Initializing AI Engine...")
            
            # Load or create models for each symbol
            symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD']  # Default symbols
            
            for symbol in symbols:
                await self._load_or_create_model(symbol)
                
            logger.info("AI Engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI Engine: {e}")
            raise
            
    async def _load_or_create_model(self, symbol: str):
        """Load existing model or create new one"""
        try:
            model_path = os.path.join(self.model_dir, f"{symbol}_{self.model_type}.joblib")
            
            if os.path.exists(model_path):
                # Load existing model
                logger.info(f"Loading existing model for {symbol}")
                if self.model_type == 'lstm':
                    self.models[symbol] = LSTMModel()
                    self.models[symbol].load_model(model_path)
                elif self.model_type == 'cnn':
                    self.models[symbol] = CNNModel()
                    self.models[symbol].load_model(model_path)
            else:
                # Create new model
                logger.info(f"Creating new model for {symbol}")
                if self.model_type == 'lstm':
                    self.models[symbol] = LSTMModel(
                        lookback_period=self.lookback_period,
                        prediction_horizon=self.prediction_horizon
                    )
                elif self.model_type == 'cnn':
                    self.models[symbol] = CNNModel(
                        lookback_period=self.lookback_period,
                        prediction_horizon=self.prediction_horizon
                    )
                    
        except Exception as e:
            logger.error(f"Error loading/creating model for {symbol}: {e}")
            
    async def predict(self, symbol: str, data: List[Dict]) -> Optional[Dict]:
        """Make prediction for a symbol"""
        try:
            if symbol not in self.models:
                await self._load_or_create_model(symbol)
                
            if symbol not in self.models:
                logger.error(f"No model available for {symbol}")
                return None
                
            # Convert data to DataFrame
            df = pd.DataFrame(data)
            df['time'] = pd.to_datetime(df['time'])
            df.set_index('time', inplace=True)
            
            # Add technical indicators
            df = self.indicators.add_all_indicators(df)
            
            # Check if we have enough data
            if len(df) < self.lookback_period:
                logger.warning(f"Not enough data for prediction: {len(df)} < {self.lookback_period}")
                return None
                
            # Prepare features
            features = self._prepare_features(df)
            
            # Make prediction
            model = self.models[symbol]
            prediction = await model.predict(features)
            
            if prediction is None:
                return None
                
            # Interpret prediction
            result = self._interpret_prediction(prediction, df)
            
            return result
            
        except Exception as e:
            logger.error(f"Error making prediction for {symbol}: {e}")
            return None
            
    def _prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """Prepare features for model input"""
        try:
            # Select feature columns
            feature_columns = [
                'open', 'high', 'low', 'close', 'tick_volume',
                'sma_20', 'sma_50', 'ema_12', 'ema_26',
                'rsi', 'macd', 'macd_signal', 'macd_histogram',
                'bb_upper', 'bb_middle', 'bb_lower',
                'atr', 'stoch_k', 'stoch_d'
            ]
            
            # Filter available columns
            available_columns = [col for col in feature_columns if col in df.columns]
            
            if len(available_columns) == 0:
                logger.error("No feature columns available")
                return None
                
            # Get last lookback_period rows
            features = df[available_columns].tail(self.lookback_period).values
            
            # Handle NaN values
            features = np.nan_to_num(features, nan=0.0)
            
            # Normalize features (simple min-max scaling)
            features = self._normalize_features(features)
            
            return features
            
        except Exception as e:
            logger.error(f"Error preparing features: {e}")
            return None
            
    def _normalize_features(self, features: np.ndarray) -> np.ndarray:
        """Simple feature normalization"""
        try:
            # Min-max normalization
            min_vals = np.min(features, axis=0)
            max_vals = np.max(features, axis=0)
            
            # Avoid division by zero
            range_vals = max_vals - min_vals
            range_vals[range_vals == 0] = 1
            
            normalized = (features - min_vals) / range_vals
            
            return normalized
            
        except Exception as e:
            logger.error(f"Error normalizing features: {e}")
            return features
            
    def _interpret_prediction(self, prediction: Dict, df: pd.DataFrame) -> Dict:
        """Interpret model prediction"""
        try:
            # Get prediction values
            direction_prob = prediction.get('direction_prob', 0.5)
            price_change = prediction.get('price_change', 0.0)
            
            # Determine direction
            if direction_prob > 0.6:
                direction = 'buy'
                confidence = direction_prob
            elif direction_prob < 0.4:
                direction = 'sell'
                confidence = 1 - direction_prob
            else:
                direction = 'hold'
                confidence = 0.5
                
            # Calculate additional metrics
            current_price = df['close'].iloc[-1]
            volatility = df['close'].pct_change().std()
            
            # Adjust confidence based on volatility and other factors
            adjusted_confidence = self._adjust_confidence(confidence, volatility, df)
            
            return {
                'direction': direction,
                'confidence': adjusted_confidence,
                'raw_confidence': confidence,
                'price_change': price_change,
                'current_price': current_price,
                'volatility': volatility,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error interpreting prediction: {e}")
            return {
                'direction': 'hold',
                'confidence': 0.0,
                'error': str(e),
                'timestamp': datetime.now()
            }
            
    def _adjust_confidence(self, confidence: float, volatility: float, df: pd.DataFrame) -> float:
        """Adjust confidence based on market conditions"""
        try:
            # Reduce confidence in high volatility
            if volatility > 0.02:  # 2% volatility threshold
                confidence *= 0.8
                
            # Check trend strength
            sma_20 = df['sma_20'].iloc[-1] if 'sma_20' in df.columns else df['close'].iloc[-1]
            sma_50 = df['sma_50'].iloc[-1] if 'sma_50' in df.columns else df['close'].iloc[-1]
            
            if abs(sma_20 - sma_50) / sma_50 < 0.001:  # Weak trend
                confidence *= 0.9
                
            # Check RSI for overbought/oversold
            if 'rsi' in df.columns:
                rsi = df['rsi'].iloc[-1]
                if rsi > 80 or rsi < 20:  # Extreme RSI
                    confidence *= 1.1  # Increase confidence for reversal
                    
            # Ensure confidence stays in valid range
            confidence = max(0.0, min(1.0, confidence))
            
            return confidence
            
        except Exception as e:
            logger.error(f"Error adjusting confidence: {e}")
            return confidence
            
    async def train_model(self, symbol: str, historical_data: List[Dict]) -> bool:
        """Train or retrain model with historical data"""
        try:
            logger.info(f"Training model for {symbol}")
            
            if symbol not in self.models:
                await self._load_or_create_model(symbol)
                
            # Convert data to DataFrame
            df = pd.DataFrame(historical_data)
            df['time'] = pd.to_datetime(df['time'])
            df.set_index('time', inplace=True)
            
            # Add technical indicators
            df = self.indicators.add_all_indicators(df)
            
            # Prepare training data
            X, y = self._prepare_training_data(df)
            
            if X is None or y is None:
                logger.error(f"Failed to prepare training data for {symbol}")
                return False
                
            # Train model
            model = self.models[symbol]
            success = await model.train(X, y)
            
            if success:
                # Save model
                model_path = os.path.join(self.model_dir, f"{symbol}_{self.model_type}.joblib")
                model.save_model(model_path)
                logger.info(f"Model trained and saved for {symbol}")
                
            return success
            
        except Exception as e:
            logger.error(f"Error training model for {symbol}: {e}")
            return False
            
    def _prepare_training_data(self, df: pd.DataFrame) -> tuple:
        """Prepare training data from historical data"""
        try:
            # Prepare features
            feature_columns = [
                'open', 'high', 'low', 'close', 'tick_volume',
                'sma_20', 'sma_50', 'ema_12', 'ema_26',
                'rsi', 'macd', 'macd_signal', 'macd_histogram',
                'bb_upper', 'bb_middle', 'bb_lower',
                'atr', 'stoch_k', 'stoch_d'
            ]
            
            available_columns = [col for col in feature_columns if col in df.columns]
            
            if len(available_columns) == 0:
                return None, None
                
            # Create sequences
            X, y = [], []
            
            for i in range(self.lookback_period, len(df) - self.prediction_horizon):
                # Features: lookback_period rows
                features = df[available_columns].iloc[i-self.lookback_period:i].values
                features = np.nan_to_num(features, nan=0.0)
                features = self._normalize_features(features)
                X.append(features)
                
                # Target: price direction and change
                current_price = df['close'].iloc[i]
                future_price = df['close'].iloc[i + self.prediction_horizon]
                
                # Direction (1 for up, 0 for down)
                direction = 1 if future_price > current_price else 0
                
                # Price change percentage
                price_change = (future_price - current_price) / current_price
                
                y.append([direction, price_change])
                
            return np.array(X), np.array(y)
            
        except Exception as e:
            logger.error(f"Error preparing training data: {e}")
            return None, None
            
    async def get_model_performance(self, symbol: str) -> Optional[Dict]:
        """Get model performance metrics"""
        try:
            if symbol not in self.models:
                return None
                
            model = self.models[symbol]
            return await model.get_performance_metrics()
            
        except Exception as e:
            logger.error(f"Error getting model performance for {symbol}: {e}")
            return None