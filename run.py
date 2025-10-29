#!/usr/bin/env python3
"""
Quick Start Script for Mobile Trading Bot
תסריט הפעלה מהירה לבוט מסחר נייד
"""

import uvicorn
from mobile_trading_bot.core.config import settings

if __name__ == "__main__":
    print("🚀 Starting Mobile Trading Bot...")
    print(f"📱 Access on: http://{settings.HOST}:{settings.PORT}")
    print(f"🌐 For mobile: http://<your-ip>:{settings.PORT}")
    print("=" * 50)
    
    uvicorn.run(
        "mobile_trading_bot.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
