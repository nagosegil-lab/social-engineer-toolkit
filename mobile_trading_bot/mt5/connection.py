"""
MT5 Connection Manager
מנהל חיבור ל-MetaTrader 5
"""

import MetaTrader5 as mt5
from typing import Optional, Dict, Any
from mobile_trading_bot.core.config import settings
from mobile_trading_bot.core.logger import setup_logger

logger = setup_logger(__name__)


class MT5Connection:
    """Manages connection to MT5 platform"""
    
    def __init__(self):
        self.connected = False
        self.account_info: Optional[Dict[str, Any]] = None
    
    def connect(
        self,
        login: Optional[int] = None,
        password: Optional[str] = None,
        server: Optional[str] = None,
        path: Optional[str] = None
    ) -> bool:
        """
        Connect to MT5 terminal
        התחברות לטרמינל MT5
        
        Args:
            login: Account login number
            password: Account password
            server: Broker server name
            path: Path to MT5 terminal executable
            
        Returns:
            True if connected successfully, False otherwise
        """
        try:
            # Initialize MT5
            if not mt5.initialize(path=path or settings.MT5_PATH):
                logger.error(f"MT5 initialization failed: {mt5.last_error()}")
                return False
            
            # Login
            login = login or settings.MT5_LOGIN
            password = password or settings.MT5_PASSWORD
            server = server or settings.MT5_SERVER
            
            if login and password and server:
                authorized = mt5.login(login, password=password, server=server)
                if not authorized:
                    error = mt5.last_error()
                    logger.error(f"MT5 login failed: {error}")
                    mt5.shutdown()
                    return False
            else:
                logger.warning("MT5 credentials not provided, using default connection")
            
            # Get account info
            account_info = mt5.account_info()
            if account_info is None:
                logger.error("Failed to get account info")
                mt5.shutdown()
                return False
            
            self.account_info = account_info._asdict()
            self.connected = True
            
            logger.info(f"✅ Connected to MT5 - Account: {account_info.login}, Balance: {account_info.balance}")
            return True
            
        except Exception as e:
            logger.error(f"Error connecting to MT5: {str(e)}")
            return False
    
    def disconnect(self) -> None:
        """Disconnect from MT5"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            logger.info("Disconnected from MT5")
    
    def get_account_info(self) -> Optional[Dict[str, Any]]:
        """Get account information"""
        if not self.connected:
            return None
        
        try:
            account_info = mt5.account_info()
            if account_info:
                return account_info._asdict()
        except Exception as e:
            logger.error(f"Error getting account info: {str(e)}")
        
        return None
    
    def is_connected(self) -> bool:
        """Check if connected to MT5"""
        return self.connected
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()


# Global connection instance
mt5_connection = MT5Connection()
