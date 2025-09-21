@echo off
echo Cloudflared Service Reinstall Script
echo =====================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires Administrator privileges.
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo Step 1: Stopping existing Cloudflared service...
net stop "Cloudflared" 2>nul
if %errorLevel% equ 0 (
    echo Service stopped successfully.
) else (
    echo Service was not running or already stopped.
)

echo.
echo Step 2: Uninstalling existing Cloudflared service...
"%~dp0cloudflared.exe" service uninstall
if %errorLevel% equ 0 (
    echo Service uninstalled successfully.
) else (
    echo Service uninstall completed (may have already been uninstalled).
)

echo.
echo Waiting for cleanup...
timeout /t 2 /nobreak >nul

echo.
echo Step 3: Installing Cloudflared service with new token...
"%~dp0cloudflared.exe" service install eyJhIjoiZTEzNDU3NDVmMTI2YTRjNTYwZjJmNmYzZjU2ZDJiMmQiLCJ0IjoiNDZlODc0NjAtMWFhMy00OWRkLThiYWEtNjZhYjZlZTBlN2Q0IiwicyI6Ik5ETTRObVkyTnprdE1UVmpZUzAwTmpOakxUbGhNRGt0TnpaaVpqTXpNV0ZqWkRJMSJ9
if %errorLevel% neq 0 (
    echo Failed to install service.
    pause
    exit /b 1
)
echo Service installed successfully with tunnel token.

echo.
echo Step 4: Starting the service...
net start "Cloudflared"
if %errorLevel% equ 0 (
    echo Service started successfully.
) else (
    echo Failed to start service.
    pause
    exit /b 1
)

echo.
echo Step 5: Verifying service status...
sc query "Cloudflared"

echo.
echo Cloudflared service has been successfully reinstalled and is running!
echo Your tunnel token has been configured and the service will start automatically on boot.
echo.
pause
