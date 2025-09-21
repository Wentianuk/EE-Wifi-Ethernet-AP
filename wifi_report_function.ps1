# WiFi Report PowerShell Function
# Add this to your PowerShell profile to use /wifi_report command

function wifi_report {
    param(
        [int]$Days = 7
    )
    
    # Change to the EE WIFI directory
    $originalLocation = Get-Location
    Set-Location "C:\Users\Berries\Documents\EE WIFI"
    
    try {
        # Run the Python script
        python wifi_report.py $Days
    } catch {
        Write-Host "Error running WiFi report: $($_.Exception.Message)" -ForegroundColor Red
    } finally {
        # Return to original location
        Set-Location $originalLocation
    }
}

# Create an alias for the /wifi_report command
Set-Alias -Name "/wifi_report" -Value wifi_report

Write-Host "WiFi Report command loaded! Use '/wifi_report [days]' to generate reports." -ForegroundColor Green
