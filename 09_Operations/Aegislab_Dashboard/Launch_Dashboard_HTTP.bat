@echo off
REM AegisLab Dashboard — Serve over HTTP and open in browser (fixes API/fetch issues)
cd /d "%~dp0"
echo Starting Dashboard server on http://127.0.0.1:8502
echo Dashboard will open in your browser.
echo Press Ctrl+C to stop.
echo.
py -3 serve_dashboard.py 2>nul || python serve_dashboard.py 2>nul || (echo Python not found. && pause)
