#!/usr/bin/env python3
"""
Easy start script for the Trading Bot
"""
import os
import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    🤖 בוט מסחר MT5 + AI 📱                    ║
║                                                              ║
║  בוט מסחר מתקדם עם בינה מלאכותית וממשק מובייל ידידותי        ║
║                                                              ║
║  ✨ תכונות:                                                   ║
║  • ניתוח AI מתקדם                                            ║
║  • ממשק מובייל רספונסיבי                                     ║
║  • ניהול סיכונים חכם                                         ║
║  • גרפים אינטראקטיביים                                       ║
╚══════════════════════════════════════════════════════════════╝
""")

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("   Please run: python quick_start.py first")
        return False
    
    # Check if requirements are installed
    try:
        import MetaTrader5
        import flask
        import pandas
        import numpy
        import sklearn
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("   Please run: pip install -r requirements.txt")
        return False

def open_browser():
    """Open browser after a short delay"""
    time.sleep(3)
    webbrowser.open('http://localhost:5000')

def start_mobile_interface():
    """Start the mobile interface"""
    print("🚀 Starting Trading Bot Mobile Interface...")
    print("📱 The interface will open in your browser automatically")
    print("🌐 Manual access: http://localhost:5000")
    print("\n" + "="*50)
    print("📋 Instructions:")
    print("1. Configure your MT5 credentials in the settings")
    print("2. Click 'Start Bot' to begin trading")
    print("3. Monitor your positions and performance")
    print("4. Use 'Stop Bot' to pause trading")
    print("="*50 + "\n")
    
    # Start browser opening in background
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the Flask app
    try:
        from mobile_app import app
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Trading Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

def main():
    """Main function"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Setup incomplete. Please fix the issues above.")
        sys.exit(1)
    
    print("✅ All requirements met!")
    print()
    
    # Ask user what they want to do
    print("What would you like to do?")
    print("1. Start Mobile Interface (Recommended)")
    print("2. Run Quick Setup")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            start_mobile_interface()
            break
        elif choice == '2':
            print("Running quick setup...")
            subprocess.run([sys.executable, 'quick_start.py'])
            break
        elif choice == '3':
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()