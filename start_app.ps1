# Bank Transaction Analyzer - Quick Start Script
# Run this script to install dependencies and launch the app

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Bank Transaction Analyzer - Quick Start" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8+ from python.org" -ForegroundColor Red
    exit 1
}

# Check if Ollama is running
Write-Host ""
Write-Host "Checking Ollama..." -ForegroundColor Yellow
try {
    $ollamaCheck = ollama list 2>&1
    Write-Host "✓ Ollama is installed" -ForegroundColor Green
} catch {
    Write-Host "✗ Ollama not found. Please install from ollama.com" -ForegroundColor Red
    Write-Host "After installing, run: ollama pull qwen3" -ForegroundColor Yellow
    exit 1
}

# Check if virtual environment exists
Write-Host ""
Write-Host "Checking virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install/update dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

Write-Host ""
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Check if Ollama models are available
Write-Host ""
Write-Host "Checking Ollama models..." -ForegroundColor Yellow
$models = ollama list
if ($models -match "qwen3") {
    Write-Host "✓ qwen3 model found" -ForegroundColor Green
} else {
    Write-Host "! qwen3 model not found. Pulling it now..." -ForegroundColor Yellow
    ollama pull qwen3
}

# Launch the app
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Launching Bank Transaction Analyzer..." -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The app will open in your browser at http://localhost:8501" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the app" -ForegroundColor Yellow
Write-Host ""

streamlit run app.py
