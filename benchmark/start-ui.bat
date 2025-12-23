@echo off
:: CCO Benchmark - Calls PowerShell for proper environment handling
:: This fixes conda/pip PATH issues that occur in CMD
chcp 65001 >nul 2>&1
cd /d "%~dp0"
powershell -NoExit -ExecutionPolicy Bypass -File "%~dp0start-ui.ps1"
