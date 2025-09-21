@echo off
echo Starting Beszel Agent...
echo =======================

REM Set up environment variables
set LISTEN=45876
set KEY=ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIF9OBobJRD4e8H9+mV4KrpmyHsJ3MFhp1rZKcDqgo2Hk
set TOKEN=9d18416c-3318-4910-ac92-0cabd44e3db3
set HUB_URL=http://localhost:8090

echo Configuration:
echo - Listen Port: %LISTEN%
echo - Hub URL: %HUB_URL%
echo - Token: %TOKEN%
echo.

REM Check if beszel-agent.exe exists
if not exist "beszel-agent.exe" (
    echo ERROR: beszel-agent.exe not found!
    echo Please run install_beszel_windows.bat first
    pause
    exit /b 1
)

echo Starting Beszel Agent...
beszel-agent.exe -listen %LISTEN% -key "%KEY%" -token %TOKEN% -url %HUB_URL%

pause
