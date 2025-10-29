"""
AI-powered market analyzer for trading decisions
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import ta
import joblib
import logging
from datetime import datetime, timedelta
import os
from config import Config

class AIAnalyzer:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = []
        self.logger = logging.getLogger(__name__)
        self.model_path = Config.MODEL_PATH
        
        # Create models directory if it doesn't exist
        os.makedirs(self.model_path, exist_ok=True)
        
    def prepare_features(self, df):
        """Prepare technical indicators and features for ML model"""
        try:
            # Technical indicators
            df['sma_20'] = ta.trend.sma_indicator(df['close'], window=20)
            df['sma_50'] = ta.trend.sma_indicator(df['close'], window=50)
            df['ema_12'] = ta.trend.ema_indicator(df['close'], window=12)
            df['ema_26'] = ta.trend.ema_indicator(df['close'], window=26)
            
            # MACD
            macd = ta.trend.MACD(df['close'])
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
            df['macd_histogram'] = macd.macd_diff()
            
            # RSI
            df['rsi'] = ta.momentum.rsi(df['close'], window=14)
            
            # Bollinger Bands
            bb = ta.volatility.BollingerBands(df['close'])
            df['bb_upper'] = bb.bollinger_hband()
            df['bb_lower'] = bb.bollinger_lband()
            df['bb_middle'] = bb.bollinger_mavg()
            df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']
            
            # Stochastic
            stoch = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'])
            df['stoch_k'] = stoch.stoch()
            df['stoch_d'] = stoch.stoch_signal()
            
            # ATR
            df['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'])
            
            # Volume indicators
            df['volume_sma'] = ta.volume.volume_sma(df['close'], df['volume'])
            df['volume_ratio'] = df['volume'] / df['volume_sma']
            
            # Price patterns
            df['price_change'] = df['close'].pct_change()
            df['high_low_ratio'] = df['high'] / df['low']
            df['close_open_ratio'] = df['close'] / df['open']
            
            # Moving average crossovers
            df['sma_cross'] = np.where(df['sma_20'] > df['sma_50'], 1, 0)
            df['ema_cross'] = np.where(df['ema_12'] > df['ema_26'], 1, 0)
            
            # Price position relative to Bollinger Bands
            df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
            
            # Define feature columns
            self.feature_columns = [
                'sma_20', 'sma_50', 'ema_12', 'ema_26',
                'macd', 'macd_signal', 'macd_histogram',
                'rsi', 'bb_upper', 'bb_lower', 'bb_middle', 'bb_width',
                'stoch_k', 'stoch_d', 'atr', 'volume_ratio',
                'price_change', 'high_low_ratio', 'close_open_ratio',
                'sma_cross', 'ema_cross', 'bb_position'
            ]
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error preparing features: {e}")
            return None
    
    def create_labels(self, df, lookforward=5):
        """Create trading labels based on future price movements"""
        try:
            # Calculate future returns
            future_returns = df['close'].shift(-lookforward) / df['close'] - 1
            
            # Create labels: 1 for buy, 0 for hold, -1 for sell
            labels = np.where(future_returns > 0.001, 1,  # Buy if > 0.1% gain
                            np.where(future_returns < -0.001, -1, 0))  # Sell if > 0.1% loss
            
            return labels
            
        except Exception as e:
            self.logger.error(f"Error creating labels: {e}")
            return None
    
    def train_model(self, df):
        """Train the AI model"""
        try:
            # Prepare features
            df_with_features = self.prepare_features(df.copy())
            if df_with_features is None:
                return False
            
            # Create labels
            labels = self.create_labels(df_with_features)
            if labels is None:
                return False
            
            # Prepare data
            feature_data = df_with_features[self.feature_columns].dropna()
            labels = labels[~df_with_features[self.feature_columns].isna().any(axis=1)]
            
            if len(feature_data) == 0:
                self.logger.error("No valid data for training")
                return False
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                feature_data, labels, test_size=0.2, random_state=42
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model (using Random Forest for better interpretability)
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                class_weight='balanced'
            )
            
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)
            
            self.logger.info(f"Model trained with accuracy: {accuracy:.4f}")
            
            # Save model
            self.save_model()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error training model: {e}")
            return False
    
    def predict(self, df):
        """Make trading predictions"""
        try:
            if self.model is None:
                self.logger.error("Model not trained")
                return None
            
            # Prepare features
            df_with_features = self.prepare_features(df.copy())
            if df_with_features is None:
                return None
            
            # Get latest features
            latest_features = df_with_features[self.feature_columns].iloc[-1:].dropna()
            
            if latest_features.empty:
                self.logger.error("No valid features for prediction")
                return None
            
            # Scale features
            features_scaled = self.scaler.transform(latest_features)
            
            # Make prediction
            prediction = self.model.predict(features_scaled)[0]
            probabilities = self.model.predict_proba(features_scaled)[0]
            
            # Get feature importance
            feature_importance = dict(zip(self.feature_columns, self.model.feature_importances_))
            
            return {
                'prediction': prediction,
                'probabilities': probabilities,
                'confidence': max(probabilities),
                'feature_importance': feature_importance
            }
            
        except Exception as e:
            self.logger.error(f"Error making prediction: {e}")
            return None
    
    def save_model(self):
        """Save trained model and scaler"""
        try:
            if self.model is not None:
                joblib.dump(self.model, os.path.join(self.model_path, 'trading_model.pkl'))
                joblib.dump(self.scaler, os.path.join(self.model_path, 'scaler.pkl'))
                joblib.dump(self.feature_columns, os.path.join(self.model_path, 'feature_columns.pkl'))
                self.logger.info("Model saved successfully")
                
        except Exception as e:
            self.logger.error(f"Error saving model: {e}")
    
    def load_model(self):
        """Load trained model and scaler"""
        try:
            model_file = os.path.join(self.model_path, 'trading_model.pkl')
            scaler_file = os.path.join(self.model_path, 'scaler.pkl')
            features_file = os.path.join(self.model_path, 'feature_columns.pkl')
            
            if all(os.path.exists(f) for f in [model_file, scaler_file, features_file]):
                self.model = joblib.load(model_file)
                self.scaler = joblib.load(scaler_file)
                self.feature_columns = joblib.load(features_file)
                self.logger.info("Model loaded successfully")
                return True
            else:
                self.logger.warning("Model files not found")
                return False
                
        except Exception as e:
            self.logger.error(f"Error loading model: {e}")
            return False
    
    def get_market_sentiment(self, df):
        """Analyze market sentiment based on multiple indicators"""
        try:
            # RSI sentiment
            rsi = ta.momentum.rsi(df['close'], window=14).iloc[-1]
            rsi_sentiment = 'overbought' if rsi > 70 else 'oversold' if rsi < 30 else 'neutral'
            
            # MACD sentiment
            macd = ta.trend.MACD(df['close'])
            macd_line = macd.macd().iloc[-1]
            macd_signal = macd.macd_signal().iloc[-1]
            macd_sentiment = 'bullish' if macd_line > macd_signal else 'bearish'
            
            # Moving average sentiment
            sma_20 = ta.trend.sma_indicator(df['close'], window=20).iloc[-1]
            sma_50 = ta.trend.sma_indicator(df['close'], window=50).iloc[-1]
            ma_sentiment = 'bullish' if sma_20 > sma_50 else 'bearish'
            
            # Bollinger Bands sentiment
            bb = ta.volatility.BollingerBands(df['close'])
            bb_upper = bb.bollinger_hband().iloc[-1]
            bb_lower = bb.bollinger_lband().iloc[-1]
            current_price = df['close'].iloc[-1]
            
            if current_price > bb_upper:
                bb_sentiment = 'overbought'
            elif current_price < bb_lower:
                bb_sentiment = 'oversold'
            else:
                bb_sentiment = 'neutral'
            
            return {
                'rsi': {'value': rsi, 'sentiment': rsi_sentiment},
                'macd': {'sentiment': macd_sentiment},
                'moving_average': {'sentiment': ma_sentiment},
                'bollinger_bands': {'sentiment': bb_sentiment},
                'overall_sentiment': self._calculate_overall_sentiment(
                    rsi_sentiment, macd_sentiment, ma_sentiment, bb_sentiment
                )
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing market sentiment: {e}")
            return None
    
    def _calculate_overall_sentiment(self, rsi, macd, ma, bb):
        """Calculate overall market sentiment"""
        bullish_count = sum([1 for sentiment in [rsi, macd, ma, bb] if 'bullish' in sentiment or 'oversold' in sentiment])
        bearish_count = sum([1 for sentiment in [rsi, macd, ma, bb] if 'bearish' in sentiment or 'overbought' in sentiment])
        
        if bullish_count > bearish_count:
            return 'bullish'
        elif bearish_count > bullish_count:
            return 'bearish'
        else:
            return 'neutral'