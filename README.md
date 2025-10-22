# 💰 Bank Transaction Analyzer

A **fully local, privacy-focused desktop application** for automated bank transaction processing and classification using AI.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

- ✅ **Multi-File Upload**: Process multiple CSV and PDF files from different banks simultaneously
- ✅ **PDF Intelligence**: Extract tables from PDFs with OCR support for scanned documents
- ✅ **Smart CSV Detection**: Automatic format detection and column mapping
- ✅ **Internal Transfer Detection**: Automatically identify and exclude internal transfers between your accounts
- ✅ **AI Classification**: Use local Ollama models to categorize transactions (no cloud, 100% private)
- ✅ **Interactive UI**: Beautiful Streamlit interface with charts and analytics
- ✅ **Export Ready**: Generate unified CSV files with all transactions and categories
- ✅ **Fully Customizable**: Edit categories and classification rules to match your needs
- ✅ **100% Local**: All processing happens on your computer - your data never leaves

## 🚀 Quick Start

### Option 1: Easy Start (Windows)

Double-click `start_app.bat` and follow the prompts!

### Option 2: Manual Start

```bash
# Install dependencies
pip install -r requirements.txt

# Make sure Ollama is running
ollama pull qwen3

# Launch the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📋 Requirements

### System Requirements

- **Python 3.8+**
- **Ollama** (for AI classification)
- *Optional*: **Tesseract OCR** (for scanned PDF processing)

### Python Dependencies

See `requirements.txt` for full list. Core dependencies:
- `streamlit` - Web UI framework
- `pandas` - Data processing
- `ollama` - Local LLM integration
- `pdfplumber` - PDF table extraction

## 📖 How It Works

### 1. Upload Files
Upload any number of CSV or PDF files from your bank accounts.

### 2. Automatic Processing
- PDFs are converted to structured data
- CSVs are normalized to a common format
- Columns are auto-detected (Date, Amount, Description, etc.)

### 3. Internal Transfer Detection
The app identifies transfers between your own accounts by:
- Matching opposite amounts on similar dates
- Detecting your name in recipient fields
- Allowing small rounding differences

### 4. AI Classification
Each transaction is classified into categories using local Ollama:
- Housing (rent, utilities)
- Food (groceries, restaurants)
- Transportation
- Entertainment
- And more...

### 5. Analysis & Export
- View categorized transactions
- See spending breakdowns
- Export unified CSV for further analysis

## 🎯 Use Cases

- 📊 **Personal Finance**: Track and categorize all your expenses
- 💼 **Tax Preparation**: Organize transactions by category for tax season
- 🏦 **Multi-Account Management**: Consolidate data from multiple banks
- 📈 **Budget Analysis**: Understand spending patterns over time
- 🔍 **Financial Audit**: Review all transactions in one place

## 🛠️ Configuration

### Custom Categories

Edit categories in the sidebar or modify `DEFAULT_CATEGORIES` in `app.py`:

```python
DEFAULT_CATEGORIES = [
    "Housing",
    "Transportation",
    "Food",
    "Your Custom Category"
]
```

### Classification Rules

Customize the system prompt in the UI or in `app.py` to define how transactions should be classified:

```python
SYSTEM_PROMPT = """
Your custom classification instructions here...
"""
```

### Bank Profiles

Save column mappings for frequently used bank formats in `config.json`.

## 📦 Creating an Executable

To create a standalone `.exe` file:

```bash
pip install pyinstaller
pyinstaller app.spec
```

The executable will be in the `dist/` folder. See `SETUP_INSTRUCTIONS.md` for detailed instructions.

## 🔒 Privacy & Security

- **100% Local Processing**: No data is sent to external servers
- **Open Source**: Full transparency - inspect the code yourself
- **No Tracking**: No analytics, no telemetry
- **Your Data, Your Control**: All files stay on your computer

## 📸 Screenshots

### Upload & Process
![Upload Interface](https://via.placeholder.com/800x400?text=Upload+%26+Process+Tab)

### Analysis Dashboard
![Analysis Dashboard](https://via.placeholder.com/800x400?text=Analysis+Dashboard)

### Category Breakdown
![Category Charts](https://via.placeholder.com/800x400?text=Category+Breakdown)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - UI framework
- [Ollama](https://ollama.com/) - Local LLM runtime
- [PDFPlumber](https://github.com/jsvine/pdfplumber) - PDF processing
- [Pandas](https://pandas.pydata.org/) - Data manipulation

## 📚 Documentation

For detailed setup and usage instructions, see:
- `SETUP_INSTRUCTIONS.md` - Complete installation guide
- `requirements.txt` - Python dependencies
- Comments in `app.py` - Code documentation

## 💡 Tips

1. **Start Small**: Test with a small CSV file first
2. **Verify Mappings**: Always check auto-detected column mappings
3. **Custom Prompts**: Tailor the AI prompt to your specific needs
4. **Regular Exports**: Save your processed data regularly
5. **Model Selection**: Try different Ollama models for best results

## 🐛 Troubleshooting

### Ollama Connection Failed
```bash
# Ensure Ollama is running
ollama serve

# Pull a model
ollama pull qwen3
```

### PDF Extraction Issues
- Install additional dependencies: `pip install camelot-py[cv]`
- For scanned PDFs, install Tesseract OCR

### Column Detection Problems
- Manually select columns using the dropdowns in the UI
- Check CSV encoding and delimiter

See `SETUP_INSTRUCTIONS.md` for more troubleshooting tips.

## 📬 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for privacy-conscious financial management**
