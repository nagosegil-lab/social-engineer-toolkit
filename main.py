#!/usr/bin/env python3
"""
Mobile Trading Bot with MT5 and AI Integration
Main Application Entry Point
"""
import asyncio
import logging
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from trading_bot.web.app import create_app
from trading_bot.config.settings import WEB_CONFIG, LOGGING_CONFIG

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG['level']),
    format=LOGGING_CONFIG['format'],
    handlers=[
        logging.FileHandler(LOGGING_CONFIG['file']),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main application entry point"""
    try:
        logger.info("🚀 Starting Mobile Trading Bot...")
        
        # Create Flask app and SocketIO
        app, socketio = create_app()
        
        # Print startup information
        print("\n" + "="*60)
        print("🤖 MOBILE TRADING BOT - MT5 + AI")
        print("="*60)
        print(f"📱 Web Interface: http://{WEB_CONFIG['host']}:{WEB_CONFIG['port']}")
        print(f"🔐 Default Password: trading123 (CHANGE THIS!)")
        print(f"📊 Features:")
        print(f"   • MetaTrader 5 Integration")
        print(f"   • AI-Powered Market Analysis")
        print(f"   • Risk Management System")
        print(f"   • Mobile-Friendly Interface")
        print(f"   • Real-time Notifications")
        print(f"   • Telegram & Email Alerts")
        print("="*60)
        print("🔧 Setup Instructions:")
        print("1. Configure MT5 credentials in environment variables")
        print("2. Set up Telegram bot token for notifications")
        print("3. Configure email settings for alerts")
        print("4. Access the web interface from your mobile device")
        print("="*60)
        print("⚠️  IMPORTANT: This is for educational purposes only!")
        print("   Always test with demo accounts first!")
        print("="*60 + "\n")
        
        # Run the application
        socketio.run(
            app,
            host=WEB_CONFIG['host'],
            port=WEB_CONFIG['port'],
            debug=WEB_CONFIG['debug'],
            allow_unsafe_werkzeug=True
        )
        
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()