@echo off
REM WiFi Report Command - Direct command line tool
REM Usage: wifi_report [days]

cd /d "C:\Users\Berries\Documents\EE WIFI"

if "%1"=="" (
    python wifi_report.py 7
) else (
    python wifi_report.py %1
)