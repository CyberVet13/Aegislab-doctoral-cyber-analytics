@echo off
REM AegisLab — Start Workflow API (serves dashboard at http://127.0.0.1:8002)
cd /d "%~dp0"

echo ============================================
echo AegisLab — Starting...
echo ============================================
echo.

REM 1. Start Workflow API (dashboard served at root)
start "AegisLab" cmd /k "cd /d ""%~dp0Workflow_API"" && echo Dashboard: http://127.0.0.1:8002 && echo Press Ctrl+C to stop. && echo. && (py -3 app.py || python app.py)"

REM 2. API opens browser automatically when ready
echo.
echo Dashboard: http://127.0.0.1:8002
echo.
pause
