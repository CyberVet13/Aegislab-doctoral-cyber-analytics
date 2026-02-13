@echo off
REM AegisLab n8n — double-click or run from terminal to start n8n
echo Starting n8n...
echo Open browser at http://localhost:5678
echo.

where npx >nul 2>&1
if %errorlevel% equ 0 (
    REM n8n 2.x: Execute Command node is disabled by default; enable it for AegisLab CLI
    set NODES_EXCLUDE=[]
    npx n8n
    goto :end
)

where docker >nul 2>&1
if %errorlevel% equ 0 (
    echo npx not found. Using Docker instead...
    docker run -e NODES_EXCLUDE="[]" -it --rm -p 5678:5678 n8nio/n8n
    goto :end
)

echo ERROR: npx is not recognized. Node.js is required to run n8n.
echo.
echo Fix: Install Node.js (LTS) from https://nodejs.org
echo      Then restart this launcher or reopen your terminal.
echo.
echo Alternative: If you have Docker, run: docker run -e NODES_EXCLUDE="[]" -it --rm -p 5678:5678 n8nio/n8n
echo.
pause
exit /b 1

:end
pause
