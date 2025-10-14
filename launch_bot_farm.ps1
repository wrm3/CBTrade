# CBTrade Bot Farm Launcher
# Launch multiple bots in separate Windows Terminal tabs

Write-Host "CBTrade Bot Farm Launcher" -ForegroundColor Cyan
Write-Host "=" * 40

# Set UTF-8 for all processes
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

Write-Host "Launching Bot Farm..." -ForegroundColor Green

# Launch 1 Auto Mode Bot
Write-Host "Starting Auto Mode Bot..." -ForegroundColor Yellow
Start-Process "wt.exe" -ArgumentList @(
    "new-tab", 
    "--title", "CBTrade Auto Bot",
    "powershell.exe", 
    "-NoExit",
    "-Command", "cd '$PWD'; python run_bot_tracking.py a"
)

Start-Sleep 3

# Launch 6 Full Mode Bots
for ($i = 1; $i -le 6; $i++) {
    Write-Host "Starting Full Mode Bot $i..." -ForegroundColor Yellow
    Start-Process "wt.exe" -ArgumentList @(
        "new-tab",
        "--title", "CBTrade Full Bot $i", 
        "powershell.exe",
        "-NoExit", 
        "-Command", "cd '$PWD'; python run_bot_tracking.py f"
    )
    Start-Sleep 2
}

# Launch Web Server
Write-Host "Starting Web Server..." -ForegroundColor Yellow
Start-Process "wt.exe" -ArgumentList @(
    "new-tab",
    "--title", "CBTrade Web Server",
    "powershell.exe", 
    "-NoExit",
    "-Command", "cd '$PWD'; python run_web.py"
)

Write-Host ""
Write-Host "Bot Farm Deployment Complete!" -ForegroundColor Green
Write-Host "Running:" -ForegroundColor Cyan
Write-Host "  1 Auto Mode Bot" -ForegroundColor White
Write-Host "  6 Full Mode Bots" -ForegroundColor White  
Write-Host "  1 Web Server" -ForegroundColor White
Write-Host ""
Write-Host "Each bot has exit tracking enabled." -ForegroundColor Yellow
Write-Host "Check logs/bot_exit_events_*.json for phantom exit forensics." -ForegroundColor Yellow 