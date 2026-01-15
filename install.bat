@echo off
echo ====================================
echo   Desktop-Pokemon Install Script
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

echo [INFO] Python detected, installing dependencies...
echo.

REM Upgrade pip
echo [1/2] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [2/2] Installing project dependencies...
pip install -r requirements.txt

echo.
echo ====================================
echo   Installation Complete!
echo ====================================
echo.
echo Usage:
echo   1. Double-click run.bat to start
echo   2. Or run: python src\main.py
echo.

pause
