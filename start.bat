@echo off
setlocal
cd /d "%~dp0"
echo ============================================
echo   Mobile Workbench  /  Vue + Flask
echo ============================================
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start.ps1"
set CODE=%ERRORLEVEL%
echo.
if not "%CODE%"=="0" echo [FAILED] Startup failed. Read the message above.
echo Press any key to close this window . . .
pause >nul
