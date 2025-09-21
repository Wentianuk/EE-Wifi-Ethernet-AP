@echo off
echo Reconfiguring Beszel Agent for Cloudflare Tunnel...
echo ==================================================

echo Current setup:
echo - Your tunnel: beszel.190801.xyz -> localhost:45876
echo - Agent is trying to connect to: localhost:8090 (wrong!)
echo.

echo Step 1: Stopping current service...
sc.exe stop beszel-agent
sc.exe delete beszel-agent

echo Step 2: Waiting for service removal...
timeout /t 3 /nobreak >nul

echo Step 3: Reinstalling with correct configuration...
echo - Agent will listen on: localhost:45876
echo - Agent will connect to: beszel.190801.xyz (your tunnel)
echo.

powershell -Command "Invoke-WebRequest -Uri 'https://get.beszel.dev' -OutFile '$env:TEMP\install-agent.ps1'; & Powershell -ExecutionPolicy Bypass -File '$env:TEMP\install-agent.ps1' -Port 45876 -Key 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIF9OBobJRD4e8H9+mV4KrpmyHsJ3MFhp1rZKcDqgo2Hk' -Token 'b2794628-6052-4134-9b9c-08c68f9843a6' -Url 'https://beszel.190801.xyz'"

echo.
echo Configuration updated!
echo - Agent listening on: localhost:45876
echo - Agent connecting to: https://beszel.190801.xyz
echo - Your tunnel: beszel.190801.xyz -> localhost:45876
echo.
echo The agent should now be visible in your external hub!
pause
