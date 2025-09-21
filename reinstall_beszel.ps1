# Reinstall Beszel Agent with new token
Write-Host "Reinstalling Beszel Agent with new token..." -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

Write-Host "Step 1: Stopping and removing old service..." -ForegroundColor Yellow
try {
    Stop-Service beszel-agent -Force -ErrorAction SilentlyContinue
    sc.exe delete beszel-agent
    Write-Host "Old service removed successfully" -ForegroundColor Green
} catch {
    Write-Host "Service removal completed (may have already been removed)" -ForegroundColor Yellow
}

Write-Host "Step 2: Waiting for service removal..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "Step 3: Installing with new token..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri 'https://get.beszel.dev' -OutFile "$env:TEMP\install-agent.ps1"
    & Powershell -ExecutionPolicy Bypass -File "$env:TEMP\install-agent.ps1" -Port 45876 -Key "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIF9OBobJRD4e8H9+mV4KrpmyHsJ3MFhp1rZKcDqgo2Hk" -Token "b2794628-6052-4134-9b9c-08c68f9843a6" -Url "http://localhost:8090"
    Write-Host "Installation completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error during installation: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Check service status with: Get-Service beszel-agent" -ForegroundColor Cyan
