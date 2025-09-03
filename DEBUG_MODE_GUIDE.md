# Debug Mode Guide

This guide explains how to toggle between invisible (production) and visible (debug) browser modes for troubleshooting and development.

## 🔍 Debug Mode Overview

The system supports two browser modes:
- **Production Mode (Default)**: Browser runs invisibly in the background
- **Debug Mode**: Browser runs visibly so you can see what's happening

## 🚀 How to Use Debug Mode

### WiFi Agent Debug Mode

Run the WiFi agent with visible browser for debugging:

```bash
# Debug mode - browser will be visible
python wifi_hotspot_agent.py --debug

# Production mode - browser runs invisibly (default)
python wifi_hotspot_agent.py
```

### Internet Monitor Debug Mode

Run the monitor with debug mode to see browser when WiFi agent is triggered:

```bash
# Debug mode - WiFi agent will run with visible browser
python internet_monitor.py --debug

# Production mode - WiFi agent runs invisibly (default)
python internet_monitor.py
```

### PowerShell Scripts with Debug Mode

You can also modify the PowerShell scripts to use debug mode:

```powershell
# Edit start_monitor.ps1 to add --debug flag
python internet_monitor.py --debug

# Or run directly with debug
python internet_monitor.py --debug --once
```

## 🎯 When to Use Debug Mode

### Use Debug Mode When:
- **Troubleshooting login issues** - See exactly what's happening on the login page
- **Testing new configurations** - Verify your credentials and settings work
- **Development** - When modifying the automation scripts
- **Captive portal issues** - Debug why login is failing
- **Network problems** - See if the browser can reach the login page

### Use Production Mode When:
- **Normal operation** - For regular automated WiFi connections
- **Background monitoring** - When you want the system to run silently
- **Auto-start** - For unattended operation
- **Performance** - Debug mode is slightly slower due to visible rendering

## 🔧 Debug Mode Features

### What You'll See in Debug Mode:
- **Browser window opens** - Chrome browser will be visible
- **Login process** - Watch the automated login steps
- **Page navigation** - See how the script navigates through pages
- **Element interaction** - Watch clicks, form filling, and button presses
- **Error messages** - See any browser errors or page issues

### What Happens in Production Mode:
- **No browser window** - Runs completely in background
- **Faster execution** - Optimized for speed
- **Lower resource usage** - No GUI rendering
- **Silent operation** - No visual distractions

## 🛠️ Debugging Tips

### 1. Check Browser Console
In debug mode, you can open Chrome DevTools (F12) to see:
- JavaScript errors
- Network requests
- Console messages
- Element inspection

### 2. Take Screenshots
The system automatically saves debug screenshots:
- `captive_portal_debug.png` - Initial login page
- `after_submit_debug.png` - After clicking submit

### 3. Monitor Logs
Check the log files for detailed information:
```bash
# View WiFi agent logs
Get-Content wifi_agent.log -Tail 20

# View monitor logs
Get-Content internet_monitor.log -Tail 20
```

### 4. Test Individual Components
```bash
# Test just the WiFi agent
python wifi_hotspot_agent.py --debug

# Test just connectivity check
python internet_monitor.py --once

# Test with custom config
python wifi_hotspot_agent.py --debug --config my_config.json
```

## 🚨 Common Debug Scenarios

### Scenario 1: Login Page Not Loading
**Symptoms**: Browser opens but page doesn't load
**Debug Steps**:
1. Run in debug mode: `python wifi_hotspot_agent.py --debug`
2. Check if you can see the EE WiFi login page
3. Look for network errors in browser console (F12)
4. Verify you're connected to the right WiFi network

### Scenario 2: Login Form Not Working
**Symptoms**: Page loads but login fails
**Debug Steps**:
1. Run in debug mode to see the form
2. Check if email/password fields are filled correctly
3. Verify the "Next" button is being clicked
4. Look for JavaScript errors in console

### Scenario 3: Captive Portal Not Detected
**Symptoms**: System thinks internet is available when it's not
**Debug Steps**:
1. Run monitor in debug mode: `python internet_monitor.py --debug`
2. Disconnect internet and watch the browser
3. See if the captive portal page appears
4. Check if the system detects the portal correctly

## 📊 Performance Comparison

| Mode | Browser Visibility | Speed | Resource Usage | Use Case |
|------|-------------------|-------|----------------|----------|
| Production | Invisible | Fast | Low | Normal operation |
| Debug | Visible | Slower | Higher | Troubleshooting |

## 🔄 Switching Between Modes

### Quick Switch Commands:
```bash
# Switch to debug mode
python wifi_hotspot_agent.py --debug

# Switch back to production mode
python wifi_hotspot_agent.py

# Monitor with debug mode
python internet_monitor.py --debug

# Monitor in production mode
python internet_monitor.py
```

### Permanent Configuration:
You can modify the default behavior by editing the scripts:
1. Change `headless=True` to `headless=False` in the code
2. Or always use the `--debug` flag

## 🎯 Best Practices

1. **Use production mode for normal operation**
2. **Switch to debug mode only when troubleshooting**
3. **Check logs first before using debug mode**
4. **Take screenshots in debug mode for documentation**
5. **Test in debug mode after configuration changes**
6. **Use debug mode to verify new WiFi networks**

## 🆘 Troubleshooting Debug Mode

### Debug Mode Not Working:
- Ensure Chrome browser is installed
- Check that chromedriver.exe is present
- Verify Python dependencies are installed
- Run with administrator privileges if needed

### Browser Not Opening:
- Check if another Chrome instance is running
- Kill existing Chrome processes: `taskkill /f /im chrome.exe`
- Restart the script

### Debug Mode Too Slow:
- This is normal - debug mode is slower than production
- Use production mode for regular operation
- Debug mode is only for troubleshooting

---

**Remember**: Debug mode is a powerful tool for troubleshooting, but use production mode for normal operation to get the best performance and user experience.
