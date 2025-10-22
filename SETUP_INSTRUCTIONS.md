# Bank Transaction Analyzer - Setup Instructions

## Overview

This is a fully local desktop application for processing and classifying bank transactions. All data stays on your computer - nothing is uploaded to external servers.

## Features

✅ Upload multiple CSV and PDF files from different banks  
✅ Automatic PDF table extraction and OCR for scanned documents  
✅ Smart CSV format detection and normalization  
✅ Internal transfer detection (no double-counting)  
✅ AI-powered transaction classification using local Ollama  
✅ Interactive Streamlit UI  
✅ Export unified CSV with all transactions  
✅ Visual analytics and charts  
✅ Configurable category rules  

## Prerequisites

### 1. Python Installation

Make sure you have Python 3.8 or higher installed:

```bash
python --version
```

### 2. Ollama Installation

Install Ollama for local LLM inference:

- **Windows**: Download from [ollama.com/download](https://ollama.com/download)
- **Linux/Mac**: 
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

After installation, pull a model:

```bash
ollama pull qwen3
# or
ollama pull phi4
ollama pull gemma3
```

### 3. Tesseract OCR (Optional, for scanned PDFs)

For OCR functionality, install Tesseract:

- **Windows**: Download from [GitHub Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
- **Linux**: `sudo apt-get install tesseract-ocr tesseract-ocr-deu`
- **Mac**: `brew install tesseract tesseract-lang`

After installation, add Tesseract to your PATH.

## Installation Steps

### Step 1: Install Python Dependencies

Create a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
.\venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

Install required packages:

```bash
pip install streamlit pandas numpy ollama pdfplumber pillow
```

**Optional packages** (for advanced PDF processing):

```bash
# For camelot (more robust PDF table extraction)
pip install camelot-py[cv]

# For OCR support
pip install pytesseract pdf2image
```

**Note:** `camelot-py[cv]` requires additional system dependencies:
- **Windows**: Install [Ghostscript](https://www.ghostscript.com/download/gsdnld.html)
- **Linux**: `sudo apt-get install python3-tk ghostscript`

### Step 2: Verify Installation

Create a test script `test_install.py`:

```python
import streamlit as st
import pandas as pd
import ollama
import pdfplumber

print("✅ All core packages installed successfully!")

# Test Ollama connection
try:
    models = ollama.list()
    print(f"✅ Ollama is running. Available models: {len(models.get('models', []))}")
except Exception as e:
    print(f"⚠️ Ollama connection failed: {e}")
```

Run it:
```bash
python test_install.py
```

## Running the App

### Start the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### First-Time Setup

1. **Configure Your Name** (in sidebar)
   - Enter your name to detect internal transfers (e.g., "Marc Schneider")

2. **Select Ollama Model**
   - Choose from available models (qwen3, phi4, gemma3, etc.)

3. **Customize System Prompt** (optional)
   - Modify classification rules to match your needs

4. **Save Configuration**
   - Click "💾 Save Configuration" to persist settings

## Usage Guide

### 1. Upload Files

- Go to the **"📁 Upload & Process"** tab
- Upload one or more CSV or PDF files
- The app automatically detects file formats

### 2. Map Columns

For each file:
- The app auto-detects standard columns (Date, Amount, Description, etc.)
- Verify or manually adjust column mappings using dropdowns
- Preview the data to ensure correct mapping

### 3. Detect Internal Transfers

- Click **"🔍 Detect Internal Transfers"**
- The app finds matching transactions between accounts
- Internal transfers are highlighted in red

### 4. Classify Transactions

- Click **"🤖 Classify with Ollama"**
- Wait for classification to complete (progress bar shown)
- Each transaction is categorized using AI

### 5. Analyze Results

- Switch to **"📊 Analysis"** tab
- View total income, expenses, and net
- See category breakdowns and charts
- Analyze transaction timeline

### 6. Export Data

- Click **"📥 Download Unified CSV"**
- Get a single CSV file with all transactions
- Includes categories and internal transfer flags

## Creating an Executable with PyInstaller

To create a standalone `.exe` file that doesn't require Python:

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Create Spec File

Create a file `app.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('venv/Lib/site-packages/streamlit', 'streamlit'),
    ],
    hiddenimports=[
        'streamlit',
        'pandas',
        'numpy',
        'ollama',
        'pdfplumber',
        'PIL',
        'pytesseract',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BankTransactionAnalyzer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

### Step 3: Build Executable

```bash
pyinstaller app.spec
```

The executable will be in the `dist/` folder.

### Alternative: Simple Build

For a quick build (larger file size):

```bash
pyinstaller --onefile --add-data "venv/Lib/site-packages/streamlit;streamlit" app.py
```

### Running the Executable

```bash
.\dist\BankTransactionAnalyzer.exe
```

**Important Notes:**
- Ollama must still be installed and running separately
- Tesseract (if using OCR) must be installed separately
- The executable is large (~300-500 MB) due to bundled libraries
- First run may be slow while Streamlit initializes

## Configuration File

The app saves settings in `config.json`:

```json
{
  "user_name": "Your Name",
  "bank_profiles": {},
  "custom_categories": [
    "Freizeit & Lifestyle",
    "Supermarkt",
    "..."
  ],
  "system_prompt": "Your custom prompt..."
}
```

You can edit this file manually or use the UI.

## Troubleshooting

### "Ollama connection failed"

- Ensure Ollama is running: `ollama serve`
- Check if models are installed: `ollama list`
- Pull a model: `ollama pull qwen3`

### PDF Extraction Fails

- Install additional libraries: `pip install camelot-py[cv]`
- For scanned PDFs, install Tesseract OCR
- Try different PDF files to isolate the issue

### Column Detection Issues

- Manually select columns using dropdowns
- Check CSV encoding and delimiter
- Preview data to verify correct parsing

### Classification is Slow

- Use a smaller model (e.g., `qwen3:0.6b`)
- Process fewer transactions at once
- Check Ollama performance: `ollama ps`

### PyInstaller Build Fails

- Ensure all dependencies are installed
- Try simpler build command first
- Check PyInstaller logs for missing modules
- May need to add hidden imports manually

## Tips for Best Results

1. **Consistent File Formats**: Use similar CSV structures when possible
2. **Clear Descriptions**: Better transaction descriptions = better classification
3. **Custom Prompts**: Tailor the system prompt to your spending patterns
4. **Regular Backups**: Export and save your unified CSVs regularly
5. **Test Small First**: Try with a small CSV file before processing large datasets

## Support & Customization

### Adding Custom Categories

Edit the `DEFAULT_CATEGORIES` list in `app.py`:

```python
DEFAULT_CATEGORIES = [
    "Housing",
    "Transportation",
    "Food & Dining",
    "Entertainment",
    # Add your categories here
]
```

### Adjusting Internal Transfer Detection

Modify the `tolerance` parameter in `detect_internal_transfers()`:

```python
tolerance = 0.01  # Allows ±0.01 EUR difference
```

### Using Different Ollama Models

Try different models for better accuracy:
- `qwen3` - Fast, good balance
- `phi4` - High accuracy
- `gemma3` - Good for German text
- `llama3` - General purpose

## File Structure

```
LLM-expenses-analysis/
├── app.py                      # Main application
├── config.json                 # User configuration (auto-generated)
├── main.py                     # Original script (reference)
├── SETUP_INSTRUCTIONS.md       # This file
├── requirements.txt            # Python dependencies
└── your_data_files.csv/pdf     # Your transaction files
```

## Privacy & Security

✅ **100% Local Processing**: No data leaves your computer  
✅ **No Internet Required**: Except for initial setup  
✅ **No Tracking**: No analytics or telemetry  
✅ **Open Source**: Full code transparency  
✅ **Your Data, Your Control**: You own all data and classifications  

## License

This software is provided as-is for personal use. Modify and distribute freely.

---

**Enjoy analyzing your finances locally and privately! 💰📊**
