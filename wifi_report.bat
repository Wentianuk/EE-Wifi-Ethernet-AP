@echo off
echo WiFi Disconnection Report Generator
echo ==================================
echo.

if "%1"=="" (
    echo Usage: wifi_report.bat [days]
    echo Example: wifi_report.bat 7
    echo Default: 7 days
    echo.
    set days=7
) else (
    set days=%1
)

echo Generating report for the last %days% days...
echo.

python wifi_report.py %days%

echo.
echo Report complete!
pause
