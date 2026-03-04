@echo off
REM AegisLab — Open GitHub App configuration to fix Claude connector access
echo.
echo Opening GitHub App configuration...
echo.
echo 1. Find "Claude" in the list
echo 2. Click "Configure"
echo 3. Under "Repository access" - ensure Aegislab-doctoral-cyber-analytics is selected
echo 4. Or try "All repositories" temporarily
echo 5. Click Save
echo.
start https://github.com/settings/installations
echo.
echo See Claude_GitHub_Troubleshooting.md for full steps.
pause
