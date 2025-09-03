@echo off
REM WiFi Internet Monitor Startup Script (Batch)
REM This script starts the internet connectivity monitor

setlocal enabledelayedexpansion

REM Get the script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.7+ and ensure it's in your PATH.
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "internet_monitor.py" (
    echo Error: internet_monitor.py not found in current directory.
    pause
    exit /b 1
)

if not exist "wifi_hotspot_agent.py" (
    echo Error: wifi_hotspot_agent.py not found in current directory.
    pause
    exit /b 1
)

if not exist "wifi_config.json" (
    echo Warning: Configuration file wifi_config.json not found.
    echo Please copy wifi_config_template.json to wifi_config.json and configure it.
    echo.
)

echo Starting WiFi Internet Monitor...
echo Press Ctrl+C to stop.
echo.

REM Run the monitor
python internet_monitor.py --config wifi_config.json --interval 30

echo.
echo Monitor finished.
pause
