@echo off
echo ========================================
echo   TRENDLOOM BACKEND - LOCAL TEST
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.9 or higher
    pause
    exit /b 1
)
echo OK: Python found
echo.

echo [2/4] Installing dependencies...
cd backend
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo OK: Dependencies installed
echo.

echo [3/4] Starting backend server...
echo.
echo ========================================
echo   SERVER STARTING
echo ========================================
echo   URL: http://localhost:8000
echo   Docs: http://localhost:8000/docs
echo   Health: http://localhost:8000/api/health
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

start "" http://localhost:8000/docs

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
