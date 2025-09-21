@echo off
echo ================================================================
echo    EE WiFi Auto-Login System - Quick Installation Script
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed
    echo Please install Git for Windows from https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [INFO] Prerequisites check passed
echo.

REM Install Python dependencies
echo [STEP 1] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies
    pause
    exit /b 1
)
echo [SUCCESS] Python dependencies installed
echo.

REM Create configuration file
echo [STEP 2] Setting up configuration file...
if not exist wifi_config.json (
    copy wifi_config_template.json wifi_config.json
    echo [SUCCESS] Configuration template copied to wifi_config.json
    echo [ACTION REQUIRED] Please edit wifi_config.json with your BT Business credentials
) else (
    echo [INFO] wifi_config.json already exists
)
echo.

REM Setup auto-start
echo [STEP 3] Configuring auto-start...
call setup_autostart.bat
echo [SUCCESS] Auto-start configuration completed
echo.

REM Test installation
echo [STEP 4] Testing installation...
python check_monitor_status.py
echo.

echo ================================================================
echo                    INSTALLATION COMPLETE!
echo ================================================================
echo.
echo NEXT STEPS:
echo 1. Edit wifi_config.json with your BT Business credentials
echo 2. Test: python internet_monitor.py (Ctrl+C to stop)
echo 3. Start: python start_continuous_monitor.py
echo 4. Status: python check_monitor_status.py
echo.
echo The system will auto-start after the next reboot.
echo Expected performance: 61-65 second reconnection times
echo.
pause
