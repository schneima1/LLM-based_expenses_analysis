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
✅ **AI-Powered**: Uses local LLM or embedding-based classification for smart categorization  
✅ **Multi-Bank**: Handles CSVs from any bank, automatically detects formats  
✅ **Smart Detection**: Identifies internal transfers between your accounts  
✅ **Free & Open Source**: No subscriptions, no hidden costs  
✅ **Full Control**: Customize categories and rules to match your needs  
✅ **Visual Analytics**: Beautiful charts and graphs to understand your spending  
✅ **Multiple Classification Methods**: Choose between LLM (intelligent) or embeddings (fast & efficient)

**Use Cases:**
- 📊 **Personal Finance**: Track spending, identify savings opportunities
- 💼 **Tax Preparation**: Categorize expenses for tax season
- 🏦 **Multi-Account Management**: Consolidate data from different banks
- 📈 **Budget Analysis**: Understand where your money goes each month
- 🔍 **Financial Audit**: Review all transactions in one unified view
- ⚡ **Fast Classification**: Use embedding-based method for quick processing of large datasets

---

## 📥 For End Users (Recommended - No Technical Knowledge Required)

### Quick Setup (10 minutes total)

#### Step 1: Download and Extract the Application

**Option A: Download Pre-built Executable (if available)**
- Check the [releases page](https://github.com/schneima1/LLM-based_expenses_analysis/releases) for `BankTransactionAnalyzer.exe`
- Download and save it to your desktop or Documents folder
- Double-click to run (no installation needed)

**Option B: Run from Source (Always Available)**
- Download the source code: Click "Code" → "Download ZIP" on GitHub
- Extract the ZIP file to a folder on your computer
- Open the folder and double-click `start_app.bat` (Windows) or `start_app.ps1` (PowerShell)
- The script will check requirements and launch the app

#### Step 2: Install Ollama (One-Time, ~5 minutes)

Ollama is a free program that runs AI models on your computer.

1. **Download Ollama**: Go to [ollama.com/download/windows](https://ollama.com/download/windows)
2. **Install**: Run the installer (simple, like any Windows program)
3. **Get Models**: 
   - Open Command Prompt: Press `Win + R`, type `cmd`, press Enter
   - **For LLM (Smart):** `ollama pull gemma4:e4b` (recommended, ~9.6GB)
   - **For Embeddings (Fast):** `ollama pull nomic-embed-text-v2-moe` (~957 MB)
   - Press Enter and wait a few minutes (depending on your internet speed)
4. **Done!** Ollama runs automatically in the background

#### Step 3: Launch the Application

**If using the executable:**
- Double-click `BankTransactionAnalyzer.exe`
- Your browser opens automatically at `http://localhost:8501`

**If running from source:**
- Start the app in one of the following ways:
   - Double-click `start_app.bat`
   - or right-click `start_app.ps1` → "Run with PowerShell"
   - or type `streamlit run app.py` in the terminal
- The script will check Python and dependencies, then launch the app
- Your browser opens automatically at `http://localhost:8501`

**Note:** The app automatically checks if Ollama is installed. If not, it shows helpful instructions with download links.

---

## 🎯 How to Use (For End Users)

### Every Time You Analyze Transactions:

1. **Launch the app**:
   - If using executable: Double-click `BankTransactionAnalyzer.exe`
   - If running from source: Double-click `start_app.bat` (or run `start_app.ps1`)
2. **Upload files**: Drag & drop your bank CSV files (or click to browse)
3. **Configure** (optional):
   - Enter your name for internal transfer detection
   - Select classification method (LLM or Embeddings)
   - Choose AI model if using LLM (`gemma4:e4b` recommended)
   - Adjust categories if needed
4. **Detect transfers**: Click **"🔍 Detect Internal Transfers"**
   - Finds money moved between your own accounts
   - Prevents double-counting
5. **Classify**: Click **"🤖 Classify Transactions"**
   - AI categorizes all transactions automatically
   - Watch the progress bar
   - Choose LLM (smart) or Embeddings (fast) method
6. **Review results**: 
   - See colored charts and graphs
   - Check the categorized transactions
   - Filter by category, date, or account
7. **Export**: Click **"📥 Download Unified CSV"**
   - Get all your data in one clean file
   - Compatible with Excel

### Supported File Types:

✅ **CSV files** (any bank) - Works perfectly  
✅ **Multiple files at once** - Upload all your accounts  
⚠️ **PDF statements** - Basic support (tables only, not scanned)  

### Classification Methods:

**🤖 LLM Classification (Smart & Accurate)**
- Uses local Ollama models (recommended: `gemma4:e4b`)
- Understands context and nuanced descriptions
- Best for complex or unusual transaction descriptions
- Slower but allows the user to guide the model via prompt engineering

**🔢 Embedding Classification (Fast & Efficient)**
- Uses text embeddings (`nomic-embed-text-v2-moe`) to match transactions to categories
- Much faster (processes hundreds in seconds)
- Great for large datasets or regular monthly processing
- Good accuracy for standard transactions
- Requires the embedding model in Ollama

### Tips:

💡 **Start small**: Test with one month of data first  
💡 **Check mappings**: Verify auto-detected columns are correct  
💡 **Choose method**: Use embeddings for speed, LLM for complex cases  
💡 **Custom rules**: Edit the system prompt for your specific needs  
💡 **Save regularly**: Export your results after each session  

---

## 🌟 Features in Detail

### For All Users:

- **Multi-File Upload**: Process multiple CSV and PDF files simultaneously
- **Smart Format Detection**: Automatically detects date formats, delimiters, and column types
- **Internal Transfer Detection**: Identifies money moved between your own accounts
- **AI Classification**: Uses local Ollama models (gemma4:e4b) for categorization
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
- **Embedding Classification**: Fast vector-based categorization using sentence transformers
- **PDF Extraction**: Multiple methods (PDFPlumber, PyMuPDF, OCR fallback)
- **Plotly Visualizations**: Interactive charts and graphs
- **PyInstaller Support**: Build standalone executables
- **Configuration Persistence**: Save settings between sessions
- **Comparison Tool**: Built-in script to compare LLM vs embedding accuracy
- **Modular Architecture**: Clean separation with abstract classifier base class

---

## 🔒 Privacy & Security

- **100% Local Processing**: No data sent to external servers
- **No Internet Required**: Works completely offline (after initial setup)
- **Open Source**: Full transparency - inspect the code yourself
- **No Tracking**: No analytics, no telemetry, no data collection
- **Your Data, Your Control**: All files stay on your computer

---

## 📈 Recent Updates (April 2026)

The project has seen significant improvements recently:

- **✨ Dual Classification Methods**: Added embedding-based classifier as a fast alternative to LLM
- **🎯 Centralized Categories**: All category definitions now in one base class for consistency
- **📊 Comparison Tool**: New script to benchmark LLM vs embedding accuracy side-by-side
- **🤖 Multi-Model Support**: Support for `gemma4:e4b` (LLM) and `nomic-embed-text-v2-moe` (Embeddings)
- **🔧 Enhanced Transfer Detection**: Improved internal transfer detection with tolerance and date proximity
- **📄 Better PDF Support**: Multiple extraction methods with automatic fallback
- **⚡ Performance Optimizations**: Faster processing and better memory management
- **🐛 Bug Fixes**: Fixed umlaut handling, CSV parsing, and many small issues

See the [CHANGELOG.md](CHANGELOG.md) for the complete list of features and improvements.

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
ollama pull gemma4:e4b # to download the LLM
ollama pull nomic-embed-text-v2-moe # to download the embedding model


# Launch the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Dependencies

Core dependencies (see `requirements.txt` for full list):
- `streamlit` - Web UI framework
- `pandas` - Data processing
- `ollama` - Local LLM integration (uses `gemma4:e4b` and `nomic-embed-text-v2-moe`)
- `pdfplumber` - PDF table extraction
- `PyMuPDF` - Alternative PDF processing
- `sentence-transformers` - Embedding-based classification (optional)
- `scikit-learn` - Cosine similarity for embeddings

### Comparing Classification Methods

The project includes a comparison script (`compare_methods.py`) that lets you evaluate both classification approaches side-by-side:

```bash
python compare_methods.py --file umsatzanzeige.csv --debug
```

This will:
- Classify transactions using both LLM and embedding methods
- Show agreement/disagreement rates
- Output results to `comparison_results.csv`
- Help you decide which method works best for your data

**Recent Improvements** (April 2026):
- Centralized category definitions in `TransactionClassifier` base class
- Added embedding-based classifier for fast processing
- Built-in comparison tool to evaluate accuracy
- Enhanced internal transfer detection with tolerance and date proximity
- Improved PDF processing with multiple fallback methods
- Consolidated configuration management
- Better handling of German umlauts and special characters
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
