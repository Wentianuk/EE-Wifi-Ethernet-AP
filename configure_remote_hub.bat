@echo off
echo Configure Beszel Agent for Remote Hub
echo =====================================

echo Current configuration:
echo - Port: 45876
echo - SSH Key: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIF9OBobJRD4e8H9+mV4KrpmyHsJ3MFhp1rZKcDqgo2Hk
echo - Token: b2794628-6052-4134-9b9c-08c68f9843a6
echo - Hub URL: http://localhost:8090
echo.

set /p NEW_HUB_URL="Enter the remote hub URL (e.g., https://your-hub.com:8090): "

if "%NEW_HUB_URL%"=="" (
    echo No URL provided. Exiting.
    pause
    exit /b 1
)

echo.
echo Reinstalling with new hub URL: %NEW_HUB_URL%
echo.

powershell -Command "Invoke-WebRequest -Uri 'https://get.beszel.dev' -OutFile '$env:TEMP\install-agent.ps1'; & Powershell -ExecutionPolicy Bypass -File '$env:TEMP\install-agent.ps1' -Port 45876 -Key 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIF9OBobJRD4e8H9+mV4KrpmyHsJ3MFhp1rZKcDqgo2Hk' -Token 'b2794628-6052-4134-9b9c-08c68f9843a6' -Url '%NEW_HUB_URL%'"

echo.
echo Configuration updated!
echo The agent will now connect to: %NEW_HUB_URL%
pause
