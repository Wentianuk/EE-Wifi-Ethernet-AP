# WiFi Hotspot Auto-Connect Agent with Internet Monitor & Logbook

A comprehensive Windows-based system that automatically connects to WiFi hotspots, handles captive portal authentication, monitors internet connectivity, and maintains detailed logs of all connectivity events.

## 🚀 Project Overview

This system provides **fully automated WiFi hotspot management** with:
- **Automatic WiFi Connection**: Connects to configured networks without user intervention
- **Smart Captive Portal Handling**: Supports multiple login types including BT Business Broadband
- **Continuous Internet Monitoring**: 24/7 connectivity monitoring with auto-recovery
- **Comprehensive Logging**: SQLite database + text file logging of all connectivity events
- **Auto-Start Capability**: Runs automatically on Windows startup
- **Production-Ready**: Optimized timing and error handling for reliable operation

## ⚠️ Security First

**Important**: This repository contains a template configuration file. Never commit your actual WiFi credentials to version control.

1. Copy `wifi_config_template.json` to `wifi_config.json`
2. Update `wifi_config.json` with your real credentials
3. Keep `wifi_config.json` in your `.gitignore` (already configured)
4. The template file is safe to share publicly

## 📁 File Structure & Functions

### Core System Files
| File | Function | Description |
|------|----------|-------------|
| `wifi_hotspot_agent.py` | **Main WiFi Agent** | Automatically connects to WiFi hotspots and handles captive portal authentication. Supports multiple login types with optimized timing. |
| `internet_monitor.py` | **Internet Monitor** | Continuously monitors internet connectivity every 30 seconds. Automatically triggers WiFi agent when connection is lost. |
| `internet_logbook.py` | **Connectivity Logbook** | Records all connectivity events to SQLite database. Provides reports, statistics, and text file exports. |
| `chromedriver.exe` | **Chrome Driver** | Local Chrome WebDriver for browser automation. Eliminates need for internet connection during setup. |

### Configuration Files
| File | Function | Description |
|------|----------|-------------|
| `wifi_config.json` | **WiFi Configuration** | Your actual WiFi credentials and settings (not in git). Contains SSIDs, login types, usernames, passwords. |
| `wifi_config_template.json` | **Configuration Template** | Safe template file showing required configuration structure. Safe to share publicly. |
| `requirements.txt` | **Python Dependencies** | Lists all required Python packages for the system. |

### Auto-Start & Setup
| File | Function | Description |
|------|----------|-------------|
| `setup_autostart.ps1` | **Auto-Start Setup (PowerShell)** | Creates Windows Scheduled Task to run monitor on startup. Supports custom intervals and removal. |
| `setup_autostart.bat` | **Auto-Start Setup (Batch)** | Alternative batch file for setting up auto-start functionality. |
| `AUTO_START_SETUP.md` | **Auto-Start Documentation** | Comprehensive guide for setting up automatic startup on Windows. |

### Monitoring & Control
| File | Function | Description |
|------|----------|-------------|
| `start_monitor.ps1` | **Monitor Launcher (PowerShell)** | Starts the internet monitor with various options (continuous, once, background, custom interval). |
| `start_monitor.bat` | **Monitor Launcher (Batch)** | Alternative batch file to start the internet monitor. |
| `view_logbook.ps1` | **Logbook Viewer** | PowerShell script to view connectivity reports, recent events, and export data. |

### Log Files & Data
| File | Function | Description |
|------|----------|-------------|
| `internet_logbook.db` | **SQLite Database** | Stores all connectivity events, daily summaries, and statistics. |
| `internet_connectivity_records.txt` | **Continuous Text Log** | Real-time text file logging of all connectivity events. |
| `internet_connectivity_full_export.txt` | **Full Export File** | Comprehensive export of all records with summaries and statistics. |
| `internet_logbook.log` | **System Log** | Detailed system logging for debugging and monitoring. |
| `internet_monitor.log` | **Monitor Log** | Internet monitor activity and status logs. |
| `wifi_agent.log` | **WiFi Agent Log** | WiFi connection attempts and captive portal handling logs. |

### Documentation
| File | Function | Description |
|------|----------|-------------|
| `README.md` | **Project Documentation** | This comprehensive guide covering installation, usage, and all features. |
| `CONFIGURATION_GUIDE.md` | **Configuration Guide** | Detailed guide for setting up WiFi credentials and configuration options. |
| `GITHUB_SETUP.md` | **GitHub Setup Guide** | Quick start guide for users cloning from GitHub repository. |
| `DEBUG_MODE_GUIDE.md` | **Debug Mode Guide** | Complete guide for using visible/invisible browser modes for troubleshooting. |

## 🎯 Key Features

### Automatic WiFi Connection
- **Smart Network Detection**: Automatically scans and connects to configured WiFi networks
- **Multiple Login Types**: Supports click-through, form-based, and BT Business Broadband logins
- **Optimized Performance**: Fast connection times with intelligent timing adjustments
- **Invisible Browser**: Runs completely in background with headless Chrome
- **Offline Capability**: Works without internet connection for driver management

### Captive Portal Handling
- **EE WiFi → BT Business Flow**: Complete automation of the EE WiFi login process
- **Cookie Consent**: Automatically accepts cookie policies
- **Multi-Step Login**: Handles complex login flows with email/password verification
- **Success Verification**: Confirms internet access after successful login

### Internet Monitoring
- **24/7 Monitoring**: Continuous connectivity checking every 30 seconds
- **Ultra-Fast Response**: Triggers WiFi agent after just 1 failure (30 seconds)
- **Smart Detection**: Uses multiple reliable hosts (Google DNS, Cloudflare, etc.)
- **Auto-Recovery**: Automatically runs WiFi agent when connection is lost
- **Network Awareness**: Only triggers on configured hotspot networks

### Comprehensive Logging
- **SQLite Database**: Structured storage of all connectivity events
- **Text File Logs**: Human-readable continuous logging
- **Export Functionality**: Full data export with statistics and summaries
- **Event Tracking**: Records disconnections, reconnections, downtime, and recovery times

### Auto-Start Capability
- **Windows Task Scheduler**: Runs automatically on system startup
- **Configurable Intervals**: Customizable monitoring frequency
- **Easy Setup**: Simple PowerShell scripts for installation and removal
- **Background Operation**: Runs silently without user intervention

## ⚙️ Configuration

### WiFi Configuration
Copy `wifi_config_template.json` to `wifi_config.json` and update with your settings:

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
    ],
    "check_interval": 30,
    "max_retries": 3,
    "timeout": 15
}
```

### Login Types
- **`bt_business`**: For BT Business Broadband accounts (EE WiFi, BTWiFi, etc.)
- **`form_based`**: For standard username/password forms
- **`click_through`**: For simple terms acceptance pages

## 🌐 EE WiFi Setup Guide

### Prerequisites for EE WiFi
1. **BT Business Broadband Account**: You need a BT Business Broadband account with EE WiFi access
2. **Valid Credentials**: Your BT Business email and password
3. **EE WiFi Coverage**: Ensure you're in an area with EE WiFi coverage

### Important Notes About BT Business Accounts
- **Account Type**: Must be **BT Business Broadband** (not BT Consumer)
- **EE WiFi Access**: Your BT Business account must include EE WiFi access
- **Credential Format**: Use your full BT Business email address (usually your domain email)
- **Account Status**: Ensure your BT Business account is active and in good standing
- **Coverage**: EE WiFi is available in many public locations, train stations, and business areas

### Step-by-Step EE WiFi Configuration

#### 1. Get Your BT Business Credentials
- **Email**: Your BT Business Broadband account email (usually ends with your domain)
- **Password**: Your BT Business Broadband account password
- **Account Type**: Must be BT Business Broadband (not BT Consumer)

#### 2. Configure the System
```bash
# Copy the template
copy wifi_config_template.json wifi_config.json

# Edit wifi_config.json with your credentials
```

#### 3. Update Your Configuration
Edit `wifi_config.json` and replace the placeholder values:

```json
{
    "hotspots": [
        {
            "ssid": "EE WiFi",
            "login_type": "bt_business",
            "username": "your_bt_business_email@yourdomain.com",
            "password": "your_bt_business_password",
            "portal_url": "https://ee-wifi.ee.co.uk/home"
        }
    ],
    "check_interval": 30,
    "max_retries": 3,
    "timeout": 15
}
```

#### 4. Test Your Configuration
```bash
# Test the WiFi agent manually
python wifi_hotspot_agent.py

# Test the monitor
python internet_monitor.py --once
```

### EE WiFi Network Names
The system supports these EE WiFi network variants:
- **`EE WiFi`** - Primary EE WiFi network
- **`BTWiFi`** - BT WiFi network
- **`BTWiFi-with-FON`** - BT WiFi with FON access

### EE WiFi Login Process
The system automatically handles this complete flow:
1. **Connect to EE WiFi** network
2. **Accept cookie consent** automatically
3. **Click "Log in now"** button
4. **Select "BT Business Broadband account"** tab
5. **Navigate to BT login** page
6. **Enter your email** address
7. **Click "Next"** button
8. **Enter your password**
9. **Complete login** and verify internet access
10. **Close browser** and confirm connection

### EE WiFi Troubleshooting

#### Common Issues:

1. **"Invalid credentials" error**:
   - Verify your BT Business Broadband account is active
   - Check email and password are correct
   - Ensure you're using BT Business (not BT Consumer) credentials

2. **"Network not found" error**:
   - Check you're in an area with EE WiFi coverage
   - Verify the SSID matches exactly: "EE WiFi", "BTWiFi", or "BTWiFi-with-FON"
   - Try connecting manually first to confirm the network exists

3. **"Login page not loading" error**:
   - Check your internet connection
   - Verify the portal URL is correct: `https://ee-wifi.ee.co.uk/home`
   - Try accessing the portal manually in a browser

4. **"Chrome driver issues"**:
   - The system includes a local `chromedriver.exe`
   - Ensure Chrome browser is installed
   - Check `wifi_agent.log` for detailed error messages

#### Testing Your Setup:
```bash
# Test connectivity check
python internet_logbook.py --check

# Test WiFi agent
python wifi_hotspot_agent.py

# View logs
Get-Content wifi_agent.log -Tail 20
```

## 🚀 Installation & Usage

### Quick Start for EE WiFi Users

If you have a **BT Business Broadband account** and want to automate EE WiFi connections:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure for EE WiFi
copy wifi_config_template.json wifi_config.json
# Edit wifi_config.json with your BT Business credentials

# 3. Test the setup
python wifi_hotspot_agent.py

# 4. Start monitoring (recommended)
.\start_monitor.ps1

# 5. Set up auto-start (optional)
.\setup_autostart.ps1
```

### 1. Installation

   ```bash
# Install Python dependencies
   pip install -r requirements.txt

# Configure your WiFi hotspots
copy wifi_config_template.json wifi_config.json
# Edit wifi_config.json with your credentials
```

**📖 For detailed configuration help, see [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md)**

### 2. Start Internet Monitoring (Recommended)

**PowerShell (Recommended):**
```powershell
# Start continuous monitoring
.\start_monitor.ps1

# Start with custom interval (15 seconds)
.\start_monitor.ps1 -Interval 15

# Run once to check current status
.\start_monitor.ps1 -Once

# Start in background
.\start_monitor.ps1 -Background
```

**Batch File:**
```cmd
start_monitor.bat
```

**Direct Python:**
```bash
# Continuous monitoring (invisible browser)
python internet_monitor.py

# Continuous monitoring with debug mode (visible browser)
python internet_monitor.py --debug

# Single check
python internet_monitor.py --once

# Single check with debug mode
python internet_monitor.py --once --debug

# Custom configuration and interval
python internet_monitor.py --config "wifi_config.json" --interval 60
```

### 3. Manual WiFi Agent Usage

```bash
# Run WiFi agent manually (invisible browser)
python wifi_hotspot_agent.py

# Run WiFi agent in debug mode (visible browser)
python wifi_hotspot_agent.py --debug
```

### 4. View Connectivity Logs

**PowerShell Viewer:**
```powershell
# View recent events
.\view_logbook.ps1 -Events

# Generate comprehensive report
.\view_logbook.ps1 -Report

# Export all records to text file
.\view_logbook.ps1 -Export

# Today's summary
.\view_logbook.ps1 -Today
```

**Direct Python:**
```bash
# View recent events
python internet_logbook.py --events 20

# Generate report
python internet_logbook.py --report --days 7

# Export all records
python internet_logbook.py --export

# Single connectivity check
python internet_logbook.py --check
```

### 5. Auto-Start Setup

**PowerShell (Recommended):**
```powershell
# Set up auto-start (30-second interval)
.\setup_autostart.ps1

# Set up with custom interval (15 seconds)
.\setup_autostart.ps1 -Interval 15

# Remove auto-start later
.\setup_autostart.ps1 -Remove
```

**Batch File:**
```cmd
setup_autostart.bat
```

## 🔄 How It Works

### Internet Monitor Flow
1. **Continuous Monitoring**: Checks internet connectivity every 30 seconds
2. **Smart Detection**: Uses multiple reliable hosts for accurate testing
3. **Ultra-Fast Response**: Triggers WiFi agent after just 1 failure (30 seconds)
4. **Network Awareness**: Only runs WiFi agent when connected to configured hotspots
5. **Auto-Recovery**: Automatically attempts reconnection when internet is lost

### WiFi Agent Flow
1. **Network Detection**: Scans for available WiFi networks
2. **Auto-Connection**: Connects to configured hotspots automatically
3. **Captive Portal Detection**: Identifies and handles various login types
4. **Invisible Login**: Performs complete login flow in headless browser
5. **Success Verification**: Confirms internet access after login

### EE WiFi BT Business Login Flow
1. Connects to EE WiFi network
2. Accepts cookie consent automatically
3. Clicks "Log in now" button
4. Selects "BT Business Broadband account" tab
5. Navigates to BT login page
6. Enters email address
7. Clicks "Next" button
8. Enters password
9. Completes final login and verification
10. Closes browser and confirms internet access

### Logging System
1. **Real-Time Logging**: Every connectivity event is immediately recorded
2. **Database Storage**: Structured SQLite database for queries and analysis
3. **Text File Backup**: Human-readable continuous text logging
4. **Export Functionality**: Complete data export with statistics
5. **Daily Summaries**: Automatic daily statistics and summaries

## 📊 Logging & Monitoring

### Log Files
- **`internet_logbook.db`**: SQLite database with all connectivity events
- **`internet_connectivity_records.txt`**: Continuous text log of events
- **`internet_connectivity_full_export.txt`**: Comprehensive export file
- **`internet_logbook.log`**: System logging for debugging
- **`internet_monitor.log`**: Monitor activity and status
- **`wifi_agent.log`**: WiFi connection and login attempts

### Event Types
- **CONNECTED**: Initial connection to network
- **DISCONNECTED**: Internet connection lost (with error details)
- **RECONNECTED**: Internet connection restored (with downtime duration)

### Statistics Tracked
- **Daily Success Rates**: Percentage of successful connectivity checks
- **Disconnect Counts**: Number of disconnections per day
- **Total Downtime**: Cumulative time without internet
- **Average Recovery Time**: Time to restore connection
- **Network Performance**: Success rates by network

## 🔧 Requirements

### System Requirements
- **Python 3.7+**
- **Windows 10/11** (for WiFi commands and Task Scheduler)
- **Chrome Browser** (for automation)
- **Administrator Privileges** (for WiFi operations and auto-start setup)

### Python Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- `selenium` - Browser automation
- `requests` - HTTP requests for connectivity testing
- `webdriver-manager` - Chrome driver management (optional, local driver preferred)

## 🔍 Debug Mode

The system supports both invisible (production) and visible (debug) browser modes:

### Production Mode (Default)
- Browser runs invisibly in the background
- Faster execution and lower resource usage
- Perfect for normal operation and auto-start

### Debug Mode
- Browser runs visibly so you can see what's happening
- Great for troubleshooting login issues
- Use when testing new configurations

### Usage Examples:
```bash
# Production mode (invisible browser)
python wifi_hotspot_agent.py
python internet_monitor.py

# Debug mode (visible browser)
python wifi_hotspot_agent.py --debug
python internet_monitor.py --debug
```

**📖 For detailed debug mode instructions, see [DEBUG_MODE_GUIDE.md](DEBUG_MODE_GUIDE.md)**

## 🛠️ Troubleshooting

### Common Issues

1. **"Python not found"**
   - Ensure Python is installed and in your system PATH
   - Verify Python version is 3.7 or higher

2. **"Chrome driver not found"**
   - The system includes a local `chromedriver.exe`
   - If issues persist, ensure Chrome browser is installed

3. **Permission errors**
   - Run PowerShell as Administrator for WiFi operations
   - Ensure auto-start setup is run with Administrator privileges

4. **Import errors**
   - Ensure all files are in the same directory
   - Verify all Python dependencies are installed

5. **Auto-start not working**
   - Check Windows Task Scheduler for the created task
   - Verify the task is enabled and set to run at startup
   - Check task logs for error messages

### Debug Mode

Enable detailed logging by modifying the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

### Manual Testing

Test individual components:

```bash
# Test configuration loading
python -c "from wifi_hotspot_agent import WiFiHotspotAgent; print('Config OK')"

# Test internet connectivity
python -c "from internet_monitor import InternetMonitor; m = InternetMonitor(); print('Internet:', m.check_internet_connectivity())"

# Test logbook functionality
python internet_logbook.py --check
```

## 🔒 Security Notes

- **Credential Storage**: Store sensitive credentials securely in `wifi_config.json`
- **Environment Variables**: Consider using environment variables for passwords
- **Minimal Permissions**: Run with minimal required permissions
- **Log Monitoring**: Monitor logs for unusual activity
- **Version Control**: Never commit `wifi_config.json` to version control
- **Local Driver**: Uses local Chrome driver to avoid internet dependency

## 📈 Performance Optimizations

### Timing Optimizations
- **Internet Check**: 3-second timeout for fast connectivity testing
- **Ultra-Fast Response**: 30-second trigger time (1 failure threshold)
- **Captive Portal**: Optimized delays for reliable automation
- **Login Flow**: Streamlined timing for faster connection
- **Browser Operations**: Efficient element waiting and interaction
- **Headless Mode**: Invisible browser with optimized performance

### Resource Management
- **Local Chrome Driver**: Eliminates internet dependency for driver management
- **Efficient Logging**: Structured database storage with text file backup
- **Smart Monitoring**: Configurable intervals to balance performance and responsiveness
- **Error Recovery**: Robust error handling with automatic retries

## 🎯 Use Cases

### Personal Use
- **Home WiFi Management**: Automatic connection to home networks
- **Mobile Hotspot**: Seamless switching between networks
- **Guest Networks**: Automatic handling of captive portals

### Business Use
- **Office Networks**: Automatic connection to corporate WiFi
- **Client Sites**: Seamless connectivity at customer locations
- **Remote Work**: Reliable internet connection management

### Development/Testing
- **Network Testing**: Automated connectivity testing
- **Captive Portal Testing**: Automated portal interaction testing
- **Connectivity Monitoring**: Continuous internet status monitoring

## 📚 Resources

- [Original Repository](https://github.com/Wentianuk/EE-Wifi) - Base implementation
- [Selenium Documentation](https://selenium-python.readthedocs.io/) - Browser automation
- [Windows netsh Commands](https://docs.microsoft.com/en-us/windows-server/networking/technologies/netsh/netsh-commands) - WiFi management
- [Windows Task Scheduler](https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page) - Auto-start setup

## 🤝 Contributing

This project is based on the [EE-Wifi repository](https://github.com/Wentianuk/EE-Wifi) and has been enhanced with:
- Comprehensive logging system
- Auto-start capability
- Performance optimizations
- Enhanced error handling
- Production-ready reliability

## 📄 License

This project maintains the same license as the original [EE-Wifi repository](https://github.com/Wentianuk/EE-Wifi).

---

**Ready for Production**: This system is optimized for reliable, continuous operation with comprehensive logging and monitoring capabilities.