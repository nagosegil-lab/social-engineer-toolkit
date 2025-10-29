"""
AI Prediction Module for Trading
מודול חיזוי AI למסחר
"""

import numpy as np
import pandas as pd
from typing import Optional, Dict, Tuple
from pathlib import Path
import pickle
from mobile_trading_bot.core.logger import setup_logger
from mobile_trading_bot.core.config import settings

logger = setup_logger(__name__)

try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("scikit-learn not available, AI features limited")


class AIPredictor:
    """AI-based trading signal predictor"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler() if SKLEARN_AVAILABLE else None
        self.is_trained = False
        self.model_path = Path(settings.AI_MODEL_PATH)
        self.model_path.mkdir(parents=True, exist_ok=True)
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create technical features from price data
        יצירת מאפיינים טכניים מנתוני מחיר
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with features
        """
        features = pd.DataFrame(index=df.index)
        
        # Price features
        features['close'] = df['close']
        features['high'] = df['high']
        features['low'] = df['low']
        features['volume'] = df['tick_volume']
        
        # Returns
        features['returns'] = df['close'].pct_change()
        features['returns_5'] = df['close'].pct_change(5)
        features['returns_20'] = df['close'].pct_change(20)
        
        # Moving averages
        features['sma_5'] = df['close'].rolling(window=5).mean()
        features['sma_20'] = df['close'].rolling(window=20).mean()
        features['sma_50'] = df['close'].rolling(window=50).mean()
        
        # Price vs MA
        features['price_vs_sma5'] = (df['close'] - features['sma_5']) / features['sma_5']
        features['price_vs_sma20'] = (df['close'] - features['sma_20']) / features['sma_20']
        
        # Volatility
        features['volatility'] = df['close'].rolling(window=20).std()
        features['atr'] = self._calculate_atr(df, period=14)
        
        # RSI-like momentum
        features['momentum'] = df['close'].diff(14) / df['close'].shift(14)
        
        # Drop NaN rows
        features = features.dropna()
        
        return features
    
    def _calculate_atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        
        return true_range.rolling(window=period).mean()
    
    def create_target(self, df: pd.DataFrame, forward_periods: int = 5) -> pd.Series:
        """
        Create target labels (1 for buy, 0 for sell)
        יצירת תוויות יעד (1 לקנייה, 0 למכירה)
        
        Args:
            df: DataFrame with price data
            forward_periods: Number of periods ahead to predict
            
        Returns:
            Series with target labels
        """
        future_returns = df['close'].shift(-forward_periods) / df['close'] - 1
        target = (future_returns > 0).astype(int)
        return target
    
    def train(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Train the AI model
        אימון מודל AI
        
        Args:
            df: Historical price data
            
        Returns:
            Dictionary with training metrics
        """
        if not SKLEARN_AVAILABLE:
            logger.error("scikit-learn not available, cannot train model")
            return {}
        
        try:
            # Create features and target
            features_df = self.create_features(df)
            target = self.create_target(df)
            
            # Align indices
            common_index = features_df.index.intersection(target.index)
            X = features_df.loc[common_index].values
            y = target.loc[common_index].values
            
            if len(X) == 0:
                logger.error("No valid data for training")
                return {}
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model (using Gradient Boosting for better performance)
            self.model = GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
            
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate
            train_score = self.model.score(X_train_scaled, y_train)
            test_score = self.model.score(X_test_scaled, y_test)
            
            self.is_trained = True
            
            # Save model
            self.save_model()
            
            logger.info(f"✅ Model trained - Train: {train_score:.3f}, Test: {test_score:.3f}")
            
            return {
                "train_accuracy": float(train_score),
                "test_accuracy": float(test_score),
                "samples": len(X)
            }
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return {}
    
    def predict(self, df: pd.DataFrame) -> Optional[Dict[str, float]]:
        """
        Predict trading signal
        חיזוי אות מסחר
        
        Args:
            df: Current market data
            
        Returns:
            Dictionary with prediction confidence and signal
        """
        if not self.is_trained or self.model is None:
            logger.warning("Model not trained, using default prediction")
            return {
                "signal": "HOLD",
                "confidence": 0.5,
                "buy_probability": 0.5
            }
        
        try:
            # Create features
            features_df = self.create_features(df)
            
            if len(features_df) == 0:
                return None
            
            # Get latest features
            latest_features = features_df.iloc[-1:].values
            
            # Scale
            latest_features_scaled = self.scaler.transform(latest_features)
            
            # Predict
            prediction = self.model.predict(latest_features_scaled)[0]
            probabilities = self.model.predict_proba(latest_features_scaled)[0]
            
            buy_probability = probabilities[1] if len(probabilities) > 1 else 0.5
            
            # Determine signal
            if buy_probability > (0.5 + settings.AI_CONFIDENCE_THRESHOLD / 2):
                signal = "BUY"
            elif buy_probability < (0.5 - settings.AI_CONFIDENCE_THRESHOLD / 2):
                signal = "SELL"
            else:
                signal = "HOLD"
            
            confidence = abs(buy_probability - 0.5) * 2  # Normalize to 0-1
            
            return {
                "signal": signal,
                "confidence": float(confidence),
                "buy_probability": float(buy_probability),
                "prediction": int(prediction)
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            return None
    
    def save_model(self) -> bool:
        """Save trained model to disk"""
        try:
            if self.model is not None:
                model_file = self.model_path / "trading_model.pkl"
                scaler_file = self.model_path / "scaler.pkl"
                
                with open(model_file, 'wb') as f:
                    pickle.dump(self.model, f)
                
                if self.scaler is not None:
                    with open(scaler_file, 'wb') as f:
                        pickle.dump(self.scaler, f)
                
                logger.info(f"Model saved to {model_file}")
                return True
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
        
        return False
    
    def load_model(self) -> bool:
        """Load trained model from disk"""
        try:
            model_file = self.model_path / "trading_model.pkl"
            scaler_file = self.model_path / "scaler.pkl"
            
            if not model_file.exists():
                return False
            
            with open(model_file, 'rb') as f:
                self.model = pickle.load(f)
            
            if scaler_file.exists():
                with open(scaler_file, 'rb') as f:
                    self.scaler = pickle.load(f)
            
            self.is_trained = True
            logger.info("Model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False
