@echo off
REM WiFi Monitor Auto-Start Setup Script (Batch)
REM This script sets up the WiFi monitor to start automatically on Windows startup

setlocal enabledelayedexpansion

REM Check if running as Administrator
net session >nul 2>&1
if errorlevel 1 (
    echo Error: This script requires Administrator privileges.
    echo Please right-click and select "Run as Administrator"
    pause
    exit /b 1
)

REM Get the script directory
set "SCRIPT_DIR=%~dp0"
set "MONITOR_SCRIPT=%SCRIPT_DIR%start_monitor.bat"
set "TASK_NAME=WiFi Internet Monitor"

echo Setting up WiFi Monitor auto-start...
echo Script directory: %SCRIPT_DIR%
echo Monitor script: %MONITOR_SCRIPT%

REM Check if required files exist
if not exist "%MONITOR_SCRIPT%" (
    echo Error: start_monitor.bat not found in current directory.
    pause
    exit /b 1
)

REM Create the scheduled task
schtasks /create /tn "%TASK_NAME%" /tr "\"%MONITOR_SCRIPT%\"" /sc onstart /ru "%USERNAME%" /f

if errorlevel 1 (
    echo Error creating auto-start task.
    pause
    exit /b 1
)

echo.
echo ✅ Auto-start task created successfully!
echo Task Name: %TASK_NAME%
echo.
echo The WiFi monitor will now start automatically when Windows boots.
echo To remove auto-start, run: schtasks /delete /tn "%TASK_NAME%" /f
echo.

REM Show current scheduled tasks
echo Current WiFi-related scheduled tasks:
schtasks /query /fo table | findstr /i "wifi\|monitor"

pause
