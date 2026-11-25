@echo off
setlocal
cd /d "%~dp0"
echo Checking environment . . .
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start.ps1" -CheckOnly
echo.
echo Press any key to close this window . . .
pause >nul
