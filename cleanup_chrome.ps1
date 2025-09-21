# Chrome Process Cleanup PowerShell Script
# This script helps prevent WiFi agent issues by cleaning up stuck Chrome processes

param(
    [switch]$Force,
    [switch]$Monitor,
    [int]$MaxProcesses = 5,
    [int]$CheckInterval = 300
)

function Get-ChromeProcesses {
    $chromeProcesses = Get-Process -Name "chrome" -ErrorAction SilentlyContinue
    $chromedriverProcesses = Get-Process -Name "chromedriver" -ErrorAction SilentlyContinue
    
    return @{
        Chrome = $chromeProcesses
        ChromeDriver = $chromedriverProcesses
        ChromeCount = $chromeProcesses.Count
        ChromeDriverCount = $chromedriverProcesses.Count
    }
}

function Remove-ChromeProcesses {
    param([bool]$ForceKill = $false)
    
    $killedCount = 0
    
    try {
        if ($ForceKill) {
            Stop-Process -Name "chrome" -Force -ErrorAction SilentlyContinue
            Stop-Process -Name "chromedriver" -Force -ErrorAction SilentlyContinue
        } else {
            Stop-Process -Name "chrome" -ErrorAction SilentlyContinue
            Stop-Process -Name "chromedriver" -ErrorAction SilentlyContinue
        }
        
        Start-Sleep -Seconds 2
        
        $remaining = Get-ChromeProcesses
        $killedCount = $MaxProcesses - $remaining.ChromeCount
        
        Write-Host "Cleaned up Chrome processes" -ForegroundColor Green
        return $killedCount
    }
    catch {
        Write-Host "Error cleaning up processes: $($_.Exception.Message)" -ForegroundColor Red
        return 0
    }
}

function Start-ChromeMonitoring {
    param([int]$Interval, [int]$MaxProcesses)
    
    Write-Host "Starting Chrome process monitoring (interval: ${Interval}s, max processes: ${MaxProcesses})" -ForegroundColor Cyan
    
    try {
        while ($true) {
            $processes = Get-ChromeProcesses
            
            Write-Host "Chrome processes: $($processes.ChromeCount), ChromeDriver processes: $($processes.ChromeDriverCount)" -ForegroundColor Yellow
            
            if ($processes.ChromeCount -gt $MaxProcesses -or $processes.ChromeDriverCount -gt 0) {
                Write-Host "Too many processes detected, cleaning up..." -ForegroundColor Yellow
                Remove-ChromeProcesses -ForceKill $Force
            } else {
                Write-Host "Process counts are normal" -ForegroundColor Green
            }
            
            Start-Sleep -Seconds $Interval
        }
    }
    catch {
        Write-Host "Monitoring stopped: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Main execution
Write-Host "Chrome Process Cleanup Utility" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

$processes = Get-ChromeProcesses

Write-Host "Found $($processes.ChromeCount) Chrome processes and $($processes.ChromeDriverCount) ChromeDriver processes" -ForegroundColor White

if ($Monitor) {
    Start-ChromeMonitoring -Interval $CheckInterval -MaxProcesses $MaxProcesses
} else {
    if ($processes.ChromeCount -gt $MaxProcesses -or $processes.ChromeDriverCount -gt 0) {
        Write-Host "Cleaning up processes..." -ForegroundColor Yellow
        Remove-ChromeProcesses -ForceKill $Force
    } else {
        Write-Host "No cleanup needed - process counts are normal" -ForegroundColor Green
    }
}

Write-Host "Cleanup completed!" -ForegroundColor Green
