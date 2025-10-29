"""
Mobile Trading Bot with MT5 and AI Integration
==============================================

A comprehensive trading bot that can be controlled from your mobile device,
featuring MetaTrader 5 integration and AI-powered market analysis.

Author: Trading Bot Team
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Trading Bot Team"

from .core.bot import TradingBot
from .ai.engine import AIEngine
from .mt5.connector import MT5Connector

__all__ = ['TradingBot', 'AIEngine', 'MT5Connector']