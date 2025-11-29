@echo off
echo ========================================
echo  Prompt Optimizer Frontend Launcher
echo  DEV VERSION - PORT 8081
echo ========================================
echo.

cd frontend

echo [1/2] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo Python found!
echo.

echo [2/2] Starting frontend server...
echo.
echo ========================================
echo  Frontend will open in 3 seconds...
echo  Frontend UI: http://localhost:8081
echo  
echo  NOTE: This is DEV version on port 8081
echo  Production runs on port 8080
echo  
echo  IMPORTANT: Make sure DEV backend is running!
echo  Start backend with: start_backend.bat (port 8001)
echo ========================================
echo.

timeout /t 3 /nobreak >nul

start http://localhost:8081

echo Server is starting...
echo Browser should open automatically
echo.
echo Press Ctrl+C to stop the server
echo.

python -m http.server 8081
