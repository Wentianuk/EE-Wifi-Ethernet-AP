@echo off
echo Installing Beszel Agent for Windows...
echo =====================================

REM Create data directory
if not exist "beszel_agent_data" mkdir beszel_agent_data

REM Download the latest Windows binary
echo Downloading Beszel Agent binary...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/henrygd/beszel/releases/latest/download/beszel-agent_windows_amd64.tar.gz' -OutFile 'beszel-agent.tar.gz'"

REM Extract the binary
echo Extracting binary...
powershell -Command "tar -xzf beszel-agent.tar.gz"

REM Set up environment variables
set LISTEN=45876
set KEY=ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIF9OBobJRD4e8H9+mV4KrpmyHsJ3MFhp1rZKcDqgo2Hk
set TOKEN=9d18416c-3318-4910-ac92-0cabd44e3db3
set HUB_URL=http://localhost:8090

echo Starting Beszel Agent...
echo Listening on port: %LISTEN%
echo Hub URL: %HUB_URL%

REM Start the agent
beszel-agent.exe -listen %LISTEN% -key "%KEY%" -token %TOKEN% -url %HUB_URL%

pause