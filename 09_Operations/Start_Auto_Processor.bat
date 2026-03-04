@echo off
REM AegisLab Auto-Processor — Monitor 10_Input, trigger agents on new files
cd /d "%~dp0"
echo ============================================================
echo    AEGISLAB AUTO-PROCESSOR
echo ============================================================
echo.
echo Installing watchdog if needed...
pip install watchdog -q
echo.
python aegislab_auto_processor.py
pause
