# WiFi Disconnection Report Generator
# Usage: .\wifi_report.ps1 [days]

param(
    [int]$Days = 7
)

Write-Host "WiFi Disconnection Report Generator" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""

Write-Host "Generating report for the last $Days days..." -ForegroundColor Yellow
Write-Host ""

try {
    python wifi_report.py $Days
} catch {
    Write-Host "Error running Python script: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Make sure Python is installed and in your PATH" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Report complete!" -ForegroundColor Green
