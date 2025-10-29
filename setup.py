#!/usr/bin/env python3
"""
Mobile Trading Bot - Setup Script
תסריט התקנה לבוט מסחר נייד
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="mobile-trading-bot",
    version="1.0.0",
    description="בוט מסחר נייד עם MT5 ו-AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/mobile-trading-bot",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "python-multipart>=0.0.6",
        "websockets>=12.0",
        "MetaTrader5>=5.0.45",
        "pandas>=2.1.4",
        "numpy>=1.26.3",
        "scikit-learn>=1.4.0",
        "tensorflow>=2.15.0",
        "pydantic>=2.5.3",
        "pydantic-settings>=2.1.0",
        "requests>=2.31.0",
        "python-dateutil>=2.8.2",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mobile-trading-bot=mobile_trading_bot.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="trading bot mt5 metatrader5 ai machine-learning mobile",
)
