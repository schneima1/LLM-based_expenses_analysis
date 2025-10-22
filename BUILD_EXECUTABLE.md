# 🚀 Building Standalone Executable

## Create a Simple, Portable App for End Users

This guide shows you how to build a **single executable file** that users can run without installing Python, dependencies, or configuring paths.

---

## 📋 Prerequisites (One-Time Setup for You as Developer)

### Required on Build Machine:
1. **Python 3.8+** with conda/pip
2. **All dependencies installed** (from requirements.txt)
3. **PyInstaller**: `pip install pyinstaller`
4. **Ollama installed** on the user's machine (see User Instructions below)

---

## 🔨 Build Process (3 Steps)

### Step 1: Install PyInstaller in Your Environment

```bash
conda activate llm_expense
pip install pyinstaller
```

### Step 2: Build the Executable

```bash
cd C:\Users\marcs\Projekte\LLM-expenses-analysis
pyinstaller build_simple.spec
```

This creates:
- `dist/BankTransactionAnalyzer.exe` - The standalone executable (~100-150 MB)

### Step 3: Package for Distribution

Create a release folder with:
```
BankTransactionAnalyzer/
├── BankTransactionAnalyzer.exe    # Main executable
├── README_USER.md                  # Simple user instructions
└── config.json                     # (Optional) Pre-configured settings
```

---

## 📦 What Gets Bundled

The executable includes:
- ✅ Python runtime
- ✅ Streamlit
- ✅ Pandas, NumPy
- ✅ PDFPlumber (basic PDF support)
- ✅ Ollama Python client
- ✅ All other dependencies

**NOT included** (must be installed separately):
- ❌ Poppler (for PDF images) - Optional, most CSVs work without it
- ❌ Tesseract (for OCR) - Optional, for scanned PDFs only
- ❌ Ollama itself - Required, see user instructions

---

## 👥 User Instructions (What to Give End Users)

Create a simple README for your users:

```markdown
# Bank Transaction Analyzer - Quick Start

## One-Time Setup (5 minutes)

### Step 1: Install Ollama
1. Download Ollama: https://ollama.com/download
2. Install it (simple installer, no configuration needed)
3. Open Command Prompt or PowerShell
4. Run: `ollama pull qwen3:4b-instruct-2507-q4_K_M`
   - This downloads the AI model (~2.5 GB, one-time download)
   - Takes 5-10 minutes depending on your internet speed

### Step 2: Run the App
1. Double-click `BankTransactionAnalyzer.exe`
2. Browser opens automatically with the app
3. Upload your bank CSV files
4. Click "Classify with Ollama"
5. Download the categorized results

## That's it! 
- No Python installation needed
- No dependencies to manage
- Just Ollama + the .exe file

## Troubleshooting
- **"Model not found"**: Run `ollama pull qwen3:4b-instruct-2507-q4_K_M`
- **"Cannot connect to Ollama"**: Make sure Ollama is running (starts automatically after install)
- **Firewall warning**: Allow the app through Windows Firewall
```

---

## 🎯 Simplified Build Spec

The `build_simple.spec` file removes optional dependencies:
- No Tesseract (OCR for scanned PDFs)
- No Poppler (PDF image rendering)
- No Camelot (advanced PDF tables)

**Result**: 
- ✅ All CSV processing works perfectly
- ✅ Basic PDF tables work (PDFPlumber only)
- ✅ Much smaller executable
- ✅ No external programs needed except Ollama

---

## 📊 File Sizes

Expected sizes:
- **Executable**: ~100-150 MB
- **Ollama + Model**: ~2.5 GB (installed separately)
- **Total disk space**: ~2.7 GB

---

## 🔄 Update Process

When you update the app:
1. Make changes to `app.py`
2. Run `pyinstaller build_simple.spec`
3. Distribute new `BankTransactionAnalyzer.exe`
4. Users just replace the old .exe file

---

## 🌐 Distribution Options

### Option 1: Direct File Sharing
- Zip the release folder
- Share via email, cloud storage, or USB
- No installation needed (except Ollama)

### Option 2: GitHub Releases
1. Create a release on GitHub
2. Upload `BankTransactionAnalyzer.zip`
3. Users download and extract
4. Run the .exe

### Option 3: Company Network
- Place on shared network drive
- Users run directly from network location
- Single .exe, easy to update centrally

---

## ✅ Quality Checks Before Distribution

Test the executable on a clean machine:

1. **Fresh Windows PC** without Python installed
2. Install Ollama only: https://ollama.com/download
3. Run `ollama pull qwen3:4b-instruct-2507-q4_K_M`
4. Double-click the .exe
5. Upload a test CSV file
6. Verify classification works

---

## 🚨 Known Limitations

### PDFs:
- ✅ **Tables in PDFs work** (PDFPlumber built-in)
- ❌ **Scanned PDFs** require Tesseract (not included)
- **Solution**: Most banks provide CSV exports anyway

### Performance:
- First launch may be slow (10-20 seconds) - unpacking
- Subsequent launches are faster
- Classification speed depends on Ollama model

### Antivirus:
- Some antivirus may flag PyInstaller executables
- Add exception if needed
- Sign the .exe for better trust (optional)

---

## 🎁 Advantages of This Approach

1. **User-Friendly**: Double-click to run, no installation
2. **Portable**: Copy to USB, run anywhere
3. **Privacy**: Everything runs locally (except Ollama)
4. **Simple Updates**: Just replace the .exe file
5. **Professional**: Looks like a real desktop app

---

## 📝 Build Command Reference

```bash
# Full build
pyinstaller build_simple.spec

# Clean build (recommended)
pyinstaller --clean build_simple.spec

# Build with verbose output (for debugging)
pyinstaller --clean --log-level DEBUG build_simple.spec
```

---

## 🎯 Summary

**For You (Developer)**:
1. Run `pyinstaller build_simple.spec`
2. Test the .exe
3. Package with README_USER.md
4. Distribute

**For Users**:
1. Install Ollama (one-time, 5 minutes)
2. Download AI model (one-time, 5 minutes)
3. Double-click .exe
4. Use the app

**No Python, no pip, no conda, no PATH configuration, no hassle!** ✨
