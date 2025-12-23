# CCO Benchmark - PowerShell Launcher
# Handles conda/pip environments properly

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "  +---------------------------------------+"
Write-Host "  |        CCO Benchmark v1.0            |"
Write-Host "  +---------------------------------------+"
Write-Host ""

# Set encoding for proper UTF-8 output
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
$env:NO_COLOR = "1"

# Find Python
$pythonCmd = $null

# Try py launcher
if (Get-Command "py" -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
    Write-Host "[OK] Found Python: py launcher"
}
# Try python in PATH
elseif (Get-Command "python" -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
    Write-Host "[OK] Found Python: python"
}
else {
    Write-Host "[ERROR] Python not found. Please install Python 3.10+"
    Write-Host ""
    Write-Host "  Options:"
    Write-Host "  1. Download from https://python.org/downloads"
    Write-Host "  2. Install via: winget install Python.Python.3.12"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check ccbox
if (-not (Get-Command "ccbox" -ErrorAction SilentlyContinue)) {
    Write-Host "[WARN] ccbox not found - benchmark tests will fail"
    Write-Host "       Install with: pip install ccbox"
}
else {
    Write-Host "[OK] Found ccbox"
}

# Check/install dependencies
Write-Host "[1/2] Checking dependencies..."
$fastapi = & $pythonCmd -m pip show fastapi 2>$null
if (-not $fastapi) {
    Write-Host "Installing dependencies..."
    & $pythonCmd -m pip install -r "$PSScriptRoot\requirements.txt" -q
}

# Start server
Write-Host "[2/2] Starting server..."
Write-Host ""
Write-Host "  Dashboard: http://localhost:8765"
Write-Host "  Press Ctrl+C to stop"
Write-Host ""

# Open browser after delay (background job)
Start-Job -ScriptBlock {
    Start-Sleep -Seconds 2
    Start-Process "http://localhost:8765"
} | Out-Null

# Run from parent directory
Set-Location "$PSScriptRoot\.."
& $pythonCmd -m benchmark
