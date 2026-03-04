@echo off
REM Opens a NEW visible window to run the Workflow API (use if double-click doesn't show a window)
set "APIDIR=%~dp0"
start "AegisLab Workflow API" cmd /k "cd /d ""%APIDIR:~0,-1%"" && echo Workflow API: http://127.0.0.1:8002 && echo. && (py -3 app.py || python app.py || (echo ERROR: Python not found. && pause))"
