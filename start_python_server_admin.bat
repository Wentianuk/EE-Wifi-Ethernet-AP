@echo off
echo Starting Python Web Server on Port 80
echo ====================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires Administrator privileges.
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo Step 1: Stopping nginx processes...
taskkill /IM nginx.exe /F
if %errorLevel% equ 0 (
    echo Nginx processes stopped successfully
) else (
    echo Nginx processes were not running or already stopped
)

echo.
echo Step 2: Waiting for port 80 to be released...
timeout /t 3 /nobreak >nul

echo.
echo Step 3: Starting Python web server on port 80...
cd /d "C:\Users\Berries\Documents\EE WIFI"
python kill_port80_and_start_server.py

echo.
echo If you see any errors, the server might not have started properly.
echo Check if port 80 is available and try again.
pause
