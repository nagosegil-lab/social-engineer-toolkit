#!/usr/bin/env python3
"""
Main entry point for the trading bot
Runs both the bot and the API server
"""

import sys
import logging
from threading import Thread
from bot import TradingBot
from api import run_server

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function"""
    logger.info("=" * 50)
    logger.info("MT5 AI Trading Bot Starting...")
    logger.info("=" * 50)
    
    # Initialize the bot
    bot = TradingBot()
    
    if not bot.initialize():
        logger.error("Failed to initialize bot. Please check your configuration.")
        return 1
    
    # Start the API server in a separate thread
    api_thread = Thread(target=run_server, args=(bot,), daemon=True)
    api_thread.start()
    
    logger.info("API server started. Access the web interface from your phone!")
    logger.info("Bot is ready. Use the web interface to start trading.")
    
    try:
        # Keep the main thread alive
        while True:
            api_thread.join(timeout=1)
            if not api_thread.is_alive():
                break
    
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
    
    finally:
        bot.shutdown()
        logger.info("Bot shutdown complete. Goodbye!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
