@echo off
title BridgeCanvas - Streamlit Web App
color 0B

echo ========================================
echo    BridgeCanvas - Streamlit Web App
echo ========================================
echo.
echo Starting Bridge Design Web Application...
echo.
echo This web app provides:
echo - Easy-to-use web interface
echo - File upload and processing
echo - Real-time bridge design generation
echo - Professional DXF output
echo - Cross-section plotting with Excel data
echo.
echo Please wait while the web app loads...
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

REM Check if Streamlit is installed
echo.
echo Checking Streamlit installation...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing Streamlit...
    pip install streamlit >nul 2>&1
    if errorlevel 1 (
        echo ❌ ERROR: Failed to install Streamlit
        echo Please check your internet connection and try again.
        pause
        exit /b 1
    )
    echo ✅ Streamlit installed successfully
) else (
    echo ✅ Streamlit already installed
)

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
if not exist "streamlit_app\generated" mkdir streamlit_app\generated
if not exist "streamlit_app\uploads" mkdir streamlit_app\uploads
if not exist "streamlit_app\temp" mkdir streamlit_app\temp
echo ✅ Directories ready

REM Run the Streamlit application
echo.
echo 🚀 Starting Streamlit Web Application...
echo.
echo The web app will open in your default browser.
echo If it doesn't open automatically, go to: http://localhost:8501
echo.
echo To stop the web app, press Ctrl+C in this window.
echo.
echo ========================================
echo.

REM Start the Streamlit application
cd streamlit_app
streamlit run streamlit_app.py --server.port 8501 --server.headless false

echo.
echo ========================================
echo Web app stopped. Press any key to exit...
echo ========================================
pause >nul
