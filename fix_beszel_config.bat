@echo off
echo Fixing Beszel Agent Configuration...
echo ===================================

echo The agent is still trying to connect to localhost:8090
echo We need to fix this to connect to https://node.n8n.best
echo.

echo Step 1: Force stopping and removing service...
taskkill /F /IM beszel-agent.exe >nul 2>&1
sc.exe stop beszel-agent >nul 2>&1
sc.exe delete beszel-agent >nul 2>&1

echo Step 2: Waiting for cleanup...
timeout /t 5 /nobreak >nul

echo Step 3: Reinstalling with correct configuration...
echo - Hub URL: https://node.n8n.best
echo - Port: 45876
echo - Token: b2794628-6052-4134-9b9c-08c68f9843a6
echo.

powershell -Command "Invoke-WebRequest -Uri 'https://get.beszel.dev' -OutFile '$env:TEMP\install-agent.ps1'; & Powershell -ExecutionPolicy Bypass -File '$env:TEMP\install-agent.ps1' -Port 45876 -Key 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIF9OBobJRD4e8H9+mV4KrpmyHsJ3MFhp1rZKcDqgo2Hk' -Token 'b2794628-6052-4134-9b9c-08c68f9843a6' -Url 'https://node.n8n.best'"

echo.
echo Step 4: Waiting for service to start...
timeout /t 10 /nobreak >nul

echo Step 5: Checking service status...
sc.exe query beszel-agent

echo.
echo Configuration fix complete!
echo Check your hub at https://node.n8n.best
pause
