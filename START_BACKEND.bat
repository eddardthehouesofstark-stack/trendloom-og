@echo off
echo ========================================
echo TrendLoom Backend Startup
echo ========================================
echo.

cd backend

echo [1/4] Checking Python...
python --version
if errorlevel 1 (
    echo Error: Python not found! Please install Python 3.11+
    pause
    exit /b 1
)
echo.

echo [2/4] Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists.
)
echo.

echo [3/4] Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo.

echo [4/4] Starting backend server...
echo.
echo ========================================
echo Backend will start on: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python -m app.main

pause
