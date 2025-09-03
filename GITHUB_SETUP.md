# GitHub Repository Setup Guide

This guide helps you set up this WiFi automation system from the GitHub repository.

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/EE-WIFI-Automation.git
cd EE-WIFI-Automation
```

### 2. Run Setup Script
```bash
# Install dependencies and set up configuration
python setup.py
```

### 3. Configure Your WiFi
Edit `wifi_config.json` with your credentials:
```json
{
    "hotspots": [
        {
            "ssid": "EE WiFi",
            "login_type": "bt_business",
            "username": "your_email@example.com",
            "password": "your_password",
            "portal_url": "https://ee-wifi.ee.co.uk/home"
        }
    ]
}
```

### 4. Test the System
```bash
# Test WiFi agent
python wifi_hotspot_agent.py

# Test monitoring
python internet_monitor.py --once
```

### 5. Start Monitoring
```powershell
# Start continuous monitoring
.\start_monitor.ps1

# Set up auto-start (optional)
.\setup_autostart.ps1
```

## 📋 What's Included

- ✅ **WiFi Agent**: Automatic connection and captive portal handling
- ✅ **Internet Monitor**: Continuous connectivity monitoring
- ✅ **Logbook System**: Comprehensive logging and reporting
- ✅ **Auto-Start**: Windows Task Scheduler integration
- ✅ **Chrome Driver**: Local driver for offline operation
- ✅ **Setup Script**: Automated dependency installation

## 🔒 Security Notes

- **Never commit `wifi_config.json`** - It contains your credentials
- **Use the template** - `wifi_config_template.json` is safe to share
- **Check .gitignore** - Ensures credentials stay private

## 🆘 Need Help?

1. **Check the main README.md** for detailed documentation
2. **Run the setup script** for automated configuration
3. **Check logs** for troubleshooting information
4. **Test components** individually to isolate issues

## 🎯 For EE WiFi Users

If you have a BT Business Broadband account:
1. Use `login_type: "bt_business"` in your configuration
2. Use your BT Business email and password
3. The system will handle the complete EE WiFi login flow automatically

## 📊 Features

- **24/7 Monitoring**: Continuous internet connectivity checking every 30 seconds
- **Ultra-Fast Response**: Triggers WiFi agent after just 1 failure (30 seconds)
- **Invisible Browser**: Runs completely in background with headless Chrome
- **Auto-Recovery**: Automatically reconnects when internet is lost
- **Comprehensive Logging**: SQLite database + text file logging
- **Multiple Networks**: Supports EE WiFi, BTWiFi, and custom networks
- **Production Ready**: Optimized timing and error handling
