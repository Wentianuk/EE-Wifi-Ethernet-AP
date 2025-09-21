@echo off
echo Reconfiguring Beszel Agent for External Hub...
echo ==============================================

echo Your setup:
echo - Hub URL: https://node.n8n.best
echo - Your tunnel: beszel.190801.xyz -> localhost:45876
echo - Agent will connect to: https://node.n8n.best
echo.

echo Step 1: Stopping current service...
sc.exe stop beszel-agent
sc.exe delete beszel-agent

echo Step 2: Waiting for service removal...
timeout /t 3 /nobreak >nul

echo Step 3: Reinstalling with external hub configuration...
powershell -Command "Invoke-WebRequest -Uri 'https://get.beszel.dev' -OutFile '$env:TEMP\install-agent.ps1'; & Powershell -ExecutionPolicy Bypass -File '$env:TEMP\install-agent.ps1' -Port 45876 -Key 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIF9OBobJRD4e8H9+mV4KrpmyHsJ3MFhp1rZKcDqgo2Hk' -Token 'b2794628-6052-4134-9b9c-08c68f9843a6' -Url 'https://node.n8n.best'"

echo.
echo Configuration updated!
echo - Agent listening on: localhost:45876
echo - Agent connecting to: https://node.n8n.best
echo - Your tunnel: beszel.190801.xyz -> localhost:45876
echo.
echo The agent should now be visible in your hub at https://node.n8n.best!
pause
