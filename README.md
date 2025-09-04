# EE WiFi Auto-Login System

A production-ready Windows system that automatically handles EE WiFi captive portal authentication with BT Business Broadband accounts. Features continuous internet monitoring, automatic re-authentication, and comprehensive logging.

## 🚀 Overview

This system provides **fully automated EE WiFi management** for users with BT Business Broadband accounts:

- **🔄 Automatic Re-authentication**: Handles EE WiFi captive portal when AP router logs out
- **⏱️ Continuous Monitoring**: 24/7 internet connectivity monitoring every 30 seconds
- **⚡ Fast Recovery**: 13.48-second optimized login process
- **🔍 Production Ready**: Invisible browser mode for seamless operation
- **📊 Comprehensive Logging**: SQLite database + text file logging
- **🚀 Auto-Start**: Runs automatically on Windows startup

## ⚠️ Security First

**Important**: This repository contains a template configuration file. Never commit your actual WiFi credentials to version control.

1. Copy `wifi_config_template.json` to `wifi_config.json`
2. Update `wifi_config.json` with your real BT Business credentials
3. Keep `wifi_config.json` in your `.gitignore` (already configured)
4. The template file is safe to share publicly

## 🎯 Perfect For

- **Ethernet + AP Setup**: Monitor Ethernet connection to AP router connected to EE WiFi
- **BT Business Users**: Automatic EE WiFi authentication with BT Business Broadband accounts
- **24/7 Operation**: Continuous monitoring with automatic recovery
- **Production Use**: Optimized timing and invisible browser operation

## 📁 Project Structure

### Core System Files
| File | Purpose |
|------|---------|
| `wifi_hotspot_agent.py` | **Main Agent** - Handles BT Business login automation |
| `internet_monitor.py` | **Monitor** - Continuous connectivity monitoring every 30s |
| `internet_logbook.py` | **Logging** - SQLite database + text file logging |
| `start_continuous_monitor.py` | **Launcher** - Start continuous monitoring |
| `check_monitor_status.py` | **Status** - Check system status and health |
| `toggle_browser_mode.py` | **Utility** - Switch between debug/production modes |

### Configuration & Setup
| File | Purpose |
|------|---------|
| `wifi_config.json` | **Your Config** - BT Business credentials (not in git) |
| `wifi_config_template.json` | **Template** - Safe configuration template |
| `requirements.txt` | **Dependencies** - Python package requirements |
| `chromedriver.exe` | **Driver** - Local Chrome WebDriver |

### Auto-Start & Control
| File | Purpose |
|------|---------|
| `start_monitor.ps1` | **PowerShell Launcher** - Start monitoring with options |
| `start_monitor.bat` | **Batch Launcher** - Alternative startup method |
| `setup_autostart.ps1` | **Auto-Start Setup** - Configure Windows startup |
| `setup_autostart.bat` | **Auto-Start Batch** - Alternative auto-start setup |

### Documentation
| File | Purpose |
|------|---------|
| `README.md` | **This Guide** - Complete project documentation |
| `CONFIGURATION_GUIDE.md` | **Setup Guide** - Detailed configuration instructions |
| `DEBUG_MODE_GUIDE.md` | **Debug Guide** - Troubleshooting with visible browser |
| `ETHERNET_SETUP_GUIDE.md` | **Ethernet Guide** - Ethernet + AP setup instructions |
| `AUTO_START_SETUP.md` | **Auto-Start Guide** - Windows startup configuration |

## ⚙️ Quick Setup

### 1. Prerequisites
- **BT Business Broadband Account** (not BT Consumer)
- **Python 3.7+** installed
- **Chrome Browser** installed
- **Windows 10/11** with Administrator privileges

### 2. Installation
```bash
# Clone the repository
git clone <repository-url>
cd EE-WIFI

# Install dependencies
pip install -r requirements.txt

# Configure your credentials
copy wifi_config_template.json wifi_config.json
# Edit wifi_config.json with your BT Business credentials
```

### 3. Configuration
Edit `wifi_config.json` with your BT Business credentials:

```json
{
    "connection_mode": "ethernet",
    "description": "Ethernet + AP setup - AP router connected to EE WiFi network",
    "hotspots": [
        {
            "ssid": "EE WiFi",
            "login_type": "bt_business",
            "username": "your_bt_business_email@yourdomain.com",
            "password": "your_bt_business_password",
            "portal_url": "https://ee-wifi.ee.co.uk/home",
            "description": "AP router's target network - handles captive portal re-authentication"
        }
    ],
    "check_interval": 30,
    "max_retries": 1,
    "timeout": 15,
    "debug_mode": false,
    "headless_browser": true
}
```

### 4. Start Monitoring
```bash
# Start continuous monitoring (recommended)
python start_continuous_monitor.py

# Or use PowerShell launcher
.\start_monitor.ps1
```

### 5. Auto-Start Setup (Optional)
```bash
# Set up automatic startup
.\setup_autostart.ps1
```

## 🔄 How It Works

### System Flow
1. **Continuous Monitoring**: Checks internet connectivity every 30 seconds
2. **Disconnection Detection**: Detects when AP router loses EE WiFi connection
3. **Automatic Recovery**: Triggers BT Business login process
4. **Fast Authentication**: Completes login in 13.48 seconds
5. **Connection Restored**: Internet access automatically restored

### BT Business Login Process
1. **Navigate to EE WiFi Portal**: `https://ee-wifi.ee.co.uk/home`
2. **Accept Cookies**: Automatically handles cookie consent
3. **Click "Log in now"**: Initiates login process
4. **Select BT Business Tab**: Chooses BT Business Broadband account
5. **Enter Email**: Inputs your BT Business email address
6. **Click "Next"**: Proceeds to password step
7. **Enter Password**: Inputs your BT Business password
8. **Complete Login**: Final authentication and verification
9. **Verify Internet**: Confirms successful connection

## 🚀 Usage

### Start Continuous Monitoring
```bash
# Production mode (invisible browser)
python start_continuous_monitor.py

# PowerShell launcher with options
.\start_monitor.ps1                    # Default 30-second interval
.\start_monitor.ps1 -Interval 15       # Custom interval
.\start_monitor.ps1 -Once              # Single check
.\start_monitor.ps1 -Background        # Background mode
```

### Check System Status
```bash
# Check monitor status and health
python check_monitor_status.py

# View recent logs
Get-Content internet_monitor.log -Tail 20
```

### Toggle Browser Mode
```bash
# Switch between debug and production modes
python toggle_browser_mode.py

# Show current mode
python toggle_browser_mode.py show
```

### View Logs and Reports
```bash
# PowerShell log viewer
.\view_logbook.ps1 -Events    # Recent events
.\view_logbook.ps1 -Report    # Comprehensive report
.\view_logbook.ps1 -Today     # Today's summary
.\view_logbook.ps1 -Export    # Export all data

# Direct Python access
python internet_logbook.py --events 20
python internet_logbook.py --report --days 7
python internet_logbook.py --export
```

## 📊 Performance

### Optimized Timing
- **Total Login Time**: 13.48 seconds (33% faster than original)
- **Check Interval**: 30 seconds
- **Recovery Time**: < 30 seconds from disconnection
- **Browser Mode**: Invisible (headless) for production

### Resource Usage
- **Memory**: Minimal footprint with headless browser
- **CPU**: Low usage during monitoring
- **Network**: Only connectivity checks and login attempts
- **Storage**: Efficient SQLite database logging

## 🔧 Configuration Options

### Connection Modes
- **`ethernet`**: Monitor Ethernet connection (recommended for AP setup)
- **`wifi`**: Monitor WiFi connection directly

### Browser Modes
- **`headless_browser: true`**: Invisible browser (production)
- **`headless_browser: false`**: Visible browser (debugging)

### Debug Options
- **`debug_mode: true`**: Detailed logging and visible browser
- **`debug_mode: false`**: Production mode with minimal logging

### Timing Settings
- **`check_interval`**: Seconds between connectivity checks (default: 30)
- **`timeout`**: Connection timeout in seconds (default: 15)
- **`max_retries`**: Login attempt retries (default: 1)

## 🛠️ Troubleshooting

### Common Issues

1. **"Invalid credentials" error**
   - Verify BT Business Broadband account is active
   - Check email and password are correct
   - Ensure using BT Business (not BT Consumer) credentials

2. **"Network not found" error**
   - Check you're in an area with EE WiFi coverage
   - Verify SSID matches exactly: "EE WiFi"
   - Try connecting manually first

3. **"Chrome driver issues"**
   - System includes local `chromedriver.exe`
   - Ensure Chrome browser is installed
   - Check `wifi_agent.log` for detailed errors

4. **Monitor not starting**
   - Run PowerShell as Administrator
   - Check `internet_monitor.log` for errors
   - Verify configuration file exists and is valid

### Debug Mode
Enable visible browser for troubleshooting:

```bash
# Switch to debug mode
python toggle_browser_mode.py

# Start monitoring with visible browser
python start_continuous_monitor.py
```

### Manual Testing
```bash
# Test single connectivity check
python internet_monitor.py --once

# Test WiFi agent manually
python wifi_hotspot_agent.py

# Check system status
python check_monitor_status.py
```

## 📈 Logging & Monitoring

### Log Files
- **`internet_logbook.db`**: SQLite database with all events
- **`internet_monitor.log`**: Monitor activity and status
- **`wifi_agent.log`**: Login attempts and results
- **`internet_logbook.log`**: System logging

### Event Types
- **CONNECTED**: Internet connection established
- **DISCONNECTED**: Internet connection lost
- **RECONNECTED**: Internet connection restored
- **LOGIN_ATTEMPT**: BT Business login initiated
- **LOGIN_SUCCESS**: Login completed successfully
- **LOGIN_FAILED**: Login attempt failed

### Statistics Tracked
- **Daily Success Rates**: Percentage of successful connections
- **Disconnect Counts**: Number of disconnections per day
- **Total Downtime**: Cumulative time without internet
- **Average Recovery Time**: Time to restore connection
- **Login Success Rate**: Percentage of successful logins

## 🔒 Security

- **Credential Storage**: Secure storage in `wifi_config.json`
- **Local Driver**: No internet dependency for Chrome driver
- **Minimal Permissions**: Runs with required permissions only
- **Log Monitoring**: Track all authentication attempts
- **Version Control**: `wifi_config.json` excluded from git

## 📋 Requirements

### System Requirements
- **Python 3.7+**
- **Windows 10/11**
- **Chrome Browser**
- **Administrator Privileges** (for auto-start setup)

### Python Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- `selenium` - Browser automation
- `requests` - HTTP connectivity testing
- `webdriver-manager` - Chrome driver management

## 🎯 Use Cases

### Primary Use Case
- **Ethernet + AP Setup**: Monitor Ethernet connection to AP router
- **Automatic Re-authentication**: Handle EE WiFi captive portal when AP logs out
- **24/7 Operation**: Continuous monitoring with automatic recovery

### Additional Use Cases
- **Direct EE WiFi**: Connect directly to EE WiFi networks
- **Multiple Networks**: Support for various BT WiFi networks
- **Business Environments**: Reliable connectivity for business users

## 📚 Documentation

- **[CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md)** - Detailed setup instructions
- **[DEBUG_MODE_GUIDE.md](DEBUG_MODE_GUIDE.md)** - Troubleshooting guide
- **[ETHERNET_SETUP_GUIDE.md](ETHERNET_SETUP_GUIDE.md)** - Ethernet + AP setup
- **[AUTO_START_SETUP.md](AUTO_START_SETUP.md)** - Windows startup configuration

## 🤝 Contributing

This project is based on the [EE-Wifi repository](https://github.com/Wentianuk/EE-Wifi) and enhanced with:
- Optimized BT Business login flow
- Continuous monitoring system
- Comprehensive logging
- Production-ready reliability
- Ethernet + AP support

## 📄 License

This project maintains the same license as the original [EE-Wifi repository](https://github.com/Wentianuk/EE-Wifi).

---

**🚀 Production Ready**: This system is optimized for reliable, continuous operation with automatic EE WiFi re-authentication for BT Business Broadband users.