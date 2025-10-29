"""
AI Models for Trading Predictions
"""
import asyncio
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime
import joblib
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class BaseModel:
    """Base class for trading models"""
    
    def __init__(self, lookback_period: int = 60, prediction_horizon: int = 5):
        self.lookback_period = lookback_period
        self.prediction_horizon = prediction_horizon
        self.direction_model = None
        self.price_model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.performance_metrics = {}
        
    async def train(self, X: np.ndarray, y: np.ndarray) -> bool:
        """Train the model"""
        try:
            logger.info(f"Training {self.__class__.__name__} with {len(X)} samples")
            
            # Reshape X for sklearn models
            X_reshaped = X.reshape(X.shape[0], -1)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X_reshaped)
            
            # Split targets
            y_direction = y[:, 0]  # Direction (0 or 1)
            y_price = y[:, 1]      # Price change
            
            # Train direction model
            self.direction_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            self.direction_model.fit(X_scaled, y_direction)
            
            # Train price change model
            self.price_model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            self.price_model.fit(X_scaled, y_price)
            
            self.is_trained = True
            
            # Calculate performance metrics
            await self._calculate_performance(X_scaled, y_direction, y_price)
            
            logger.info(f"Model training completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            return False
            
    async def predict(self, X: np.ndarray) -> Optional[Dict]:
        """Make prediction"""
        try:
            if not self.is_trained:
                logger.warning("Model not trained yet")
                return None
                
            # Reshape and scale input
            X_reshaped = X.reshape(1, -1)
            X_scaled = self.scaler.transform(X_reshaped)
            
            # Predict direction probability
            direction_proba = self.direction_model.predict_proba(X_scaled)[0]
            direction_prob = direction_proba[1] if len(direction_proba) > 1 else 0.5
            
            # Predict price change
            price_change = self.price_model.predict(X_scaled)[0]
            
            return {
                'direction_prob': direction_prob,
                'price_change': price_change,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return None
            
    async def _calculate_performance(self, X: np.ndarray, y_direction: np.ndarray, y_price: np.ndarray):
        """Calculate model performance metrics"""
        try:
            # Direction predictions
            direction_pred = self.direction_model.predict(X)
            
            # Calculate metrics
            accuracy = accuracy_score(y_direction, direction_pred)
            precision = precision_score(y_direction, direction_pred, average='weighted', zero_division=0)
            recall = recall_score(y_direction, direction_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_direction, direction_pred, average='weighted', zero_division=0)
            
            # Price prediction error
            price_pred = self.price_model.predict(X)
            price_mse = np.mean((y_price - price_pred) ** 2)
            price_mae = np.mean(np.abs(y_price - price_pred))
            
            self.performance_metrics = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'price_mse': price_mse,
                'price_mae': price_mae,
                'last_updated': datetime.now()
            }
            
            logger.info(f"Model performance - Accuracy: {accuracy:.3f}, F1: {f1:.3f}")
            
        except Exception as e:
            logger.error(f"Error calculating performance: {e}")
            
    def save_model(self, filepath: str):
        """Save model to file"""
        try:
            model_data = {
                'direction_model': self.direction_model,
                'price_model': self.price_model,
                'scaler': self.scaler,
                'lookback_period': self.lookback_period,
                'prediction_horizon': self.prediction_horizon,
                'is_trained': self.is_trained,
                'performance_metrics': self.performance_metrics
            }
            
            joblib.dump(model_data, filepath)
            logger.info(f"Model saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            
    def load_model(self, filepath: str):
        """Load model from file"""
        try:
            model_data = joblib.load(filepath)
            
            self.direction_model = model_data['direction_model']
            self.price_model = model_data['price_model']
            self.scaler = model_data['scaler']
            self.lookback_period = model_data['lookback_period']
            self.prediction_horizon = model_data['prediction_horizon']
            self.is_trained = model_data['is_trained']
            self.performance_metrics = model_data.get('performance_metrics', {})
            
            logger.info(f"Model loaded from {filepath}")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            
    async def get_performance_metrics(self) -> Dict:
        """Get model performance metrics"""
        return self.performance_metrics.copy()

class LSTMModel(BaseModel):
    """LSTM-based trading model (using RandomForest as fallback)"""
    
    def __init__(self, lookback_period: int = 60, prediction_horizon: int = 5):
        super().__init__(lookback_period, prediction_horizon)
        self.model_type = "LSTM (RandomForest Implementation)"
        
    async def train(self, X: np.ndarray, y: np.ndarray) -> bool:
        """Train LSTM model (using RandomForest implementation)"""
        try:
            logger.info("Training LSTM model (RandomForest implementation)")
            
            # Use enhanced RandomForest for LSTM-like behavior
            X_reshaped = X.reshape(X.shape[0], -1)
            X_scaled = self.scaler.fit_transform(X_reshaped)
            
            y_direction = y[:, 0]
            y_price = y[:, 1]
            
            # Enhanced RandomForest with more trees for LSTM-like performance
            self.direction_model = RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            
            self.price_model = RandomForestRegressor(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            
            # Train models
            self.direction_model.fit(X_scaled, y_direction)
            self.price_model.fit(X_scaled, y_price)
            
            self.is_trained = True
            await self._calculate_performance(X_scaled, y_direction, y_price)
            
            return True
            
        except Exception as e:
            logger.error(f"Error training LSTM model: {e}")
            return False

class CNNModel(BaseModel):
    """CNN-based trading model (using RandomForest as fallback)"""
    
    def __init__(self, lookback_period: int = 60, prediction_horizon: int = 5):
        super().__init__(lookback_period, prediction_horizon)
        self.model_type = "CNN (RandomForest Implementation)"
        
    async def train(self, X: np.ndarray, y: np.ndarray) -> bool:
        """Train CNN model (using RandomForest implementation)"""
        try:
            logger.info("Training CNN model (RandomForest implementation)")
            
            # Use feature engineering for CNN-like pattern recognition
            X_features = self._extract_cnn_features(X)
            X_scaled = self.scaler.fit_transform(X_features)
            
            y_direction = y[:, 0]
            y_price = y[:, 1]
            
            # RandomForest with feature engineering for CNN-like behavior
            self.direction_model = RandomForestClassifier(
                n_estimators=150,
                max_depth=12,
                max_features='sqrt',
                random_state=42,
                n_jobs=-1
            )
            
            self.price_model = RandomForestRegressor(
                n_estimators=150,
                max_depth=12,
                max_features='sqrt',
                random_state=42,
                n_jobs=-1
            )
            
            # Train models
            self.direction_model.fit(X_scaled, y_direction)
            self.price_model.fit(X_scaled, y_price)
            
            self.is_trained = True
            await self._calculate_performance(X_scaled, y_direction, y_price)
            
            return True
            
        except Exception as e:
            logger.error(f"Error training CNN model: {e}")
            return False
            
    def _extract_cnn_features(self, X: np.ndarray) -> np.ndarray:
        """Extract CNN-like features from input data"""
        try:
            features = []
            
            for sample in X:
                sample_features = []
                
                # Flatten the sample
                flattened = sample.flatten()
                sample_features.extend(flattened)
                
                # Add statistical features (CNN-like pooling)
                sample_features.extend([
                    np.mean(sample, axis=0).mean(),
                    np.std(sample, axis=0).mean(),
                    np.max(sample, axis=0).mean(),
                    np.min(sample, axis=0).mean()
                ])
                
                # Add trend features
                if len(sample) > 1:
                    trends = np.diff(sample, axis=0)
                    sample_features.extend([
                        np.mean(trends),
                        np.std(trends),
                        np.sum(trends > 0) / len(trends)
                    ])
                else:
                    sample_features.extend([0, 0, 0])
                    
                features.append(sample_features)
                
            return np.array(features)
            
        except Exception as e:
            logger.error(f"Error extracting CNN features: {e}")
            return X.reshape(X.shape[0], -1)
            
    async def predict(self, X: np.ndarray) -> Optional[Dict]:
        """Make prediction with CNN features"""
        try:
            if not self.is_trained:
                return None
                
            # Extract CNN features
            X_features = self._extract_cnn_features(X.reshape(1, *X.shape))
            X_scaled = self.scaler.transform(X_features)
            
            # Predict
            direction_proba = self.direction_model.predict_proba(X_scaled)[0]
            direction_prob = direction_proba[1] if len(direction_proba) > 1 else 0.5
            
            price_change = self.price_model.predict(X_scaled)[0]
            
            return {
                'direction_prob': direction_prob,
                'price_change': price_change,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error making CNN prediction: {e}")
            return None