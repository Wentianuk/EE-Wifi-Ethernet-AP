# Ethernet + AP Router Setup Guide

## 🎯 Overview

Your system has been configured to use **Ethernet connection** instead of WiFi, with automatic handling of AP router re-authentication to the EE WiFi network.

## 🔧 What Changed

### 1. **Connection Mode**
- **Before**: WiFi connection to "Profile" network
- **After**: Ethernet connection to AP router (which connects to EE WiFi)

### 2. **Monitoring Logic**
- **Before**: Monitored WiFi network status
- **After**: Monitors Ethernet connection and internet connectivity
- **Trigger**: When internet fails, automatically handles AP router re-authentication

### 3. **Auto-Login Process**
- **Before**: Connected to EE WiFi when Profile failed
- **After**: Handles captive portal login when AP router gets logged out from EE WiFi

## 🚀 Setup Instructions

### Step 1: Enable Ethernet-Only Mode
```bash
# Run the setup script
.\setup_ethernet_mode.bat
```

This will:
- Disable WiFi adapter
- Enable Ethernet adapter
- Set Ethernet as preferred connection

### Step 2: Test Your Setup
```bash
# Test the Ethernet + AP configuration
python test_ethernet_connection.py
```

### Step 3: Start Monitoring
```bash
# Start the internet monitor in Ethernet mode
python internet_monitor.py
```

## 📋 How It Works

### **Normal Operation**
1. Your computer connects via **Ethernet cable** to the **AP router**
2. AP router is connected to **EE WiFi network**
3. System monitors internet connectivity every 30 seconds
4. When internet is available, everything works normally

### **When AP Router Gets Logged Out**
1. Internet connectivity check fails
2. System detects Ethernet connection (not WiFi)
3. Automatically triggers captive portal login process
4. Opens browser to `https://ee-wifi.ee.co.uk/home`
5. Performs BT Business login with your credentials
6. Restores internet connectivity

## 🔍 Configuration Details

### **Your Current Config** (`wifi_config.json`)
```json
{
    "connection_mode": "ethernet",
    "description": "Ethernet + AP setup - AP router connected to EE WiFi network",
    "hotspots": [
        {
            "ssid": "EE WiFi",
            "login_type": "bt_business",
            "username": "lawrence@berriescoffee.co.uk",
            "password": "luqian66",
            "portal_url": "https://ee-wifi.ee.co.uk/home"
        }
    ],
    "check_interval": 30,
    "max_retries": 1
}
```

### **Key Features**
- ✅ **Ethernet-only mode** - WiFi disabled
- ✅ **Automatic AP re-authentication** - Handles EE WiFi logouts
- ✅ **Same login credentials** - Uses your BT Business account
- ✅ **30-second monitoring** - Quick detection of issues
- ✅ **Headless operation** - Runs invisibly in background

## 🛠️ Troubleshooting

### **If Internet Stops Working**
1. Check Ethernet cable connection
2. Verify AP router is powered on
3. Check if AP router is connected to EE WiFi
4. Run test script: `python test_ethernet_connection.py`

### **If Auto-Login Fails**
1. Check your BT Business credentials in `wifi_config.json`
2. Verify EE WiFi portal is accessible
3. Check browser automation (ChromeDriver)
4. Look at logs in `internet_monitor.log`

### **To Re-enable WiFi**
```bash
# Re-enable WiFi adapter
netsh interface set interface "Wi-Fi" enable
```

## 📊 Monitoring

### **Log Files**
- `internet_monitor.log` - Main monitoring log
- `wifi_agent.log` - Captive portal login attempts
- `internet_logbook.log` - Connection history

### **Screenshots** (for debugging)
- `captive_portal_debug.png` - Captive portal page
- `after_submit_debug.png` - After login attempt

## 🎉 Benefits

1. **More Stable**: Ethernet connection is more reliable than WiFi
2. **Faster**: Direct connection to AP router
3. **Automatic**: No manual intervention needed for re-authentication
4. **Transparent**: Works in background without user interaction
5. **Same Credentials**: Uses your existing BT Business login

## 📞 Support

If you encounter issues:
1. Check the log files for error messages
2. Run the test script to verify setup
3. Ensure your AP router is properly configured
4. Verify your BT Business credentials are correct

Your system is now configured for **Ethernet + AP router** operation with automatic EE WiFi re-authentication! 🚀
