#!/usr/bin/env python3
"""
Main entry point for the Trading Bot
"""
import sys
import os
import logging
from mobile_app import app, init_bot

def main():
    """Main function"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('trading_bot.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Trading Bot Application...")
    
    try:
        # Initialize bot
        bot = init_bot()
        
        # Check if running in mobile mode
        if len(sys.argv) > 1 and sys.argv[1] == '--mobile':
            logger.info("Starting mobile web interface...")
            app.run(host='0.0.0.0', port=5000, debug=False)
        else:
            # Run bot in console mode
            logger.info("Starting bot in console mode...")
            bot.start()
            
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()