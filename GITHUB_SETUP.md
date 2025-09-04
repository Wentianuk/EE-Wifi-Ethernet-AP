# GitHub Setup Guide

Quick start guide for users cloning this repository from GitHub.

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd EE-WIFI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Credentials
```bash
# Copy the template
copy wifi_config_template.json wifi_config.json

# Edit with your BT Business credentials
notepad wifi_config.json
```

### 4. Update Configuration
Edit `wifi_config.json` with your BT Business Broadband credentials:

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

### 5. Test Configuration
```bash
# Test single connectivity check
python internet_monitor.py --once

# Test WiFi agent
python wifi_hotspot_agent.py
```

### 6. Start Monitoring
```bash
# Start continuous monitoring
python start_continuous_monitor.py

# Or use PowerShell launcher
.\start_monitor.ps1
```

## ⚠️ Important Notes

### Prerequisites
- **BT Business Broadband Account** (not BT Consumer)
- **Python 3.7+** installed
- **Chrome Browser** installed
- **Windows 10/11** with Administrator privileges

### Security
- **Never commit** `wifi_config.json` to version control
- **Keep credentials secure** in your local configuration
- **Use template file** for sharing configuration structure

### First Run
- **Test manually** before setting up auto-start
- **Check logs** for any configuration issues
- **Verify credentials** work with manual EE WiFi login

## 🔧 Troubleshooting

### Common Issues

1. **"Python not found"**
   ```bash
   # Verify Python installation
   python --version
   # Should show Python 3.7 or higher
   ```

2. **"Module not found"**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **"Chrome driver not found"**
   - System includes local `chromedriver.exe`
   - Ensure Chrome browser is installed
   - Check `wifi_agent.log` for detailed errors

4. **"Invalid credentials"**
   - Verify BT Business Broadband account is active
   - Check email and password are correct
   - Ensure using BT Business (not BT Consumer) credentials

### Debug Mode
Enable visible browser for troubleshooting:

```bash
# Switch to debug mode
python toggle_browser_mode.py

# Start monitoring with visible browser
python start_continuous_monitor.py
```

## 📚 Next Steps

1. **Read Documentation**: Check `README.md` for complete guide
2. **Configure Auto-Start**: See `AUTO_START_SETUP.md`
3. **Troubleshoot Issues**: See `DEBUG_MODE_GUIDE.md`
4. **Monitor Logs**: Use `view_logbook.ps1` to check system status

## 🆘 Support

- **Check Logs**: `internet_monitor.log`, `wifi_agent.log`
- **System Status**: `python check_monitor_status.py`
- **Documentation**: All `.md` files in the repository
- **Configuration**: `CONFIGURATION_GUIDE.md`

---

**Ready to go!** Your EE WiFi auto-login system should now be running and monitoring your internet connection every 30 seconds.