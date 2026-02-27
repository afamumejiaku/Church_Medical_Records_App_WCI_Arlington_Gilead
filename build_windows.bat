@echo off
REM =====================================================
REM Gilead Vital Signs - Windows Build Script
REM Winners Chapel International Arlington
REM Creates a standalone .exe file
REM =====================================================

echo.
echo ========================================
echo  Gilead Vital Signs - Desktop App Builder
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv build_env
call build_env\Scripts\activate.bat

echo.
echo [2/4] Installing dependencies...
pip install --upgrade pip
pip install -r requirements_desktop.txt

echo.
echo [3/4] Building executable...
pyinstaller VitalSigns.spec --clean

echo.
echo [4/4] Cleaning up...
rmdir /s /q build 2>nul
rmdir /s /q build_env 2>nul
del /q *.pyc 2>nul

echo.
echo ========================================
echo  BUILD COMPLETE!
echo ========================================
echo.
echo Your executable is located at:
echo   dist\VitalSigns.exe
echo.
echo You can copy VitalSigns.exe to any Windows
echo computer and run it without installing Python!
echo.
pause
