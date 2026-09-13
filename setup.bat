@echo off
REM setup.bat — Clean environment setup for Windows
REM Usage: setup.bat

echo === Inventory Management System — Setup ===

REM 1. Check Python
python --version || (echo "Python not found. Install Python 3.10+." && exit /b 1)

REM 2. Create virtual environment
echo Creating virtual environment...
python -m venv .venv

REM 3. Activate and install
echo Installing dependencies...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q

REM 4. Copy env template
if not exist .env (
    copy .env.example .env
    echo .env created from .env.example — please review settings.
)

REM 5. Smoke test
echo Running smoke tests...
python -m pytest test_app.py tests/ -q --tb=short

echo.
echo Setup complete. Run: python main.py
