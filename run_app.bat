@echo off
REM =====================================================
REM Gilead Vital Signs - Quick Run Script (Windows)
REM Winners Chapel International Arlington
REM Runs the app in a desktop window
REM =====================================================

echo Starting Gilead Vital Signs Medical Records...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Check if dependencies are installed, if not install them
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Installing dependencies for first run...
    pip install -r requirements_desktop.txt
)

REM Run the desktop app
python app_desktop.py

pause
