@echo off
echo Installing Beszel Agent (Client Only)...
echo =======================================

echo This will install the Beszel agent that can connect to:
echo - Remote Beszel hubs
echo - Beszel cloud services
echo - Any Beszel hub accessible via network
echo.

echo Step 1: Installing Beszel Agent...
powershell -Command "Invoke-WebRequest -Uri 'https://get.beszel.dev' -OutFile '$env:TEMP\install-agent.ps1'; & Powershell -ExecutionPolicy Bypass -File '$env:TEMP\install-agent.ps1' -Port 45876 -Key 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIF9OBobJRD4e8H9+mV4KrpmyHsJ3MFhp1rZKcDqgo2Hk' -Token 'b2794628-6052-4134-9b9c-08c68f9843a6' -Url 'http://localhost:8090'"

echo.
echo Installation complete!
echo.
echo NOTE: The agent is configured to connect to localhost:8090
echo If you want to connect to a different hub, you can:
echo 1. Edit the service configuration with: nssm edit beszel-agent
echo 2. Or reinstall with a different URL
echo.
echo The agent will start automatically and try to connect to the configured hub.
pause