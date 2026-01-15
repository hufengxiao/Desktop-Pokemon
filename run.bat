@echo off
echo ====================================
echo   Desktop-Pokemon Launcher
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

echo [INFO] Starting Desktop-Pokemon...
echo.

REM Run the program
python src\main.py

pause
