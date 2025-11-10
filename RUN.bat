@echo off
title Tourism Guide FastAPI Server
color 0A

echo ========================================
echo   TOURISM GUIDE FASTAPI SERVER
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run SETUP.bat first to create the virtual environment.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if packages are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [ERROR] FastAPI not installed!
    echo.
    echo Please run SETUP.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

echo [INFO] Starting FastAPI server...
echo.
echo ========================================
echo   Server will start on:
echo   http://localhost:8000
echo.
echo   Access points:
echo   - Homepage: http://localhost:8000
echo   - Login: http://localhost:8000/login
echo   - Admin: http://localhost:8000/admin/dashboard
echo   - API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause