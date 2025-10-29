"""
Mobile Trading Bot - Main Application
בוט מסחר נייד עם MT5 ו-AI
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from pathlib import Path

from mobile_trading_bot.api.routes import router
from mobile_trading_bot.core.config import settings
from mobile_trading_bot.core.logger import setup_logger

# Initialize logger
logger = setup_logger()

# Create FastAPI app
app = FastAPI(
    title="Mobile Trading Bot - MT5 + AI",
    description="בוט מסחר נייד עם אינטגרציה ל-MetaTrader 5 ו-AI",
    version="1.0.0"
)

# CORS middleware for mobile access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your mobile app domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

# Mount static files for mobile interface
static_path = Path(__file__).parent / "mobile_interface"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve mobile-friendly interface"""
    mobile_interface_path = Path(__file__).parent / "mobile_interface" / "index.html"
    if mobile_interface_path.exists():
        return FileResponse(mobile_interface_path)
    return HTMLResponse(content="<h1>Mobile Trading Bot - MT5 + AI</h1><p>בוט מסחר נייד</p>")


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("🚀 Starting Mobile Trading Bot...")
    logger.info("📱 MT5 + AI Trading Bot is ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down Mobile Trading Bot...")


if __name__ == "__main__":
    uvicorn.run(
        "mobile_trading_bot.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
