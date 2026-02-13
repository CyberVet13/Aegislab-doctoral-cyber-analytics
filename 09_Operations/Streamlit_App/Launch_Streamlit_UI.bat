@echo off
REM AegisLab Streamlit UI — double-click or run from terminal to start the app
cd /d "%~dp0"
echo Starting AegisLab Operational Console...
echo Open browser at http://localhost:8501
echo.
streamlit run app.py
pause
