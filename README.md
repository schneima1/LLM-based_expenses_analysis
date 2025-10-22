# 💰 Bank Transaction Analyzer

**Automatically categorize your bank transactions using AI - 100% local, 100% private**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 The Problem This Solves

**Managing personal finances is tedious.** You have transactions scattered across:
- Multiple bank accounts (checking, savings, credit cards)
- Different banks with different CSV formats
- Months or years of unorganized data
- No easy way to see where your money actually goes

**Manual categorization takes hours.** Sorting hundreds of transactions by hand:
- Going through each "Supermarket", "Restaurant", "Gas station" entry one by one
- Remembering which transactions belong to which category
- Updating spreadsheets manually
- Repeating this every month

**Existing solutions have problems:**
- 💰 **Expensive**: Subscription fees for budgeting apps ($10-15/month)
- 🔓 **Privacy risks**: Your financial data stored on someone else's servers
- 🌐 **Online only**: Need internet, need to trust third parties
- 🔒 **Lock-in**: Data trapped in proprietary formats
- 🤖 **Black box**: No control over how transactions are categorized

---

## ✨ The Solution

**Bank Transaction Analyzer** is a desktop application that:

✅ **Works Offline**: All processing happens on your computer  
✅ **100% Private**: Your financial data never leaves your PC  
✅ **AI-Powered**: Uses local LLM (Large Language Model) for smart categorization  
✅ **Multi-Bank**: Handles CSVs from any bank, automatically detects formats  
✅ **Smart Detection**: Identifies internal transfers between your accounts  
✅ **Free & Open Source**: No subscriptions, no hidden costs  
✅ **Full Control**: Customize categories and rules to match your needs  
✅ **Visual Analytics**: Beautiful charts and graphs to understand your spending  

**Use Cases:**
- 📊 **Personal Finance**: Track spending, identify savings opportunities
- 💼 **Tax Preparation**: Categorize expenses for tax season
- 🏦 **Multi-Account Management**: Consolidate data from different banks
- 📈 **Budget Analysis**: Understand where your money goes each month
- 🔍 **Financial Audit**: Review all transactions in one unified view

---

## 📥 For End Users (Recommended - No Technical Knowledge Required)

### Quick Setup (10 minutes total)

#### Step 1: Download the Application

**[📥 Download BankTransactionAnalyzer.exe](../../releases/latest)** (~150 MB)

Just download and save it to your desktop or Documents folder.

#### Step 2: Install Ollama (One-Time, ~5 minutes)

Ollama is a free program that runs AI models on your computer.

1. **Download Ollama**: Go to [ollama.com/download/windows](https://ollama.com/download/windows)
2. **Install**: Run the installer (simple, like any Windows program)
3. **Get AI Model**: 
   - Open Command Prompt: Press `Win + R`, type `cmd`, press Enter
   - Copy and paste: `ollama pull gemma3:4b`
   - Press Enter and wait (~3GB download, 3-5 minutes)
4. **Done!** Ollama runs automatically in the background

#### Step 3: Run the Application

1. **Double-click** `BankTransactionAnalyzer.exe`
2. Your browser opens automatically with the app running at `http://localhost:8501`
3. **Start analyzing!** Upload your bank statements and let AI do the work

**Note:** The app automatically checks if Ollama is installed. If not, it shows helpful instructions with download links.

---

## 🎯 How to Use (For End Users)

### Every Time You Analyze Transactions:

1. **Launch the app**: Double-click `BankTransactionAnalyzer.exe`
2. **Upload files**: Drag & drop your bank CSV files (or click to browse)
3. **Configure** (optional):
   - Enter your name for internal transfer detection
   - Select AI model (gemma3:4b recommended)
   - Adjust categories if needed
4. **Detect transfers**: Click **"🔍 Detect Internal Transfers"**
   - Finds money moved between your own accounts
   - Prevents double-counting
5. **Classify**: Click **"🤖 Classify with Ollama"**
   - AI categorizes all transactions automatically
   - Watch the progress bar
6. **Review results**: 
   - See colored charts and graphs
   - Check the categorized transactions
7. **Export**: Click **"📥 Download Unified CSV"**
   - Get all your data in one clean file
   - Compatible with Excel

### Supported File Types:

✅ **CSV files** (any bank) - Works perfectly  
✅ **Multiple files at once** - Upload all your accounts  
⚠️ **PDF statements** - Basic support (tables only, not scanned)  

### Tips:

💡 **Start small**: Test with one month of data first  
💡 **Check mappings**: Verify auto-detected columns are correct  
💡 **Custom rules**: Edit the system prompt for your specific needs  
💡 **Save regularly**: Export your results after each session  

---

## 🌟 Features in Detail

### For All Users:

- **Multi-File Upload**: Process multiple CSV and PDF files simultaneously
- **Smart Format Detection**: Automatically detects date formats, delimiters, and column types
- **Internal Transfer Detection**: Identifies money moved between your own accounts
- **AI Classification**: Uses local Ollama models (gemma3, qwen3, llama3.2) for categorization
- **Rich Visualizations**: 
  - 📊 Income vs Expense pie charts
  - 🔀 Sankey diagrams showing money flow
  - 📈 Key metrics at a glance
- **Export Ready**: Generate unified CSV files with all transactions
- **Fully Customizable**: Edit categories and classification rules
- **100% Private**: All processing on your computer, no internet required

### Technical Features (For Developers):

- **Streamlit UI**: Modern, responsive web interface
- **Pandas Processing**: Fast data manipulation and analysis
- **Ollama Integration**: Local LLM for intelligent classification
- **PDF Extraction**: Multiple methods (PDFPlumber, PyMuPDF, OCR fallback)
- **Plotly Visualizations**: Interactive charts and graphs
- **PyInstaller Support**: Build standalone executables
- **Configuration Persistence**: Save settings between sessions

---

## 🔒 Privacy & Security

- **100% Local Processing**: No data sent to external servers
- **No Internet Required**: Works completely offline (after initial setup)
- **Open Source**: Full transparency - inspect the code yourself
- **No Tracking**: No analytics, no telemetry, no data collection
- **Your Data, Your Control**: All files stay on your computer

---

## 💻 For Developers (Run from Source)

Want to modify the code or contribute? Here's how to run from source:

### Prerequisites

- Python 3.8 or higher
- Git (optional, for cloning)

### Installation

```bash
# Clone the repository
git clone https://github.com/schneima1/LLM-based_expenses_analysis.git
cd LLM-based_expenses_analysis

# Install dependencies
pip install -r requirements.txt

# Make sure Ollama is running with a model
ollama pull gemma3:4b

# Launch the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Dependencies

Core dependencies (see `requirements.txt` for full list):
- `streamlit` - Web UI framework
- `pandas` - Data processing
- `ollama` - Local LLM integration
- `pdfplumber` - PDF table extraction
- `PyMuPDF` - Alternative PDF processing
- `plotly` - Interactive visualizations

### Project Structure

```
LLM-expenses-analysis/
├── app.py                  # Main application (1600+ lines, fully commented)
├── requirements.txt        # Python dependencies
├── build_simple.spec       # PyInstaller configuration
├── config.json            # User configuration (auto-generated)
├── dist/                  # Built executables
└── README.md             # This file
```

---

## 🛠️ Configuration for Developers

### Custom Categories

Edit in the sidebar or modify `DEFAULT_CATEGORIES` in `app.py`:

```python
DEFAULT_CATEGORIES = [
    "Freizeit & Lifestyle",
    "Supermarkt",
    "Essen unterwegs",
    "Mobilität",
    "Kleidung & Körperpflege",
    "Überschuss",
    "Erstattung",
    "Versicherung",
    "Wohnen",
    "Sonstiges"
]
```

### Classification Rules

Customize the system prompt to define how transactions are classified:

```python
SYSTEM_PROMPT = """
Your custom classification instructions...
Include income vs expense rules...
Define category criteria...
"""
```

The prompt is also editable in the Advanced tab of the UI.

### Bank Profiles

Column mappings are saved automatically in `config.json` for reuse.

---

## 📦 Building Standalone Executable (For Developers)

Want to share the app with non-technical users? Build a standalone .exe:

### Build Process

```bash
# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller --clean build_simple.spec
```

**Output**: `dist/BankTransactionAnalyzer.exe` (~150 MB)

### Distribution

The executable includes:
- Python runtime
- All dependencies
- Streamlit server
- Your application code

**Users need:**
- ✅ Windows 10/11
- ✅ Ollama installed
- ✅ AI model downloaded
- ❌ No Python required
- ❌ No dependencies to install

### Creating a GitHub Release

1. **Build** the executable (see above)
2. **Go to GitHub**: Navigate to your repository
3. **Create Release**: Click "Releases" → "Create a new release"
4. **Tag version**: e.g., `v1.0.0`
5. **Upload**: Drag `dist/BankTransactionAnalyzer.exe` to the release
6. **Publish**: Click "Publish release"

Users can then download from: `https://github.com/schneima1/LLM-based_expenses_analysis/releases/latest`

---

## 🐛 Troubleshooting

### For End Users:

**"Ollama is not available"**
- Make sure Ollama is installed from [ollama.com/download](https://ollama.com/download)
- Check that it's running (look for Ollama icon in system tray)
- Try restarting Ollama

**"Could not extract data from PDF"**
- PDFs are tricky! Use CSV export from your bank instead (much more reliable)
- Make sure the PDF contains selectable text (not a scanned image)

**"Column detection problems"**
- Manually select columns using the dropdowns
- Check that your CSV uses common delimiters (semicolon, comma)
- Try opening the CSV in Notepad to verify the format

### For Developers:

**Ollama Connection Failed**
```bash
# Ensure Ollama is running
ollama serve

# Pull a model
ollama pull gemma3:4b
```

**PDF Extraction Issues**
- Install additional dependencies: `pip install PyMuPDF`
- For scanned PDFs: Install Tesseract OCR (not included by default)

**Module Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

---

## 🤝 Contributing

Contributions are welcome! Ways to help:
- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repository

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

Built with amazing open-source tools:
- [Streamlit](https://streamlit.io/) - Beautiful UI framework
- [Ollama](https://ollama.com/) - Local LLM runtime
- [PDFPlumber](https://github.com/jsvine/pdfplumber) - PDF processing
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [Plotly](https://plotly.com/) - Interactive visualizations

---

## 📬 Support

For issues, questions, or suggestions:
- 📋 Open an issue on GitHub
- 💬 Check existing issues for solutions
- 📖 Read the troubleshooting section above

---

**Made with ❤️ for privacy-conscious financial management**

*Your data, your computer, your control.*
