#!/usr/bin/env python3
"""
Quick Start Script for Trading Bot
"""
import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
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

def check_mt5_path():
    """Check if MT5 path is configured"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        mt5_path = os.getenv('MT5_PATH', '')
        if not mt5_path:
            print("⚠️  MT5_PATH not configured in .env file")
            return False
        
        if platform.system() == "Windows":
            if os.path.exists(mt5_path):
                print(f"✅ MT5 found at: {mt5_path}")
                return True
            else:
                print(f"❌ MT5 not found at: {mt5_path}")
                print("Please update MT5_PATH in .env file")
                return False
        else:
            print("⚠️  MT5 is only available on Windows")
            print("You can still use the mobile interface for monitoring")
            return True
    except Exception as e:
        print(f"❌ Error checking MT5 path: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Trading Bot Quick Start")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Check MT5 path
    mt5_ok = check_mt5_path()
    
    print("\n" + "=" * 40)
    print("🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your MT5 credentials")
    print("2. Run: python main.py --mobile")
    print("3. Open browser: http://localhost:5000")
    
    if not mt5_ok:
        print("\n⚠️  Note: MT5 connection may not work on this system")
        print("   The mobile interface will still be available")
    
    print("\n📚 For more help, see README.md")

if __name__ == "__main__":
    main()