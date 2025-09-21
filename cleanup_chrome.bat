@echo off
REM Chrome Process Cleanup Script
REM This script helps prevent WiFi agent issues by cleaning up stuck Chrome processes

echo Chrome Process Cleanup Utility
echo =============================

echo Checking for Chrome processes...

REM Check Chrome processes
tasklist /fi "imagename eq chrome.exe" | find /c "chrome.exe" > temp_count.txt
set /p chrome_count=<temp_count.txt
del temp_count.txt

REM Check ChromeDriver processes  
tasklist /fi "imagename eq chromedriver.exe" | find /c "chromedriver.exe" > temp_count.txt
set /p chromedriver_count=<temp_count.txt
del temp_count.txt

echo Found %chrome_count% Chrome processes and %chromedriver_count% ChromeDriver processes

if %chrome_count% gtr 5 (
    echo Too many Chrome processes detected! Cleaning up...
    taskkill /f /im chrome.exe
    echo Chrome processes cleaned up
) else (
    echo Chrome process count is normal
)

if %chromedriver_count% gtr 0 (
    echo ChromeDriver processes detected! Cleaning up...
    taskkill /f /im chromedriver.exe
    echo ChromeDriver processes cleaned up
) else (
    echo No ChromeDriver processes found
)

echo Cleanup completed!
pause
