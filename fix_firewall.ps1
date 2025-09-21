# Fix Windows Firewall for Cloudflare Tunnel
# Run this script as Administrator

Write-Host "🔧 Fixing Windows Firewall for Cloudflare Tunnel" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "This script requires Administrator privileges. Please run PowerShell as Administrator and try again."
    exit 1
}

Write-Host "Step 1: Creating firewall rule for HTTP Port 80..." -ForegroundColor Yellow
try {
    # Remove existing rule if it exists
    Remove-NetFirewallRule -DisplayName "HTTP Port 80 - Cloudflare Tunnel" -ErrorAction SilentlyContinue
    
    # Create new rule for port 80
    New-NetFirewallRule -DisplayName "HTTP Port 80 - Cloudflare Tunnel" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow -Profile Any
    Write-Host "✅ HTTP Port 80 rule created successfully" -ForegroundColor Green
} catch {
    Write-Error "Failed to create HTTP Port 80 rule: $($_.Exception.Message)"
    exit 1
}

Write-Host "Step 2: Creating firewall rule for HTTPS Port 443..." -ForegroundColor Yellow
try {
    # Remove existing rule if it exists
    Remove-NetFirewallRule -DisplayName "HTTPS Port 443 - Cloudflare Tunnel" -ErrorAction SilentlyContinue
    
    # Create new rule for port 443
    New-NetFirewallRule -DisplayName "HTTPS Port 443 - Cloudflare Tunnel" -Direction Inbound -Protocol TCP -LocalPort 443 -Action Allow -Profile Any
    Write-Host "✅ HTTPS Port 443 rule created successfully" -ForegroundColor Green
} catch {
    Write-Error "Failed to create HTTPS Port 443 rule: $($_.Exception.Message)"
    exit 1
}

Write-Host "Step 3: Creating firewall rule for Nginx..." -ForegroundColor Yellow
try {
    # Remove existing rule if it exists
    Remove-NetFirewallRule -DisplayName "Nginx Web Server" -ErrorAction SilentlyContinue
    
    # Create rule for nginx.exe
    $nginxPath = "C:\nginx\nginx-1.24.0\nginx.exe"
    if (Test-Path $nginxPath) {
        New-NetFirewallRule -DisplayName "Nginx Web Server" -Direction Inbound -Program $nginxPath -Action Allow -Profile Any
        Write-Host "✅ Nginx firewall rule created successfully" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Nginx not found at expected path, skipping nginx-specific rule" -ForegroundColor Yellow
    }
} catch {
    Write-Error "Failed to create Nginx rule: $($_.Exception.Message)"
}

Write-Host "Step 4: Verifying firewall rules..." -ForegroundColor Yellow
$rules = Get-NetFirewallRule -DisplayName "*Cloudflare*", "*HTTP Port 80*", "*HTTPS Port 443*", "*Nginx*" | Where-Object {$_.Enabled -eq $true}
if ($rules) {
    Write-Host "✅ Active firewall rules:" -ForegroundColor Green
    $rules | ForEach-Object { Write-Host "  - $($_.DisplayName)" -ForegroundColor Cyan }
} else {
    Write-Host "⚠️ No matching firewall rules found" -ForegroundColor Yellow
}

Write-Host "`n🎉 Firewall configuration completed!" -ForegroundColor Green
Write-Host "Your web server should now be accessible from external devices." -ForegroundColor Green
Write-Host "`nTest your website at: https://web.190801.xyz" -ForegroundColor Cyan
