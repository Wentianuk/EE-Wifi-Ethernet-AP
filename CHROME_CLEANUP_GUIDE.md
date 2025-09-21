# Chrome Process Cleanup Guide

## Problem Prevention

The WiFi agent can sometimes leave Chrome WebDriver processes running, which can cause connection issues and system resource problems. This guide explains how to prevent and resolve these issues.

## What Was Fixed

### 1. Improved WebDriver Cleanup
- Added proper `finally` blocks to ensure WebDriver cleanup even when errors occur
- Added force cleanup methods for stuck processes
- Added process monitoring before starting new WebDriver sessions

### 2. Process Monitoring
- WiFi agent now checks for stuck processes before starting
- Automatic cleanup when too many Chrome processes are detected
- Better error handling and logging

### 3. Cleanup Utilities
- Created multiple cleanup scripts for different scenarios
- Added monitoring capabilities for continuous process management

## Prevention Methods

### 1. Automatic Prevention (Built-in)
The WiFi agent now automatically:
- Checks for stuck processes before starting
- Cleans up WebDriver resources in `finally` blocks
- Monitors process counts and cleans up when needed

### 2. Manual Cleanup Scripts

#### Python Cleanup Script
```bash
# Check and clean up processes
python cleanup_chrome_processes.py --check

# Force cleanup
python cleanup_chrome_processes.py --check --force

# Start continuous monitoring
python cleanup_chrome_processes.py --monitor --interval 300
```

#### Batch Script (Windows)
```cmd
# Simple cleanup
cleanup_chrome.bat
```

#### PowerShell Script (Advanced)
```powershell
# Check and clean up
.\cleanup_chrome.ps1

# Force cleanup
.\cleanup_chrome.ps1 -Force

# Start monitoring
.\cleanup_chrome.ps1 -Monitor -CheckInterval 300
```

### 3. Scheduled Cleanup (Recommended)

Create a Windows Task Scheduler task to run cleanup periodically:

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to "Daily" or "At startup"
4. Set action to run: `python cleanup_chrome_processes.py --check`
5. Set working directory to your EE WiFi folder

### 4. Startup Script Integration

Add cleanup to your startup scripts:

```batch
@echo off
REM Clean up any stuck processes before starting
python cleanup_chrome_processes.py --check --force

REM Start the WiFi monitor
python internet_monitor.py
```

## Monitoring and Detection

### Signs of Chrome Process Issues
- WiFi agent fails to start
- Connection errors in logs
- High memory usage
- Multiple Chrome processes in Task Manager

### Process Count Thresholds
- **Normal**: 0-5 Chrome processes
- **Warning**: 6-10 Chrome processes
- **Critical**: 10+ Chrome processes (automatic cleanup triggered)

### Log Monitoring
Check these log files for issues:
- `wifi_agent.log` - WiFi agent activity
- `chrome_cleanup.log` - Cleanup utility activity
- `internet_monitor.log` - Monitor activity

## Troubleshooting

### If WiFi Agent Still Fails

1. **Manual Cleanup**:
   ```cmd
   taskkill /f /im chrome.exe
   taskkill /f /im chromedriver.exe
   ```

2. **Check Process Count**:
   ```cmd
   tasklist | findstr chrome
   ```

3. **Run Cleanup Script**:
   ```cmd
   python cleanup_chrome_processes.py --check --force
   ```

4. **Restart WiFi Agent**:
   ```cmd
   python wifi_hotspot_agent.py --debug
   ```

### If Issues Persist

1. Check Chrome installation
2. Update ChromeDriver
3. Check system resources
4. Review log files for specific errors

## Best Practices

### 1. Regular Maintenance
- Run cleanup script daily
- Monitor process counts
- Check log files weekly

### 2. System Monitoring
- Set up process monitoring alerts
- Monitor system memory usage
- Track WiFi agent success rates

### 3. Configuration
- Use headless mode for production
- Enable debug mode only when needed
- Set appropriate timeouts

## Files Created/Modified

### New Files
- `cleanup_chrome_processes.py` - Python cleanup utility
- `cleanup_chrome.bat` - Windows batch cleanup script
- `cleanup_chrome.ps1` - PowerShell cleanup script
- `CHROME_CLEANUP_GUIDE.md` - This guide

### Modified Files
- `wifi_hotspot_agent.py` - Added cleanup mechanisms
- `internet_monitor.py` - Added process cleanup before running agent

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python cleanup_chrome_processes.py --check` | Check and clean up processes |
| `python cleanup_chrome_processes.py --monitor` | Start continuous monitoring |
| `cleanup_chrome.bat` | Quick Windows cleanup |
| `.\cleanup_chrome.ps1 -Monitor` | PowerShell monitoring |
| `taskkill /f /im chrome.exe` | Emergency cleanup |

## Support

If you continue to experience issues:
1. Check the log files for specific error messages
2. Run the cleanup scripts manually
3. Verify Chrome and ChromeDriver are properly installed
4. Consider restarting the system if process issues persist
