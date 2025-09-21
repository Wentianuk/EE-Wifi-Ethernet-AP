@echo off
echo Reinstalling Beszel Agent with new token...
echo ===========================================

echo Step 1: Stopping and removing old service...
sc.exe stop beszel-agent
sc.exe delete beszel-agent

echo Step 2: Waiting for service removal...
timeout /t 3 /nobreak >nul

echo Step 3: Installing with new token...
powershell -Command "Invoke-WebRequest -Uri 'https://get.beszel.dev' -OutFile '$env:TEMP\install-agent.ps1'; & Powershell -ExecutionPolicy Bypass -File '$env:TEMP\install-agent.ps1' -Port 45876 -Key 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIF9OBobJRD4e8H9+mV4KrpmyHsJ3MFhp1rZKcDqgo2Hk' -Token 'b2794628-6052-4134-9b9c-08c68f9843a6' -Url 'http://localhost:8090'"

echo.
echo Installation complete!
echo Check service status with: Get-Service beszel-agent
pause
