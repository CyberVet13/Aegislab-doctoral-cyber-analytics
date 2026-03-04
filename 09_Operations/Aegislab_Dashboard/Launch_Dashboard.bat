@echo off
REM AegisLab Dashboard — Open in default browser
cd /d "%~dp0"
echo Opening AegisLab Dashboard...
if not exist "%~dp0aegislab-dashboard.html" (
  echo ERROR: aegislab-dashboard.html not found.
  pause
  exit /b 1
)
REM Use explorer to open with default browser (more reliable from OneDrive)
explorer "%~dp0aegislab-dashboard.html"
