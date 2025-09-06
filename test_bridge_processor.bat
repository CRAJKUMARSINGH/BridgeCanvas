@echo off
title BridgeCanvas - Test Bridge Processor
color 0E

echo ========================================
echo    BridgeCanvas - Test Bridge Processor
echo ========================================
echo.
echo Testing Bridge Design Processing...
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed
    pause
    exit /b 1
)

echo ✅ Python found: 
python --version

REM Test the bridge processor
echo.
echo 🧪 Testing Bridge Processor...
echo.

python -c "from bridge_processor import BridgeProcessor; print('✅ BridgeProcessor imported successfully')"

echo.
echo 🧪 Testing Excel file processing...
echo.

python -c "from bridge_processor import BridgeProcessor; bp = BridgeProcessor(); result = bp.process_excel_file('attached_assets/input.xlsx'); print('✅ Processing result: Success=' + str(result['success'])); print('✅ Variables count: ' + str(len(result['variables']))); print('✅ Key variables: CAPT=' + str(result['variables'].get('CAPT', 'Not found')) + ', LBRIDGE=' + str(result['variables'].get('LBRIDGE', 'Not found')))"

echo.
echo ========================================
echo Test completed! Press any key to exit...
echo ========================================
pause >nul
