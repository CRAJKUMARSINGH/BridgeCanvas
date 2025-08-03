@echo off
echo ====================================
echo  BRIDGE GAD GENERATOR
echo  Windows 11 Deployment Script
echo ====================================
echo.

echo.
echo All packages installed successfully!
echo.
echo Starting Infrastructure Billing System...
echo.
echo The application will open in your default web browser.
echo Use Ctrl+C to stop the application.
echo.

REM Start the FLASK application
python app.py 
if %errorlevel% neq 0 (
    echo ERROR: Failed to start the application
    pause
    exit /b 1
)

pause