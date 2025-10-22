@echo off
echo ==================================================
echo Bank Transaction Analyzer - Quick Start
echo ==================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python not found. Please install Python 3.8+ from python.org
    pause
    exit /b 1
)
echo + Python found

echo.
echo Checking Ollama...
ollama list >nul 2>&1
if errorlevel 1 (
    echo X Ollama not found. Please install from ollama.com
    echo   After installing, run: ollama pull qwen3
    pause
    exit /b 1
)
echo + Ollama found

echo.
echo Setting up virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo + Virtual environment created
) else (
    echo + Virtual environment exists
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo + Setup complete!

echo.
echo ==================================================
echo Launching Bank Transaction Analyzer...
echo ==================================================
echo.
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the app
echo.

streamlit run app.py
