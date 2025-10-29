"""
API Routes for Mobile Trading Bot
נתיבי API לבוט מסחר נייד
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import datetime

from mobile_trading_bot.mt5.connection import MT5Connection, mt5_connection
from mobile_trading_bot.mt5.trading import MT5Trading, OrderType
from mobile_trading_bot.mt5.data import MT5Data
from mobile_trading_bot.ai.predictor import AIPredictor
from mobile_trading_bot.ai.analyzer import MarketAnalyzer
from mobile_trading_bot.core.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()

# Initialize services
mt5_trading = MT5Trading()
mt5_data = MT5Data()
ai_predictor = AIPredictor()
market_analyzer = MarketAnalyzer()


# Pydantic models for requests/responses
class MT5ConnectionRequest(BaseModel):
    login: Optional[int] = None
    password: Optional[str] = None
    server: Optional[str] = None
    path: Optional[str] = None


class PlaceOrderRequest(BaseModel):
    symbol: str
    order_type: str  # "BUY" or "SELL"
    volume: float
    price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    comment: str = "Mobile Trading Bot"


class TrainModelRequest(BaseModel):
    symbol: str
    timeframe: Optional[int] = None
    periods: Optional[int] = 1000


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "mt5_connected": mt5_connection.is_connected(),
        "timestamp": datetime.now().isoformat()
    }


@router.post("/mt5/connect")
async def connect_mt5(request: MT5ConnectionRequest):
    """Connect to MT5"""
    try:
        success = mt5_connection.connect(
            login=request.login,
            password=request.password,
            server=request.server,
            path=request.path
        )
        
        if success:
            account_info = mt5_connection.get_account_info()
            return {
                "success": True,
                "message": "Connected to MT5",
                "account_info": account_info
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to connect to MT5")
            
    except Exception as e:
        logger.error(f"Connection error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mt5/account")
async def get_account_info():
    """Get MT5 account information"""
    if not mt5_connection.is_connected():
        raise HTTPException(status_code=400, detail="Not connected to MT5")
    
    account_info = mt5_connection.get_account_info()
    if account_info:
        return account_info
    raise HTTPException(status_code=404, detail="Account info not available")


@router.get("/mt5/symbols/{symbol}")
async def get_symbol_info(symbol: str):
    """Get symbol information"""
    info = mt5_data.get_symbol_info(symbol)
    if info:
        return info
    raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found")


@router.get("/mt5/price/{symbol}")
async def get_current_price(symbol: str):
    """Get current price for symbol"""
    price = mt5_data.get_current_price(symbol)
    if price:
        return price
    raise HTTPException(status_code=404, detail=f"Price for {symbol} not available")


@router.get("/mt5/positions")
async def get_positions(symbol: Optional[str] = None):
    """Get open positions"""
    positions = mt5_data.get_positions(symbol=symbol)
    return {"positions": positions, "count": len(positions)}


@router.get("/mt5/orders")
async def get_orders():
    """Get pending orders"""
    orders = mt5_data.get_orders()
    return {"orders": orders, "count": len(orders)}


@router.post("/mt5/order")
async def place_order(request: PlaceOrderRequest):
    """Place a trading order"""
    try:
        # Map order type string to enum
        order_type_map = {
            "BUY": OrderType.BUY,
            "SELL": OrderType.SELL,
            "BUY_LIMIT": OrderType.BUY_LIMIT,
            "SELL_LIMIT": OrderType.SELL_LIMIT,
        }
        
        order_type = order_type_map.get(request.order_type.upper())
        if order_type is None:
            raise HTTPException(status_code=400, detail=f"Invalid order type: {request.order_type}")
        
        result = mt5_trading.place_order(
            symbol=request.symbol,
            order_type=order_type,
            volume=request.volume,
            price=request.price,
            sl=request.stop_loss,
            tp=request.take_profit,
            comment=request.comment
        )
        
        if result:
            return result
        else:
            raise HTTPException(status_code=500, detail="Failed to place order")
            
    except Exception as e:
        logger.error(f"Order placement error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mt5/close/{ticket}")
async def close_position(ticket: int):
    """Close a position"""
    result = mt5_trading.close_position(ticket)
    if result:
        return result
    raise HTTPException(status_code=500, detail="Failed to close position")


@router.get("/ai/predict/{symbol}")
async def get_ai_prediction(symbol: str, timeframe: Optional[int] = None):
    """Get AI prediction for symbol"""
    try:
        # Load model if not loaded
        if not ai_predictor.is_trained:
            ai_predictor.load_model()
        
        # Get market data
        df = mt5_data.get_rates(symbol, count=200)
        if df is None or len(df) == 0:
            raise HTTPException(status_code=404, detail=f"No data available for {symbol}")
        
        # Get prediction
        prediction = ai_predictor.predict(df)
        if prediction:
            # Also get market analysis
            analysis = market_analyzer.analyze_market(df)
            prediction["analysis"] = analysis
            return prediction
        
        raise HTTPException(status_code=500, detail="Prediction failed")
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ai/train")
async def train_ai_model(request: TrainModelRequest):
    """Train AI model with historical data"""
    try:
        # Get historical data
        df = mt5_data.get_rates(request.symbol, count=request.periods or 1000)
        if df is None or len(df) == 0:
            raise HTTPException(status_code=404, detail=f"No data available for {request.symbol}")
        
        # Train model
        metrics = ai_predictor.train(df)
        if metrics:
            return {
                "success": True,
                "message": "Model trained successfully",
                "metrics": metrics
            }
        
        raise HTTPException(status_code=500, detail="Training failed")
        
    except Exception as e:
        logger.error(f"Training error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/{symbol}")
async def get_market_analysis(symbol: str):
    """Get comprehensive market analysis"""
    try:
        df = mt5_data.get_rates(symbol, count=200)
        if df is None or len(df) == 0:
            raise HTTPException(status_code=404, detail=f"No data available for {symbol}")
        
        analysis = market_analyzer.analyze_market(df)
        return analysis
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
