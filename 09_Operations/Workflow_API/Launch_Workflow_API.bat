@echo off
REM AegisLab Workflow API — Required for dashboard Upload to save files to 10_Input
REM If nothing happens when double-clicking, try Start_Workflow_API_NewWindow.bat instead.
cd /d "%~dp0"

echo ============================================
echo AegisLab Workflow API
echo ============================================
echo.
echo Starting on http://127.0.0.1:8002
echo Upload: POST /upload
echo.
echo Press Ctrl+C to stop.
echo ============================================
echo.

REM Try py (Python Launcher) first, then python
py -3 app.py 2>nul
if errorlevel 1 (
  python app.py 2>nul
  if errorlevel 1 (
    echo ERROR: Python not found. Install Python or add it to PATH.
    echo.
    echo Alternative: Right-click this file, choose "Run as administrator"
    echo Or try: Start_Workflow_API_NewWindow.bat
    echo.
    pause
    exit /b 1
  )
)

pause
