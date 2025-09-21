@echo off
echo Fixing Windows Firewall for Cloudflare Tunnel
echo =============================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires Administrator privileges.
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo Step 1: Creating firewall rule for HTTP Port 80...
netsh advfirewall firewall add rule name="HTTP Port 80 - Cloudflare Tunnel" dir=in action=allow protocol=TCP localport=80
if %errorLevel% equ 0 (
    echo HTTP Port 80 rule created successfully
) else (
    echo Failed to create HTTP Port 80 rule
)

echo.
echo Step 2: Creating firewall rule for HTTPS Port 443...
netsh advfirewall firewall add rule name="HTTPS Port 443 - Cloudflare Tunnel" dir=in action=allow protocol=TCP localport=443
if %errorLevel% equ 0 (
    echo HTTPS Port 443 rule created successfully
) else (
    echo Failed to create HTTPS Port 443 rule
)

echo.
echo Step 3: Creating firewall rule for Nginx...
netsh advfirewall firewall add rule name="Nginx Web Server" dir=in action=allow program="C:\nginx\nginx-1.24.0\nginx.exe"
if %errorLevel% equ 0 (
    echo Nginx firewall rule created successfully
) else (
    echo Failed to create Nginx rule
)

echo.
echo Step 4: Verifying firewall rules...
netsh advfirewall firewall show rule name="HTTP Port 80 - Cloudflare Tunnel"
netsh advfirewall firewall show rule name="HTTPS Port 443 - Cloudflare Tunnel"
netsh advfirewall firewall show rule name="Nginx Web Server"

echo.
echo Firewall configuration completed!
echo Your web server should now be accessible from external devices.
echo.
echo Test your website at: https://web.190801.xyz
echo.
pause
