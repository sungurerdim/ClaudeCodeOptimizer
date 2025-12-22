@echo off
title CCO Benchmark
cd /d "%~dp0"

echo.
echo  ╔═══════════════════════════════════════╗
echo  ║        CCO Benchmark v1.0             ║
echo  ╚═══════════════════════════════════════╝
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

:: Check/install dependencies
echo [1/2] Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt -q
)

:: Start server
echo [2/2] Starting server...
echo.
echo  Dashboard: http://localhost:8765
echo  Press Ctrl+C to stop
echo.

python -m benchmark

pause
