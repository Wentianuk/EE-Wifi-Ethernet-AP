@echo off
echo Fixing Beszel Agent HUB_URL Configuration...
echo ===========================================

echo Current configuration shows:
echo - TOKEN: b2794628-6052-4134-9b9c-08c68f9843a6 (CORRECT)
echo - HUB_URL: http://localhost:8090 (WRONG - should be https://node.n8n.best)
echo.

echo Step 1: Stopping service...
sc.exe stop beszel-agent

echo Step 2: Updating HUB_URL to https://node.n8n.best...
"C:\Users\Berries\AppData\Local\Microsoft\WinGet\Packages\NSSM.NSSM_Microsoft.Winget.Source_8wekyb3d8bbwe\nssm-2.24-101-g897c7ad\win64\nssm.exe" set beszel-agent AppEnvironmentExtra "KEY=ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIF9OBobJRD4e8H9+mV4KrpmyHsJ3MFhp1rZKcDqgo2Hk" "TOKEN=b2794628-6052-4134-9b9c-08c68f9843a6" "HUB_URL=https://node.n8n.best"

echo Step 3: Starting service...
sc.exe start beszel-agent

echo.
echo Configuration updated!
echo - TOKEN: b2794628-6052-4134-9b9c-08c68f9843a6
echo - HUB_URL: https://node.n8n.best
echo.
echo The agent should now connect to your external hub!
echo Check your hub at https://node.n8n.best
pause
