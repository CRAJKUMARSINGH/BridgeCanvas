@echo off
title BridgeCanvas - Bridge Design Desktop App
color 0A

echo ========================================
echo    BridgeCanvas - Bridge Design App
echo ========================================
echo.
echo Starting Bridge Design Desktop Application...
echo.
echo This app provides:
echo - Professional DXF bridge drawings
echo - Detailed pier and abutment geometry
echo - Cross-section plotting with real Excel data
echo - Advanced layout grid system
echo - User-friendly web interface
echo.
echo Please wait while the app loads...
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    echo.
    echo After installing Python, run this batch file again.
    echo.
    pause
    exit /b 1
)

echo ✅ Python found: 
python --version

REM Check if required packages are installed
echo.
echo Installing/updating required packages...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Warning: Some packages may not have installed correctly
    echo Continuing anyway...
) else (
    echo ✅ Required packages installed/updated
)

REM Create necessary directories
echo.
echo Setting up directories...
if not exist "generated" mkdir generated
if not exist "uploads" mkdir uploads
echo ✅ Directories ready

REM Run the main application
echo.
echo 🚀 Starting Bridge Design Application...
echo.
echo The web interface will open in your default browser.
echo If it doesn't open automatically, go to: http://localhost:5000
echo.
echo To stop the application, press Ctrl+C in this window.
echo.
echo ========================================
echo.

REM Start the Flask application
python main.py

echo.
echo ========================================
echo Application stopped. Press any key to exit...
echo ========================================
pause >nul
