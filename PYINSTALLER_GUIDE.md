# 🎯 PyInstaller Build Guide - Simple Executable Distribution

## Quick Overview

**Goal**: Create a single `.exe` file that users can run without installing Python or dependencies.

**What Users Need**:
1. ✅ Windows 10/11
2. ✅ Ollama (free download, 5-minute install)
3. ✅ Your `.exe` file

**What Users DON'T Need**:
- ❌ Python installation
- ❌ pip/conda
- ❌ Setting PATH variables
- ❌ Installing dependencies
- ❌ Technical knowledge

---

## 📋 Build Process (For You)

### Step 1: Prepare Environment

```bash
# Activate your conda environment
conda activate llm_expense

# Install PyInstaller
pip install pyinstaller
```

### Step 2: Build the Executable

**Option A: Automated (Recommended)**
```bash
# Double-click this file or run:
build_executable.bat
```

**Option B: Manual**
```bash
# Clean previous builds
pyinstaller --clean build_simple.spec

# Result: dist/BankTransactionAnalyzer.exe
```

### Step 3: Test the Executable

```bash
# Run test script
python test_executable.py

# Manual test
cd release
BankTransactionAnalyzer.exe
```

### Step 4: Package for Distribution

```
Create folder: BankTransactionAnalyzer_v1.0/
├── BankTransactionAnalyzer.exe    # The app
└── README_USER.md                  # Simple user guide
```

Zip it and share!

---

## 📦 What Gets Built

### Executable Details:
- **Name**: `BankTransactionAnalyzer.exe`
- **Size**: ~100-150 MB
- **Type**: Console application (shows Streamlit output)
- **Dependencies**: All bundled inside

### Included:
✅ Python runtime  
✅ Streamlit  
✅ Pandas, NumPy  
✅ Ollama client  
✅ PDFPlumber (basic PDF support)  
✅ All necessary libraries  

### Not Included (Optional):
❌ Tesseract (OCR for scanned PDFs)  
❌ Poppler (PDF image conversion)  
❌ Camelot (advanced PDF tables)  

**Why?** These require external programs and PATH configuration. Most users only need CSV support anyway.

---

## 👥 User Instructions (Give Them This)

### 1️⃣ One-Time Setup (5 minutes)

**Install Ollama:**
1. Go to https://ollama.com/download
2. Download and run installer
3. Open Command Prompt
4. Run: `ollama pull qwen3:4b-instruct-2507-q4_K_M`
5. Wait for download (~2.5 GB)

Done! Ollama runs automatically in the background.

### 2️⃣ Using the App (Every Time)

1. **Double-click** `BankTransactionAnalyzer.exe`
2. Browser opens with the app
3. **Upload** your bank CSV files
4. Click **"Detect Internal Transfers"**
5. Click **"Classify with Ollama"**
6. **Download** the categorized CSV

That's it! No technical knowledge needed.

---

## 🔧 Build Configuration

### `build_simple.spec` Settings:

```python
# Single file executable
onefile=True

# Show console (for Streamlit output)
console=True

# Compress with UPX
upx=True

# Exclude optional dependencies
excludes=[
    'pytesseract',
    'pdf2image', 
    'camelot',
    'matplotlib',
    'scipy'
]
```

**Why these settings?**
- **Single file**: Easy distribution, one .exe
- **Console**: Users see Streamlit status messages
- **UPX compression**: Smaller file size
- **Excludes**: Remove unused heavy libraries

---

## 📊 Size Comparison

### Full Build (with OCR):
- Executable: ~180-200 MB
- Requires: Tesseract, Poppler installation
- Complexity: High

### Simple Build (CSV only):
- Executable: ~100-150 MB
- Requires: Nothing (except Ollama)
- Complexity: Low ✅ **Recommended**

**Recommendation**: Use simple build. If users need PDF support, they can convert PDFs to CSV online.

---

## ✅ Quality Checklist

Before distributing, verify:

- [ ] Executable runs on your machine
- [ ] Streamlit opens in browser
- [ ] Can upload CSV files
- [ ] Classification works with Ollama
- [ ] Can download results
- [ ] Test on clean Windows VM (no Python installed)
- [ ] Antivirus doesn't flag it
- [ ] README_USER.md is clear and complete

---

## 🚀 Distribution Methods

### Method 1: Direct Sharing
```
1. Zip the release folder
2. Email/Drive/Dropbox to users
3. Users extract and run .exe
```

### Method 2: GitHub Release
```
1. Create GitHub release (v1.0)
2. Upload BankTransactionAnalyzer.zip
3. Users download from Releases page
```

### Method 3: Company Network
```
1. Place .exe on shared drive
2. Users run directly from network
3. Easy to update centrally
```

---

## 🆘 Common Build Issues

### Issue: "Module not found" error
**Fix**: Add to `hiddenimports` in build_simple.spec

### Issue: Executable is too large (>200 MB)
**Fix**: Add more libraries to `excludes`

### Issue: Streamlit doesn't start
**Fix**: Ensure `console=True` in spec file

### Issue: "Cannot find Streamlit runtime"
**Fix**: Include Streamlit files in `datas`

### Issue: Antivirus flags executable
**Fix**: 
- Expected with PyInstaller
- Add exception in antivirus
- Or code-sign the .exe (advanced)

---

## 🔄 Update Process

When you update the app:

```bash
# 1. Make changes to app.py
# 2. Rebuild
build_executable.bat

# 3. Test
python test_executable.py

# 4. Version number in README
# 5. Redistribute new .exe
```

Users just replace the old .exe file. Settings persist in `config.json`.

---

## 📁 File Structure After Build

```
project/
├── app.py                          # Source code
├── build_simple.spec               # Build configuration
├── build_executable.bat            # Automated build script
├── test_executable.py              # Test script
├── README_USER.md                  # User guide
├── BUILD_EXECUTABLE.md            # This file
├── build/                          # Temporary build files
│   └── (auto-generated)
├── dist/                           # Build output
│   └── BankTransactionAnalyzer.exe
└── release/                        # Distribution package
    ├── BankTransactionAnalyzer.exe
    └── README_USER.md
```

---

## 💡 Pro Tips

1. **Version Numbering**: Add version to filename (`BankTransactionAnalyzer_v1.0.exe`)
2. **Change Log**: Keep track of changes for users
3. **Icon**: Add custom icon in spec file: `icon='myicon.ico'`
4. **Code Signing**: Sign .exe for better trust (costs money)
5. **Auto-Update**: Consider update checker in future versions

---

## 🎯 Success Criteria

Your build is successful if:

✅ User downloads one .exe file  
✅ User installs Ollama (5 minutes)  
✅ User double-clicks .exe  
✅ App opens in browser  
✅ User uploads CSV and gets results  
✅ No Python knowledge required  
✅ No PATH configuration needed  
✅ Works on fresh Windows machine  

---

## 📞 User Support

### Users Will Ask:

**"Do I need Python?"**
→ No! Everything is bundled in the .exe

**"Why do I need Ollama?"**
→ That's the AI that classifies transactions locally

**"Can I use Excel files?"**
→ Save as CSV first, then upload

**"Is my data safe?"**
→ Yes! Everything runs locally, no internet needed (except Ollama install)

**"The app is slow"**
→ Normal. AI processing takes time. First launch is slower.

---

## 🎉 Summary

### For You (Developer):
1. Run `build_executable.bat`
2. Test with `test_executable.py`
3. Zip the `release` folder
4. Share with users

### For Users:
1. Install Ollama (one-time, 5 min)
2. Double-click .exe
3. Upload CSVs
4. Get categorized transactions

**No complexity. No dependencies. Just works.** ✨

---

**Last Updated**: October 2025  
**Build Tool**: PyInstaller  
**Target**: Windows 10/11 (64-bit)  
**Python Version**: 3.8+
