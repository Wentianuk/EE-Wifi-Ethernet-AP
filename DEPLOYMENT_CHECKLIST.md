# 📋 EE WiFi System - Deployment Checklist

Use this checklist to ensure complete and correct installation on fresh Windows systems.

## 🔧 Pre-Installation Requirements

### System Environment
- [ ] Windows 10/11 (64-bit)
- [ ] Administrator access available
- [ ] Stable internet connection for initial setup
- [ ] Ethernet connection to AP router (target setup)

### Software Prerequisites
- [ ] **Python 3.8+** installed ([python.org](https://python.org/downloads/))
  - [ ] "Add Python to PATH" option checked during installation
  - [ ] Verify: `python --version` shows 3.8+
  - [ ] Verify: `pip --version` works
- [ ] **Git for Windows** installed ([git-scm.com](https://git-scm.com/download/win))
  - [ ] Verify: `git --version` works
- [ ] **Google Chrome** browser installed
  - [ ] Launch Chrome once to complete initial setup

## 📥 Installation Process

### Repository Setup
- [ ] Navigate to installation directory: `cd C:\Users\%USERNAME%\Documents`
- [ ] Clone repository: `git clone [REPO_URL] "EE WIFI"`
- [ ] Enter directory: `cd "EE WIFI"`
- [ ] Verify files present: `dir` shows all core files

### Dependency Installation
- [ ] Run: `pip install -r requirements.txt`
- [ ] Verify key packages: `pip show selenium requests psutil`
- [ ] No error messages during installation

### Configuration Setup
- [ ] Create config: `copy wifi_config_template.json wifi_config.json`
- [ ] Edit `wifi_config.json` with BT Business credentials:
  ```json
  {
      "bt_business": {
          "username": "your-actual-email@domain.com",
          "password": "your-actual-password"
      }
  }
  ```
- [ ] **Security**: Verify `wifi_config.json` is in `.gitignore`
- [ ] **Security**: Never commit real credentials

### Auto-Start Configuration
- [ ] Run: `.\setup_autostart.bat`
- [ ] Verify scheduled task: `schtasks /query /tn "EE WiFi Monitor"`
- [ ] Verify startup shortcut exists in startup folder
- [ ] No error messages during setup

## 🧪 Testing and Verification

### Initial Testing
- [ ] **Monitor Test**: Run `python internet_monitor.py`
  - [ ] Shows "Configuration loaded from wifi_config.json"
  - [ ] Shows "Starting continuous internet monitoring"
  - [ ] Shows connectivity check results
  - [ ] Stop with Ctrl+C
- [ ] **Status Check**: Run `python check_monitor_status.py`
  - [ ] Shows configuration is OK
  - [ ] No critical errors displayed
- [ ] **Agent Test** (if behind captive portal): `python wifi_hotspot_agent.py`

### Production Deployment
- [ ] **Start Background**: Run `python start_continuous_monitor.py`
- [ ] **Verify Active**: Run `python check_monitor_status.py`
  - [ ] Shows "Monitor active"
  - [ ] Recent check timestamp visible
- [ ] **Check Logs**: `Get-Content internet_monitor.log -Tail 10`
  - [ ] Shows recent monitoring activity
  - [ ] No error messages

### Reboot Test (Critical)
- [ ] **Reboot System**: Restart Windows completely
- [ ] **Wait 15 minutes** for auto-start
- [ ] **Verify Auto-Start**: Run `python check_monitor_status.py`
  - [ ] Monitor shows as active
  - [ ] Recent activity logged
- [ ] **Check Auto-Start Logs**: Look for fresh startup sequence

## 📊 Performance Validation

### Expected Benchmarks
- [ ] **Auto-Start Time**: 10-15 minutes after reboot
- [ ] **Detection Speed**: 4-10 seconds for disconnection detection
- [ ] **Reconnection Time**: 60-75 seconds total duration
- [ ] **Chrome Preservation**: User browser sessions untouched
- [ ] **Success Rate**: >95% EE WiFi login success

### Performance Testing
- [ ] **Simulate Disconnection**: Briefly disconnect ethernet cable
- [ ] **Observe Response**: Monitor should detect within 30 seconds
- [ ] **Watch Reconnection**: Should complete within 75 seconds
- [ ] **Verify Logging**: Check logs show complete cycle with duration
- [ ] **Check Chrome**: Any existing Chrome windows remain open

## 🔍 Troubleshooting Verification

### Common Issue Prevention
- [ ] **PowerShell Execution Policy**: 
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- [ ] **Windows Defender**: Add project folder to exclusions if needed
- [ ] **Firewall**: Ensure Python and Chrome have network access
- [ ] **ChromeDriver**: System auto-downloads compatible version

### Error Resolution
- [ ] **Python PATH Issues**: Reinstall Python with PATH option
- [ ] **Permission Errors**: Run initial setup as Administrator
- [ ] **Network Issues**: Verify ethernet connectivity to AP router
- [ ] **Credential Issues**: Double-check BT Business login details

## ✅ Final Validation

### Deployment Success Criteria
- [ ] Monitor auto-starts reliably after reboot
- [ ] Disconnections detected within 10 seconds
- [ ] Reconnections complete within 75 seconds consistently
- [ ] Chrome browsing sessions preserved during reconnection
- [ ] Logs show clear [SUCCESS] messages
- [ ] No recurring error messages in logs
- [ ] System operates 24/7 without intervention

### Documentation Handover
- [ ] User knows how to check status: `python check_monitor_status.py`
- [ ] User knows how to view logs: `Get-Content internet_monitor.log -Tail 20`
- [ ] User knows how to restart: `python start_continuous_monitor.py`
- [ ] User has INSTALLATION_GUIDE.md for reference
- [ ] User understands credential security (never commit wifi_config.json)

## 🎯 Sign-Off

**Installation Completed By**: _________________

**Date**: _________________

**System Details**:
- Windows Version: _________________
- Python Version: _________________
- Installation Directory: _________________

**Performance Verified**:
- [ ] Auto-start working
- [ ] Reconnection time: _____ seconds (target: <75s)
- [ ] Chrome preservation confirmed
- [ ] 24/7 operation confirmed

**Next Review Date**: _________________

---

**🏆 Deployment Complete**: System ready for enterprise-grade 24/7 WiFi monitoring with sub-75 second recovery times and intelligent browser preservation.
