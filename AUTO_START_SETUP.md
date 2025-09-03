# WiFi Monitor Auto-Start Setup Guide

This guide shows you how to set up the WiFi Internet Monitor to start automatically when Windows boots. The system uses **Windows Task Scheduler** for reliable auto-start functionality.

**Current Implementation**: The project includes automated setup scripts that handle all the configuration automatically.

## 🚀 Auto-Start Setup (Scheduled Task Method)

### Using PowerShell Script (Recommended - Run as Administrator):
```powershell
# Set up auto-start with default 30-second interval
.\setup_autostart.ps1

# Set up with custom interval (15 seconds)
.\setup_autostart.ps1 -Interval 15

# Set up with custom interval (60 seconds)
.\setup_autostart.ps1 -Interval 60

# Remove auto-start
.\setup_autostart.ps1 -Remove
```

### Using Batch File (Alternative - Run as Administrator):
```cmd
# Set up auto-start
setup_autostart.bat

# Remove auto-start (manual command)
schtasks /delete /tn "WiFi Internet Monitor" /f
```

### What the Setup Script Does:
The `setup_autostart.ps1` script automatically:
1. **Creates a Windows Scheduled Task** named "WiFi Internet Monitor"
2. **Sets the trigger** to run at Windows startup
3. **Configures the action** to run the monitor with specified interval
4. **Sets proper permissions** for the current user
5. **Enables the task** to start automatically
6. **Provides removal option** with the `-Remove` parameter

**No manual configuration required** - the script handles everything automatically!

## 🚀 Manual Task Scheduler Setup (Alternative Method)

1. Open **Task Scheduler** (`taskschd.msc`)
2. Click **Create Basic Task**
3. Name: `WiFi Internet Monitor`
4. Trigger: **When the computer starts**
5. Action: **Start a program**
6. Program: `PowerShell.exe`
7. Arguments: `-WindowStyle Hidden -ExecutionPolicy Bypass -File "C:\Users\Berries\Documents\EE WIFI\start_monitor.ps1" -Interval 30 -Background`
8. Check **Run whether user is logged on or not**
9. Check **Run with highest privileges**

**Note**: This manual method is provided as an alternative. The automated `setup_autostart.ps1` script handles all these steps automatically.

## ✅ Verification

After setup, verify the auto-start is working:

### Check Scheduled Tasks:
```powershell
Get-ScheduledTask | Where-Object {$_.TaskName -like "*WiFi*"}
```

### Check Startup Folder:
```powershell
Get-ChildItem [Environment]::GetFolderPath("Startup")
```

### Test the Monitor:
```powershell
# Test once
.\start_monitor.ps1 -Once

# Test continuous (Ctrl+C to stop)
.\start_monitor.ps1
```

## 🔧 Configuration Options

### Monitor Intervals:
- **15 seconds**: Very responsive, more CPU usage
- **30 seconds**: Balanced (default)
- **60 seconds**: Less responsive, minimal CPU usage

### Background Mode:
- **Enabled**: Runs silently in background (recommended)
- **Disabled**: Shows console window

## 🛠️ Troubleshooting

### Common Issues:

1. **"Execution Policy" Error**:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **"Access Denied" Error**:
   - Run PowerShell as Administrator
   - Check file permissions

3. **Monitor Not Starting**:
   - Check `internet_monitor.log` for errors
   - Verify `wifi_config.json` exists and is configured
   - Test manually: `.\start_monitor.ps1 -Once`

4. **Task Not Running**:
   - Check Task Scheduler for the "WiFi Internet Monitor" task
   - Verify the task is enabled and set to run at startup
   - Check the task history for error messages
   - Re-run setup: `.\setup_autostart.ps1 -Remove` then `.\setup_autostart.ps1`

5. **Setup Script Issues**:
   - Ensure PowerShell execution policy allows scripts: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
   - Run PowerShell as Administrator
   - Check that all files are in the same directory

### Log Files:
- `internet_monitor.log` - Monitor activity
- `wifi_agent.log` - WiFi agent activity

## 🎯 Recommended Setup

For best results, use the **automated PowerShell script** with these settings:
- **Method**: `.\setup_autostart.ps1` (automated setup)
- **Interval**: 30 seconds (default, balanced performance)
- **Background**: Enabled (runs silently)
- **Run as**: Current user
- **Trigger**: At Windows startup

### Quick Setup Command:
```powershell
# Run as Administrator
.\setup_autostart.ps1
```

This provides reliable auto-start with minimal system impact and automatic configuration.
