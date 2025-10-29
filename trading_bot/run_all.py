#!/usr/bin/env python3
"""
Complete Trading Bot Launcher
Provides all options in one place
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
║  • תמיכה מלאה בעברית                                         ║
╚══════════════════════════════════════════════════════════════╝
""")

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_requirements():
    """Check if requirements are installed"""
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

def install_requirements():
    """Install requirements"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("📝 Creating .env file...")
        try:
            with open('.env.example', 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)
            print("✅ .env file created. Please edit it with your MT5 credentials.")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
        return True

def create_directories():
    """Create necessary directories"""
    dirs = ['models', 'logs', 'static/css', 'static/js', 'templates']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
    print("✅ Directories created")

def run_demo():
    """Run demo mode"""
    print("🎮 Running Demo Mode...")
    print("This will show the bot capabilities without requiring MT5 connection")
    print()
    
    try:
        subprocess.run([sys.executable, "run_demo.py"])
    except Exception as e:
        print(f"❌ Error running demo: {e}")

def run_mobile_interface():
    """Run mobile interface"""
    print("📱 Starting Mobile Interface...")
    print("The interface will open in your browser automatically")
    print("Manual access: http://localhost:5000")
    print()
    
    # Start browser opening in background
    def open_browser():
        time.sleep(3)
        webbrowser.open('http://localhost:5000')
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        from mobile_app import app
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Mobile interface stopped by user")
    except Exception as e:
        print(f"❌ Error starting mobile interface: {e}")

def run_console_mode():
    """Run console mode"""
    print("💻 Starting Console Mode...")
    print("The bot will run in the console without web interface")
    print()
    
    try:
        from trading_bot import TradingBot
        bot = TradingBot()
        bot.start()
    except KeyboardInterrupt:
        print("\n👋 Console mode stopped by user")
    except Exception as e:
        print(f"❌ Error in console mode: {e}")

def run_examples():
    """Run examples"""
    print("📚 Running Examples...")
    print("This will demonstrate the bot's capabilities")
    print()
    
    try:
        subprocess.run([sys.executable, "example_usage.py"])
    except Exception as e:
        print(f"❌ Error running examples: {e}")

def main():
    """Main function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if we're in the right directory
    if not os.path.exists('trading_bot.py'):
        print("❌ Please run this script from the trading_bot directory")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Check requirements
    if not check_requirements():
        print("\n🔧 Would you like to install requirements? (y/n): ", end="")
        if input().lower() == 'y':
            if not install_requirements():
                sys.exit(1)
        else:
            print("❌ Cannot continue without required packages")
            sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    print("\n" + "="*50)
    print("🎯 What would you like to do?")
    print("="*50)
    print("1. 🎮 Run Demo (No MT5 required)")
    print("2. 📱 Start Mobile Interface (Recommended)")
    print("3. 💻 Run Console Mode")
    print("4. 📚 Run Examples")
    print("5. 🔧 Install/Update Requirements")
    print("6. ❌ Exit")
    print("="*50)
    
    while True:
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                run_demo()
                break
            elif choice == '2':
                run_mobile_interface()
                break
            elif choice == '3':
                run_console_mode()
                break
            elif choice == '4':
                run_examples()
                break
            elif choice == '5':
                install_requirements()
                break
            elif choice == '6':
                print("👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please enter 1-6.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()