@echo off
echo ========================================
echo  Prompt Optimizer - Full Launch
echo  DEV VERSION - PORTS 8001/8081
echo ========================================
echo.
echo This will start both Backend and Frontend
echo.
echo Backend will run on: http://localhost:8001
echo Frontend will run on: http://localhost:8081
echo.
echo NOTE: This is DEV version
echo Production runs on ports 8000/8080
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul
echo.

echo Starting Backend in new window...
start "Prompt Optimizer - Backend DEV" cmd /k "cd backend && echo Installing dependencies... && pip install -r requirements.txt --quiet && echo Starting FastAPI... && timeout /t 2 /nobreak >nul && start http://localhost:8001/docs && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001"

echo Waiting 8 seconds for backend to initialize...
timeout /t 8 /nobreak

echo.
echo Starting Frontend in new window...
start "Prompt Optimizer - Frontend DEV" cmd /k "cd frontend && echo Starting HTTP server... && timeout /t 2 /nobreak >nul && start http://localhost:8081 && python -m http.server 8081"

echo.
echo ========================================
echo  Both servers are starting!
echo  DEV VERSION
echo ========================================
echo.
echo Backend (Swagger): http://localhost:8001/docs
echo Frontend (UI):     http://localhost:8081
echo.
echo Two windows will open:
echo 1. Backend server window (port 8001)
echo 2. Frontend server window (port 8081)
echo.
echo Close this window or the server windows to stop.
echo.

pause
