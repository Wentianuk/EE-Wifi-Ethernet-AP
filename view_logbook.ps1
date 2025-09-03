# Internet Logbook Viewer
# This script provides easy access to view internet connectivity logs

param(
    [switch]$Report,
    [switch]$Events,
    [switch]$Today,
    [switch]$Export,
    [int]$Days = 7,
    [int]$EventCount = 20,
    [string]$ExportFile = "internet_connectivity_full_export.txt"
)

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "🌐 Internet Connectivity Logbook Viewer" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray

if ($Report) {
    Write-Host "Generating comprehensive report..." -ForegroundColor Yellow
    python internet_logbook.py --report --days $Days
} elseif ($Events) {
    Write-Host "Showing recent connectivity events..." -ForegroundColor Yellow
    python internet_logbook.py --events $EventCount
} elseif ($Today) {
    Write-Host "Today's connectivity summary..." -ForegroundColor Yellow
    python internet_logbook.py --report --days 1
} elseif ($Export) {
    Write-Host "Exporting all records to text file..." -ForegroundColor Yellow
    python internet_logbook.py --export --export-file $ExportFile
    if (Test-Path $ExportFile) {
        Write-Host "✅ Export completed: $ExportFile" -ForegroundColor Green
        Write-Host "File size: $((Get-Item $ExportFile).Length) bytes" -ForegroundColor Gray
    }
} else {
    Write-Host "Available options:" -ForegroundColor Green
    Write-Host "  -Report     : Generate comprehensive report" -ForegroundColor White
    Write-Host "  -Events     : Show recent connectivity events" -ForegroundColor White
    Write-Host "  -Today      : Show today's summary" -ForegroundColor White
    Write-Host "  -Export     : Export all records to text file" -ForegroundColor White
    Write-Host "  -Days N     : Number of days for report (default: 7)" -ForegroundColor White
    Write-Host "  -EventCount N : Number of events to show (default: 20)" -ForegroundColor White
    Write-Host "  -ExportFile : Export filename (default: internet_connectivity_full_export.txt)" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\view_logbook.ps1 -Report" -ForegroundColor White
    Write-Host "  .\view_logbook.ps1 -Events" -ForegroundColor White
    Write-Host "  .\view_logbook.ps1 -Today" -ForegroundColor White
    Write-Host "  .\view_logbook.ps1 -Export" -ForegroundColor White
    Write-Host "  .\view_logbook.ps1 -Report -Days 30" -ForegroundColor White
}
