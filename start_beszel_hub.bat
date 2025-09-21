@echo off
echo Starting Beszel Hub...
echo =====================

echo Checking if Docker is installed...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not running!
    echo Please install Docker Desktop first.
    echo Download from: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo Docker is available. Starting Beszel Hub...
echo.

echo Creating data directories...
if not exist "beszel_data" mkdir beszel_data
if not exist "beszel_socket" mkdir beszel_socket

echo Starting Beszel Hub on port 8090...
docker-compose -f docker-compose-hub.yml up -d

echo.
echo Beszel Hub is starting...
echo Access it at: http://localhost:8090
echo.
echo Waiting for hub to be ready...
timeout /t 10 /nobreak >nul

echo Checking hub status...
curl -s http://localhost:8090 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Beszel Hub is running at http://localhost:8090
) else (
    echo ⏳ Hub is still starting up, please wait a moment...
)

echo.
echo You can now run the Beszel agent!
pause
