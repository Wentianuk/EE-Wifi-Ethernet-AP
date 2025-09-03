# WiFi Monitor Auto-Start Setup Script
# This script sets up the WiFi monitor to start automatically on Windows startup

param(
    [switch]$Remove,
    [string]$Interval = 30,
    [switch]$Background = $true
)

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script requires Administrator privileges. Please run as Administrator." -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$MonitorScript = Join-Path $ScriptDir "start_monitor.ps1"
$TaskName = "WiFi Internet Monitor"

if ($Remove) {
    Write-Host "Removing auto-start task..." -ForegroundColor Yellow
    
    try {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
        Write-Host "Auto-start task removed successfully." -ForegroundColor Green
    } catch {
        Write-Host "Task may not exist or already removed." -ForegroundColor Yellow
    }
    
    exit 0
}

# Check if required files exist
if (-not (Test-Path $MonitorScript)) {
    Write-Host "Error: start_monitor.ps1 not found in current directory." -ForegroundColor Red
    exit 1
}

Write-Host "Setting up WiFi Monitor auto-start..." -ForegroundColor Cyan
Write-Host "Script directory: $ScriptDir" -ForegroundColor Gray
Write-Host "Monitor script: $MonitorScript" -ForegroundColor Gray

# Create the scheduled task action
$Action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$MonitorScript`" -Interval $Interval -Background"

# Create the scheduled task trigger (at startup)
$Trigger = New-ScheduledTaskTrigger -AtStartup

# Create the scheduled task settings
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

# Create the scheduled task principal (run as current user)
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

# Register the scheduled task
try {
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "Automatically starts WiFi Internet Monitor on Windows startup"
    
    Write-Host "✅ Auto-start task created successfully!" -ForegroundColor Green
    Write-Host "Task Name: $TaskName" -ForegroundColor Gray
    Write-Host "Check Interval: $Interval seconds" -ForegroundColor Gray
    Write-Host "Background Mode: $Background" -ForegroundColor Gray
    Write-Host "" -ForegroundColor White
    Write-Host "The WiFi monitor will now start automatically when Windows boots." -ForegroundColor Cyan
    Write-Host "To remove auto-start, run: .\setup_autostart.ps1 -Remove" -ForegroundColor Yellow
    
} catch {
    Write-Host "Error creating auto-start task: $_" -ForegroundColor Red
    exit 1
}

# Show current scheduled tasks
Write-Host "`nCurrent WiFi-related scheduled tasks:" -ForegroundColor Cyan
Get-ScheduledTask | Where-Object {$_.TaskName -like "*WiFi*" -or $_.TaskName -like "*Monitor*"} | Format-Table TaskName, State, LastRunTime -AutoSize
