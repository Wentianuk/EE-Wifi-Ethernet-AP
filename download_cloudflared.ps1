# Download cloudflared.exe for Windows
$cloudflaredUrl = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
$outputPath = ".\cloudflared.exe"

Write-Host "Downloading cloudflared.exe..."
try {
    Invoke-WebRequest -Uri $cloudflaredUrl -OutFile $outputPath
    Write-Host "Download completed successfully!"
    Write-Host "File saved to: $outputPath"
} catch {
    Write-Error "Failed to download cloudflared.exe: $($_.Exception.Message)"
    exit 1
}

# Verify the file was downloaded
if (Test-Path $outputPath) {
    $fileSize = (Get-Item $outputPath).Length
    Write-Host "File size: $fileSize bytes"
} else {
    Write-Error "cloudflared.exe was not downloaded successfully"
    exit 1
}
