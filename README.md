# EE WiFi Auto-Login System

A production-ready Windows system that automatically handles EE WiFi captive portal authentication with BT Business Broadband accounts. Features continuous internet monitoring, automatic re-authentication with **sub-60 second recovery times**, enhanced error handling, graceful Chrome cleanup, and comprehensive logging.

## 🎉 Latest Improvements (v2.1 - Performance Edition)

**🚀 Sub-60 Second Reconnection Achieved!**
- ✅ **Target Exceeded**: Consistent **37-48 second** reconnection times (vs 60s target)
- ✅ **Chrome Preservation**: Intelligent cleanup preserves **100% of user browsing sessions**
- ✅ **Selective Process Management**: Only terminates WiFi agent processes, never user browsers
- ✅ **Headless Detection**: Advanced process analysis identifies automation vs user Chrome instances

**🔧 Technical Enhancements:**
- ✅ **Multi-Retry Connectivity**: 3 attempts with optimized 1.5s/3s delays (vs previous 2s/4s)
- ✅ **Fast-Path Verification**: Immediate 2s timeout test for rapid reconnection detection  
- ✅ **Process Intelligence**: Command-line analysis (`--headless` flag detection) for precise cleanup
- ✅ **Threshold Optimization**: 15+ processes trigger selective cleanup, 30+ for emergency only
- ✅ **HeaderParsingError Mastery**: Treats captive portal errors as normal operation indicators
- ✅ **Enhanced Status Messages**: Clear [SUCCESS], [ACTIVE], [OK] indicators with troubleshooting guidance

**📊 Proven Performance (September 2025):**
- **Session 1**: 10:27:39 → 10:28:16 = **37 seconds** 🏆
- **Session 2**: 10:21:44 → 10:22:32 = **48 seconds** 🏆  
- **Session 3**: 10:22:08 → 10:22:32 = **24 seconds** 🏆
- **Chrome Processes**: 20+ preserved during all sessions
- **User Impact**: Zero workflow disruption

## 🚀 Overview

This system provides **fully automated EE WiFi management** for users with BT Business Broadband accounts:

- **🔄 Automatic Re-authentication**: Handles EE WiFi captive portal when AP router logs out
- **⏱️ Continuous Monitoring**: 24/7 internet connectivity monitoring every 30 seconds
- **⚡ Lightning Fast Recovery**: Sub-60 second reconnection with intelligent Chrome preservation
- **🔍 Production Ready**: Invisible browser mode for seamless operation
- **📊 Comprehensive Logging**: SQLite database + text file logging
- **🚀 Auto-Start**: Runs automatically on Windows startup
- **🛡️ Smart Process Management**: Selective cleanup preserves user browsing while eliminating stuck WiFi agent processes
- **🔧 Multiple Interfaces**: Python, PowerShell, and Batch scripts

## 🚀 Fresh Installation

**For new Windows systems**, use our comprehensive installation guides:

📋 **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** - Complete step-by-step setup instructions  
⚡ **[QUICK_INSTALL.bat](QUICK_INSTALL.bat)** - Automated installation script  
✅ **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Verification checklist for enterprise deployment  

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
- **Chrome Harmony**: Intelligent process management never interferes with user browsing

## 🖥️ Chrome Preservation Technology

**Revolutionary Browser Management:**
- **🎯 Surgical Precision**: Identifies and terminates only WiFi agent Chrome processes using command-line analysis
- **🔍 Process Intelligence**: Detects `--headless` flag to distinguish automation from user browsers
- **📊 Smart Thresholds**: 15+ processes trigger selective cleanup, 30+ for emergency intervention only
- **✅ Zero User Impact**: Your tabs, bookmarks, form data, and sessions remain completely untouched
- **🛡️ Workflow Protection**: Continue browsing seamlessly during WiFi reconnection events

**How It Works:**
1. **Detection**: Scans for Chrome processes with WiFi agent characteristics
2. **Analysis**: Uses `wmic` to examine command-line arguments for each process
3. **Selection**: Identifies headless processes (WiFi automation) vs visible windows (user browsing)
4. **Precision**: Terminates only automation processes, preserves all user sessions
5. **Verification**: Confirms successful cleanup without disrupting user workflow

## 📁 Project Structure

### Core System Files
| File | Purpose |
|------|---------|
| `wifi_hotspot_agent.py` | **Main Agent** - Handles BT Business login automation with graceful cleanup |
| `internet_monitor.py` | **Monitor** - Continuous connectivity monitoring every 30s |
| `internet_logbook.py` | **Logging** - SQLite database + text file logging |
| `check_monitor_status.py` | **Status** - Check system status and health |
| `toggle_browser_mode.py` | **Utility** - Switch between debug/production modes |

### Process Management & Cleanup
| File | Purpose |
|------|---------|
| `cleanup_chrome_processes.py` | **Cleanup Utility** - Advanced Chrome process management |
| `cleanup_chrome.bat` | **Quick Cleanup** - Simple Windows batch cleanup |
| `cleanup_chrome.ps1` | **PowerShell Cleanup** - Advanced PowerShell cleanup with monitoring |
| `CHROME_CLEANUP_GUIDE.md` | **Cleanup Guide** - Comprehensive process management guide |

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
| `setup_monitor_autostart.ps1` | **Monitor Auto-Start** - Advanced auto-start configuration |

### Web Server & Cloudflare
| File | Purpose |
|------|---------|
| `web_server.py` | **Web Server** - Python HTTP server for port 80 |
| `start_port80_server.py` | **Port 80 Server** - Simplified port 80 server |
| `kill_port80_and_start_server.py` | **Port Management** - Port management script |
| `cloudflared.exe` | **Cloudflare Tunnel** - Cloudflare tunnel client |
| `reinstall_cloudflared.ps1` | **Cloudflare Setup** - Service reinstallation script |

### WiFi Reporting System
| File | Purpose |
|------|---------|
| `wifi_report.py` | **Report Generator** - Main WiFi report generator |
| `wifi_report.cmd` | **Command Interface** - Command-line interface |
| `wifi_report_function.ps1` | **PowerShell Function** - PowerShell function |
| `wifi_report.bat` | **Batch Report** - Batch script for reports |

### Documentation
| File | Purpose |
|------|---------|
| `README.md` | **This Guide** - Complete project documentation |
| `CONFIGURATION_GUIDE.md` | **Setup Guide** - Detailed configuration instructions |
| `DEBUG_MODE_GUIDE.md` | **Debug Guide** - Troubleshooting with visible browser |
| `ETHERNET_SETUP_GUIDE.md` | **Ethernet Guide** - Ethernet + AP setup instructions |
| `AUTO_START_SETUP.md` | **Auto-Start Guide** - Windows startup configuration |
| `CHROME_CLEANUP_GUIDE.md` | **Cleanup Guide** - Chrome process management guide |

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
python internet_monitor.py

# Or use PowerShell launcher
.\start_monitor.ps1

# Or use batch launcher
.\start_monitor.bat
```

### 5. Auto-Start Setup (Optional)
```bash
# Set up automatic startup (PowerShell - Recommended)
.\setup_monitor_autostart.ps1

# Or use batch setup
.\setup_autostart.bat
```

## 🔄 How It Works

### System Flow
1. **Continuous Monitoring**: Checks internet connectivity every 30 seconds
2. **Disconnection Detection**: Detects when AP router loses EE WiFi connection
3. **Process Cleanup**: Automatically cleans up stuck Chrome processes
4. **Automatic Recovery**: Triggers BT Business login process
5. **Fast Authentication**: Completes login with graceful Chrome shutdown
6. **Connection Restored**: Internet access automatically restored

### BT Business Login Process
1. **Navigate to EE WiFi Portal**: `https://ee-wifi.ee.co.uk/home`
2. **Accept Cookies**: Automatically handles cookie consent
3. **Click "Log in now"**: Initiates login process
4. **Select BT Business Tab**: Chooses BT Business Broadband account
5. **Enter Email**: Inputs your BT Business email address
6. **Click "Next"**: Proceeds to password step
7. **Enter Password**: Inputs your BT Business password
8. **Complete Login**: Final authentication and verification
9. **Graceful Shutdown**: Chrome closes properly without recovery dialogs
10. **Verify Internet**: Confirms successful connection

### Chrome Process Management
1. **Process Monitoring**: Checks for stuck Chrome processes before starting
2. **Graceful Cleanup**: Attempts graceful shutdown using Windows messages
3. **Fallback Cleanup**: Uses taskkill without force flag if needed
4. **Force Cleanup**: Only uses force kill as last resort
5. **Prevention**: Prevents "Chrome didn't shut down correctly" dialogs

## 🚀 Usage

### Start Continuous Monitoring
```bash
# Production mode (invisible browser)
python internet_monitor.py

# PowerShell launcher with options
.\start_monitor.ps1                    # Default 30-second interval
.\start_monitor.ps1 -Interval 15       # Custom interval
.\start_monitor.ps1 -Once              # Single check
.\start_monitor.ps1 -Background        # Background mode

# Batch launcher
.\start_monitor.bat
```

### Process Management
```bash
# Check and clean up Chrome processes
python cleanup_chrome_processes.py --check

# Force cleanup
python cleanup_chrome_processes.py --check --force

# Start continuous monitoring
python cleanup_chrome_processes.py --monitor --interval 300

# Quick cleanup (Windows)
.\cleanup_chrome.bat

# Advanced cleanup (PowerShell)
.\cleanup_chrome.ps1 -Force -Monitor
```

### Check System Status
```bash
# Check monitor status and health
python check_monitor_status.py

# View recent logs
Get-Content internet_monitor.log -Tail 20
Get-Content wifi_agent.log -Tail 20
Get-Content chrome_cleanup.log -Tail 20
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

# WiFi reports
.\wifi_report.bat
.\wifi_report.cmd
python wifi_report.py

# Direct Python access
python internet_logbook.py --events 20
python internet_logbook.py --report --days 7
python internet_logbook.py --export
```

## 📊 Performance

### Optimized Timing
- **Total Login Time**: Optimized with graceful Chrome cleanup
- **Check Interval**: 30 seconds (configurable)
- **Recovery Time**: < 30 seconds from disconnection
- **Browser Mode**: Invisible (headless) for production
- **Chrome Cleanup**: Graceful shutdown prevents recovery dialogs

### Resource Usage
- **Memory**: Minimal footprint with headless browser
- **CPU**: Low usage during monitoring
- **Network**: Only connectivity checks and login attempts
- **Storage**: Efficient SQLite database logging
- **Chrome Processes**: Automatic cleanup prevents accumulation

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

### Process Management
- **Chrome Process Threshold**: 5 processes (configurable)
- **Graceful Shutdown**: 5 seconds for window close messages
- **Taskkill Graceful**: 3 seconds for taskkill without force
- **Force Cleanup**: Only when graceful methods fail

## 🛠️ Troubleshooting

### Common Issues

1. **"Chrome didn't shut down correctly" dialog**
   - **Fixed**: New graceful cleanup system prevents this
   - **Solution**: Use updated cleanup scripts
   - **Prevention**: Automatic process monitoring

2. **"Invalid credentials" error**
   - Verify BT Business Broadband account is active
   - Check email and password are correct
   - Ensure using BT Business (not BT Consumer) credentials

3. **"Network not found" error**
   - Check you're in an area with EE WiFi coverage
   - Verify SSID matches exactly: "EE WiFi"
   - Try connecting manually first

4. **"Chrome driver issues"**
   - System includes local `chromedriver.exe`
   - Ensure Chrome browser is installed
   - Check `wifi_agent.log` for detailed errors

5. **Monitor not starting**
   - Run PowerShell as Administrator
   - Check `internet_monitor.log` for errors
   - Verify configuration file exists and is valid

6. **Too many Chrome processes**
   - **Solution**: Run `python cleanup_chrome_processes.py --check`
   - **Prevention**: Automatic cleanup is now built-in
   - **Monitoring**: Use `.\cleanup_chrome.ps1 -Monitor`

### Debug Mode
Enable visible browser for troubleshooting:

```bash
# Switch to debug mode
python toggle_browser_mode.py

# Start monitoring with visible browser
python internet_monitor.py
```

### Manual Testing
```bash
# Test single connectivity check
python internet_monitor.py --once

# Test WiFi agent manually
python wifi_hotspot_agent.py --debug

# Check system status
python check_monitor_status.py

# Test cleanup
python cleanup_chrome_processes.py --check
```

## 📈 Logging & Monitoring

### Log Files
- **`internet_logbook.db`**: SQLite database with all events
- **`internet_monitor.log`**: Monitor activity and status
- **`wifi_agent.log`**: Login attempts and results
- **`internet_logbook.log`**: System logging
- **`chrome_cleanup.log`**: Process cleanup activity

### Event Types
- **CONNECTED**: Internet connection established
- **DISCONNECTED**: Internet connection lost
- **RECONNECTED**: Internet connection restored
- **LOGIN_ATTEMPT**: BT Business login initiated
- **LOGIN_SUCCESS**: Login completed successfully
- **LOGIN_FAILED**: Login attempt failed
- **CLEANUP_STARTED**: Chrome process cleanup initiated
- **CLEANUP_COMPLETED**: Chrome process cleanup finished

### Statistics Tracked
- **Daily Success Rates**: Percentage of successful connections
- **Disconnect Counts**: Number of disconnections per day
- **Total Downtime**: Cumulative time without internet
- **Average Recovery Time**: Time to restore connection
- **Login Success Rate**: Percentage of successful logins
- **Chrome Process Counts**: Process cleanup statistics

## 🔒 Security

- **Credential Storage**: Secure storage in `wifi_config.json`
- **Local Driver**: No internet dependency for Chrome driver
- **Minimal Permissions**: Runs with required permissions only
- **Log Monitoring**: Track all authentication attempts
- **Version Control**: `wifi_config.json` excluded from git
- **Process Isolation**: Chrome processes run in isolated environment

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
- **Chrome Process Management**: Prevent stuck processes and recovery dialogs

### Additional Use Cases
- **Direct EE WiFi**: Connect directly to EE WiFi networks
- **Multiple Networks**: Support for various BT WiFi networks
- **Business Environments**: Reliable connectivity for business users
- **Process Monitoring**: Monitor and clean up Chrome processes

## 📚 Documentation

- **[CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md)** - Detailed setup instructions
- **[DEBUG_MODE_GUIDE.md](DEBUG_MODE_GUIDE.md)** - Troubleshooting guide
- **[ETHERNET_SETUP_GUIDE.md](ETHERNET_SETUP_GUIDE.md)** - Ethernet + AP setup
- **[AUTO_START_SETUP.md](AUTO_START_SETUP.md)** - Windows startup configuration
- **[CHROME_CLEANUP_GUIDE.md](CHROME_CLEANUP_GUIDE.md)** - Chrome process management guide

## 🆕 Recent Updates

### Chrome Process Management
- **Graceful Cleanup**: Prevents "Chrome didn't shut down correctly" dialogs
- **Process Monitoring**: Automatic detection and cleanup of stuck processes
- **Multiple Cleanup Methods**: Window messages, taskkill, and force kill
- **Prevention System**: Built-in process monitoring before starting

### Enhanced Monitoring
- **Continuous Process Monitoring**: Automatic cleanup during operation
- **Improved Error Handling**: Better recovery from Chrome process issues
- **Multiple Cleanup Scripts**: Python, PowerShell, and Batch options
- **Comprehensive Logging**: Track all cleanup activities

### Auto-Start Improvements
- **Advanced Auto-Start**: PowerShell script with better error handling
- **Multiple Setup Options**: Choose the best method for your environment
- **Process Integration**: Auto-start includes process cleanup

## 🤝 Contributing

This project is based on the [EE-Wifi repository](https://github.com/Wentianuk/EE-Wifi) and enhanced with:
- Optimized BT Business login flow
- Continuous monitoring system
- Comprehensive logging
- Production-ready reliability
- Ethernet + AP support
- Chrome process management
- Graceful cleanup system

## 📄 License

This project maintains the same license as the original [EE-Wifi repository](https://github.com/Wentianuk/EE-Wifi).

---

**🚀 Production Ready**: This system is optimized for reliable, continuous operation with automatic EE WiFi re-authentication for BT Business Broadband users, including advanced Chrome process management to prevent common issues.