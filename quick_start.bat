@echo off
REM Invoice Management System - Quick Start Script (Windows)
REM This script sets up and runs the application

echo ========================================
echo Invoice Management System - Quick Start
echo ========================================
echo.

REM Check Python
echo Checking Python version...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.9 or higher.
    pause
    exit /b 1
)
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo Dependencies installed
echo.

REM Setup environment file
if not exist ".env" (
    echo Setting up environment file...
    copy .env.example .env
    echo .env file created (please edit with your settings)
    echo.
) else (
    echo .env file already exists
    echo.
)

REM Create necessary directories
echo Creating directories...
if not exist "database" mkdir database
if not exist "static\uploads" mkdir static\uploads
if not exist "static\invoices" mkdir static\invoices
echo Directories created
echo.

REM Initialize database
echo Initializing database...
python init_db.py
echo.

REM Run the application
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Starting the application...
echo Visit http://localhost:5000 in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
