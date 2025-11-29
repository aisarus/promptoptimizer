@echo off
echo ========================================
echo  Prompt Optimizer Backend Launcher
echo  DEV VERSION - PORT 8001
echo ========================================
echo.

cd backend

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo Python found!
echo.

echo [2/3] Installing dependencies...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo WARNING: Failed to install some dependencies
    echo Attempting to continue anyway...
)
echo Dependencies installed!
echo.

echo [3/3] Starting FastAPI server...
echo.
echo ========================================
echo  Server will start in 3 seconds...
echo  Swagger UI: http://localhost:8001/docs
echo  API Base:   http://localhost:8001/api
echo  
echo  NOTE: This is DEV version on port 8001
echo  Production runs on port 8000
echo ========================================
echo.

timeout /t 3 /nobreak >nul

start http://localhost:8001/docs

echo Server is starting...
echo Browser should open automatically with Swagger UI
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
