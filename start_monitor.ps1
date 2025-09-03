# WiFi Internet Monitor Startup Script
# This script starts the internet connectivity monitor with various options

param(
    [int]$Interval = 30,
    [switch]$Once,
    [switch]$Background,
    [string]$Config = "wifi_config.json"
)

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python not found. Please install Python 3.7+ and ensure it's in your PATH." -ForegroundColor Red
    exit 1
}

# Check if required files exist
if (-not (Test-Path "internet_monitor.py")) {
    Write-Host "Error: internet_monitor.py not found in current directory." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "wifi_hotspot_agent.py")) {
    Write-Host "Error: wifi_hotspot_agent.py not found in current directory." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $Config)) {
    Write-Host "Warning: Configuration file $Config not found." -ForegroundColor Yellow
    Write-Host "Please copy wifi_config_template.json to $Config and configure it." -ForegroundColor Yellow
}

# Build the Python command
$pythonArgs = @("internet_monitor.py", "--config", $Config, "--interval", $Interval)

if ($Once) {
    $pythonArgs += "--once"
    Write-Host "Running single connectivity check..." -ForegroundColor Cyan
} elseif ($Background) {
    $pythonArgs += "--background"
    Write-Host "Starting background monitoring..." -ForegroundColor Cyan
} else {
    Write-Host "Starting continuous monitoring (interval: $Interval seconds)..." -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow
}

# Run the monitor
try {
    if ($Background) {
        # Start in background
        Start-Process python -ArgumentList $pythonArgs -WindowStyle Hidden
        Write-Host "Monitor started in background. Check internet_monitor.log for output." -ForegroundColor Green
    } else {
        # Run in foreground
        python $pythonArgs
    }
} catch {
    Write-Host "Error running internet monitor: $_" -ForegroundColor Red
    exit 1
}

Write-Host "Monitor finished." -ForegroundColor Green
