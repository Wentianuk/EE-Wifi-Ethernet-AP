# Reinstall Cloudflared Service Script
# Run this script as Administrator

param(
    [Parameter(Mandatory=$true)]
    [string]$TunnelToken
)

Write-Host "Cloudflared Service Reinstall Script" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "This script requires Administrator privileges. Please run PowerShell as Administrator and try again."
    exit 1
}

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CloudflaredPath = Join-Path $ScriptDir "cloudflared.exe"

# Check if cloudflared.exe exists
if (-not (Test-Path $CloudflaredPath)) {
    Write-Error "cloudflared.exe not found at: $CloudflaredPath"
    exit 1
}

Write-Host "Step 1: Stopping existing Cloudflared service..." -ForegroundColor Yellow
try {
    Stop-Service -Name "Cloudflared" -Force -ErrorAction SilentlyContinue
    Write-Host "Service stopped successfully." -ForegroundColor Green
} catch {
    Write-Host "Service was not running or already stopped." -ForegroundColor Yellow
}

Write-Host "Step 2: Uninstalling existing Cloudflared service..." -ForegroundColor Yellow
try {
    & $CloudflaredPath service uninstall
    Write-Host "Service uninstalled successfully." -ForegroundColor Green
} catch {
    Write-Host "Service uninstall completed (may have already been uninstalled)." -ForegroundColor Yellow
}

# Wait a moment for cleanup
Start-Sleep -Seconds 2

Write-Host "Step 3: Installing Cloudflared service with new token..." -ForegroundColor Yellow
try {
    & $CloudflaredPath service install $TunnelToken
    Write-Host "Service installed successfully with tunnel token." -ForegroundColor Green
} catch {
    Write-Error "Failed to install service: $($_.Exception.Message)"
    exit 1
}

Write-Host "Step 4: Starting the service..." -ForegroundColor Yellow
try {
    Start-Service -Name "Cloudflared"
    Write-Host "Service started successfully." -ForegroundColor Green
} catch {
    Write-Error "Failed to start service: $($_.Exception.Message)"
    exit 1
}

Write-Host "Step 5: Verifying service status..." -ForegroundColor Yellow
$ServiceStatus = Get-Service -Name "Cloudflared"
Write-Host "Service Status: $($ServiceStatus.Status)" -ForegroundColor Green
Write-Host "Service Name: $($ServiceStatus.Name)" -ForegroundColor Green
Write-Host "Display Name: $($ServiceStatus.DisplayName)" -ForegroundColor Green

Write-Host "`nCloudflared service has been successfully reinstalled and is running!" -ForegroundColor Green
Write-Host "Your tunnel token has been configured and the service will start automatically on boot." -ForegroundColor Green
