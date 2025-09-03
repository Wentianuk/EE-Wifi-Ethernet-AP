# WiFi Configuration Guide

This guide shows you how to configure the WiFi automation system with your credentials.

## 🔧 Configuration Process

### Step 1: Run Setup Script
The setup script automatically creates your configuration file from the template:

```bash
python setup.py
```

This will:
- ✅ Install Python dependencies
- ✅ Copy `wifi_config_template.json` to `wifi_config.json`
- ✅ Verify Chrome driver is present
- ✅ Test basic functionality

### Step 2: Edit Your Configuration
After running the setup script, edit `wifi_config.json` with your actual credentials:

```json
{
    "hotspots": [
        {
            "ssid": "EE WiFi",
            "login_type": "bt_business",
            "username": "your_actual_email@yourdomain.com",
            "password": "your_actual_password",
            "portal_url": "https://ee-wifi.ee.co.uk/home"
        }
    ],
    "check_interval": 30,
    "max_retries": 3,
    "timeout": 15
}
```

## 📋 Configuration Options

### Hotspot Configuration
Each hotspot entry contains:

| Field | Description | Example |
|-------|-------------|---------|
| `ssid` | WiFi network name | `"EE WiFi"` |
| `login_type` | Login method | `"bt_business"` |
| `username` | Your login email | `"user@company.com"` |
| `password` | Your login password | `"yourpassword123"` |
| `portal_url` | Captive portal URL | `"https://ee-wifi.ee.co.uk/home"` |

### Login Types
- **`bt_business`**: For BT Business Broadband accounts (EE WiFi, BTWiFi)
- **`form_based`**: For standard username/password forms
- **`click_through`**: For simple terms acceptance pages

### System Settings
| Field | Description | Default | Range |
|-------|-------------|---------|-------|
| `check_interval` | Internet check frequency (seconds) | `30` | 15-300 |
| `max_retries` | Maximum connection attempts | `3` | 1-10 |
| `timeout` | Connection timeout (seconds) | `15` | 5-60 |

## 🌐 EE WiFi Configuration Examples

### Single EE WiFi Network
```json
{
    "hotspots": [
        {
            "ssid": "EE WiFi",
            "login_type": "bt_business",
            "username": "your_bt_email@yourdomain.com",
            "password": "your_bt_password",
            "portal_url": "https://ee-wifi.ee.co.uk/home"
        }
    ],
    "check_interval": 30,
    "max_retries": 3,
    "timeout": 15
}
```

### Multiple EE WiFi Networks
```json
{
    "hotspots": [
        {
            "ssid": "EE WiFi",
            "login_type": "bt_business",
            "username": "your_bt_email@yourdomain.com",
            "password": "your_bt_password",
            "portal_url": "https://ee-wifi.ee.co.uk/home"
        },
        {
            "ssid": "BTWiFi",
            "login_type": "bt_business",
            "username": "your_bt_email@yourdomain.com",
            "password": "your_bt_password",
            "portal_url": "https://ee-wifi.ee.co.uk/home"
        },
        {
            "ssid": "BTWiFi-with-FON",
            "login_type": "bt_business",
            "username": "your_bt_email@yourdomain.com",
            "password": "your_bt_password",
            "portal_url": "https://ee-wifi.ee.co.uk/home"
        }
    ],
    "check_interval": 30,
    "max_retries": 3,
    "timeout": 15
}
```

### Custom Network with Form-Based Login
```json
{
    "hotspots": [
        {
            "ssid": "Custom WiFi",
            "login_type": "form_based",
            "username": "your_username",
            "password": "your_password",
            "portal_url": "https://custom-portal.com/login"
        }
    ],
    "check_interval": 30,
    "max_retries": 3,
    "timeout": 15
}
```

## 🔒 Security Best Practices

### Credential Protection
- ✅ **Never share `wifi_config.json`** - It contains your real credentials
- ✅ **Use the template** - `wifi_config_template.json` is safe to share
- ✅ **Check .gitignore** - Ensures credentials stay private
- ✅ **Backup securely** - Store credentials in a password manager

### File Permissions
On Windows, you can restrict access to your configuration file:
```powershell
# Make the file readable only by you
icacls wifi_config.json /inheritance:r /grant:r "%USERNAME%:F"
```

## 🧪 Testing Your Configuration

### Test Individual Components
```bash
# Test configuration loading
python -c "from wifi_hotspot_agent import WiFiHotspotAgent; print('Config OK')"

# Test internet connectivity
python internet_logbook.py --check

# Test WiFi agent
python wifi_hotspot_agent.py
```

### Test Monitoring
```bash
# Test monitor once
python internet_monitor.py --once

# Test continuous monitoring (Ctrl+C to stop)
python internet_monitor.py
```

## 🛠️ Troubleshooting Configuration

### Common Issues

1. **"Configuration file not found"**
   - Run `python setup.py` to create the configuration file
   - Ensure `wifi_config_template.json` exists

2. **"Invalid JSON format"**
   - Check for missing commas or brackets
   - Validate JSON syntax using an online validator
   - Ensure all strings are properly quoted

3. **"Login failed"**
   - Verify your credentials are correct
   - Check that you're using BT Business (not BT Consumer) credentials
   - Ensure your account has EE WiFi access

4. **"Network not found"**
   - Verify the SSID matches exactly (case-sensitive)
   - Check you're in an area with the specified network
   - Try connecting manually first

### Configuration Validation
The system automatically validates your configuration when it starts. Check the logs for specific error messages:

```bash
# View recent logs
Get-Content wifi_agent.log -Tail 20
```

## 📝 Configuration Template

The `wifi_config_template.json` file provides a safe starting point:

```json
{
    "hotspots": [
        {
            "ssid": "EE WiFi",
            "login_type": "bt_business",
            "username": "your_email@example.com",
            "password": "your_password",
            "portal_url": "https://ee-wifi.ee.co.uk/home"
        },
        {
            "ssid": "BTWiFi-with-FON",
            "login_type": "bt_business",
            "username": "your_email@example.com",
            "password": "your_password",
            "portal_url": "https://ee-wifi.ee.co.uk/home"
        },
        {
            "ssid": "BTWiFi",
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

## 🎯 Quick Setup Summary

1. **Run setup**: `python setup.py`
2. **Edit config**: Replace placeholders in `wifi_config.json`
3. **Test system**: `python wifi_hotspot_agent.py`
4. **Start monitoring**: `.\start_monitor.ps1`

Your WiFi automation system is now configured and ready to use! 🚀
