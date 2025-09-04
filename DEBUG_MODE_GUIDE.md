# 🔍 Debug Mode Guide

## Overview
Debug mode allows you to see the browser window during the login process, making it easier to troubleshoot issues with the EE WiFi captive portal authentication.

## 🚀 Quick Start

### Enable Debug Mode
```bash
python toggle_debug_mode.py
```

### Test Visible Browser
```bash
python test_visible_browser.py
```

### Run Full Monitor in Debug Mode
```bash
python internet_monitor.py
```

## ⚙️ Configuration

Your `wifi_config.json` now includes debug settings:

```json
{
    "debug_mode": true,
    "headless_browser": false
}
```

- **`debug_mode: true`** - Enables debug logging and visible browser
- **`headless_browser: false`** - Shows browser window (set to `true` for hidden mode)

## 🔍 What You'll See

When debug mode is enabled, you'll see:

1. **Browser Window Opens** - Chrome browser becomes visible
2. **Navigation to EE WiFi Portal** - Goes to `https://ee-wifi.ee.co.uk/home`
3. **Cookie Acceptance** - Clicks "Accept all cookies" button
4. **Login Button** - Clicks "Log in now" button
5. **BT Business Tab** - Selects "BT Business Broadband" tab
6. **Submit Button** - Clicks the submit button
7. **Username/Password Fields** - Fills in your credentials
8. **Final Submit** - Completes the login process

## 🛠️ Debugging Tips

### Watch for These Issues:
- **Page doesn't load** - Check internet connection
- **Elements not found** - EE WiFi portal may have changed
- **Login fails** - Verify your BT Business credentials
- **Browser crashes** - Check ChromeDriver compatibility

### Screenshots
The system automatically saves screenshots:
- `captive_portal_debug.png` - Initial portal page
- `after_submit_debug.png` - After clicking submit

### Log Files
Check these files for detailed information:
- `wifi_agent.log` - Browser automation logs
- `internet_monitor.log` - Connection monitoring logs

## 🔄 Toggle Debug Mode

### Method 1: Using the Toggle Script
```bash
python toggle_debug_mode.py
```

### Method 2: Manual Edit
Edit `wifi_config.json`:
```json
{
    "debug_mode": true,        // Set to false to disable
    "headless_browser": false  // Set to true for hidden mode
}
```

## 🎯 Testing Scenarios

### Test 1: Manual Trigger
```bash
python test_visible_browser.py
```
This runs the WiFi agent once in visible mode.

### Test 2: Full Monitoring
```bash
python internet_monitor.py
```
This runs continuous monitoring with visible browser when needed.

### Test 3: Single Check
```bash
python internet_monitor.py --once
```
This runs one connectivity check and triggers browser if needed.

## 🚨 Troubleshooting

### Browser Doesn't Open
- Check if Chrome is installed
- Verify ChromeDriver is working
- Check for antivirus blocking

### Login Process Fails
- Watch the browser window for error messages
- Check if EE WiFi portal has changed
- Verify your credentials are correct

### Browser Opens But Doesn't Navigate
- Check internet connectivity
- Verify the portal URL is accessible
- Check for proxy/firewall issues

## 📊 Debug Output

When debug mode is enabled, you'll see:
```
2025-09-03 17:30:00 - INFO - Debug mode enabled - browser will be visible
2025-09-03 17:30:01 - INFO - Running browser in visible mode for debugging
2025-09-03 17:30:02 - INFO - Current URL: https://ee-wifi.ee.co.uk/home
2025-09-03 17:30:03 - INFO - Clicked cookie acceptance button
2025-09-03 17:30:04 - INFO - Clicked login button
2025-09-03 17:30:05 - INFO - Clicked BT Business tab
2025-09-03 17:30:06 - INFO - Clicked submit button using selector: //input[@id='submit-btb']
```

## 🎉 Benefits of Debug Mode

1. **Visual Feedback** - See exactly what's happening
2. **Error Identification** - Spot issues immediately
3. **Process Verification** - Confirm each step works
4. **Troubleshooting** - Easier to diagnose problems
5. **Learning** - Understand how the automation works

## 🔒 Security Note

Debug mode shows your login process in a visible browser window. Make sure you're in a private environment when using debug mode to protect your credentials.

---

**Ready to debug?** Run `python test_visible_browser.py` to see the login process in action! 🚀