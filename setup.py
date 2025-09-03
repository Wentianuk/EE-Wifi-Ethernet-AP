#!/usr/bin/env python3
"""
WiFi Hotspot Agent Setup Script
This script helps users set up the WiFi automation system.
"""

import os
import shutil
import sys
import subprocess

def main():
    print("🌐 WiFi Hotspot Agent Setup")
    print("=" * 40)
    
    # Check if Python dependencies are installed
    print("📦 Checking Python dependencies...")
    try:
        import selenium
        import requests
        print("✅ All dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run: pip install -r requirements.txt")
            return False
    
    # Check if configuration file exists
    print("\n⚙️ Checking configuration...")
    if os.path.exists("wifi_config.json"):
        print("✅ Configuration file exists")
    else:
        print("📝 Creating configuration file...")
        if os.path.exists("wifi_config_template.json"):
            shutil.copy("wifi_config_template.json", "wifi_config.json")
            print("✅ Configuration file created from template")
            print("⚠️  Please edit wifi_config.json with your WiFi credentials")
        else:
            print("❌ Template file not found")
            return False
    
    # Check if Chrome driver exists
    print("\n🌐 Checking Chrome driver...")
    if os.path.exists("chromedriver.exe"):
        print("✅ Chrome driver found")
    else:
        print("❌ Chrome driver not found")
        print("Please ensure chromedriver.exe is in the project directory")
        return False
    
    # Test basic functionality
    print("\n🧪 Testing basic functionality...")
    try:
        from internet_logbook import InternetLogbook
        logbook = InternetLogbook()
        print("✅ Logbook system working")
    except Exception as e:
        print(f"❌ Logbook test failed: {e}")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit wifi_config.json with your WiFi credentials")
    print("2. Test the system: python wifi_hotspot_agent.py")
    print("3. Start monitoring: .\\start_monitor.ps1")
    print("4. Set up auto-start: .\\setup_autostart.ps1")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
