# Setup Internet Monitor Auto-Start
# This script creates a Windows Task Scheduler task to run the internet monitor on startup

param(
    [switch]$Force
)

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script requires Administrator privileges." -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
    Write-Host "Or right-click this script and select 'Run with PowerShell' as Administrator" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "Setting up Internet Monitor Auto-Start..." -ForegroundColor Cyan

# Get current directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$monitorScript = Join-Path $scriptPath "internet_monitor.py"
$pythonPath = (Get-Command python).Source

# Check if files exist
if (-not (Test-Path $monitorScript)) {
    Write-Host "Error: internet_monitor.py not found at $monitorScript" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $pythonPath)) {
    Write-Host "Error: Python not found in PATH" -ForegroundColor Red
    exit 1
}

Write-Host "Monitor script: $monitorScript" -ForegroundColor Green
Write-Host "Python path: $pythonPath" -ForegroundColor Green

# Create the task
$taskName = "EE WiFi Internet Monitor"
$taskDescription = "Automatically monitors internet connectivity and runs WiFi agent when needed"

try {
    # Remove existing task if it exists
    if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
        Write-Host "Removing existing task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    }

    # Create the action
    $action = New-ScheduledTaskAction -Execute $pythonPath -Argument "`"$monitorScript`"" -WorkingDirectory $scriptPath

    # Create the trigger (at startup)
    $trigger = New-ScheduledTaskTrigger -AtStartup

    # Create the principal (run as current user)
    $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType InteractiveToken

    # Create the settings
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

    # Register the task
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description $taskDescription

    Write-Host "✅ Task created successfully!" -ForegroundColor Green
    Write-Host "Task Name: $taskName" -ForegroundColor White
    Write-Host "The internet monitor will now start automatically when Windows boots." -ForegroundColor Green

    # Show task info
    Write-Host "`nTask Details:" -ForegroundColor Cyan
    Get-ScheduledTask -TaskName $taskName | Format-List TaskName, State, LastRunTime, NextRunTime

} catch {
    Write-Host "Error creating task: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`nSetup completed! The internet monitor will start automatically on next boot." -ForegroundColor Green
Write-Host "To test immediately, you can run the task manually from Task Scheduler." -ForegroundColor Yellow

pause
