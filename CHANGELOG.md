# Changelog

## Version 1.0.0 - Initial Release

### Features Implemented

#### 📁 File Upload & Processing
- ✅ Multi-file upload support (CSV and PDF)
- ✅ Automatic encoding detection (UTF-8, ISO-8859-1, cp1252, latin1)
- ✅ Automatic CSV delimiter detection (;, ,, tab, |)
- ✅ Smart column name detection and mapping
- ✅ Manual column mapping override via dropdowns

#### 📄 PDF Support
- ✅ PDF table extraction using PDFPlumber
- ✅ Advanced PDF processing with Camelot (optional)
- ✅ OCR support for scanned PDFs via Pytesseract (optional)
- ✅ Multi-page PDF support
- ✅ Automatic method selection (pdfplumber → camelot → OCR)

#### 🔄 Data Normalization
- ✅ Unified data model: Date, Description, Amount, Account, Currency
- ✅ Date parsing for multiple formats (DD.MM.YYYY, YYYY-MM-DD, etc.)
- ✅ Amount cleaning (handles European/US formats, currency symbols)
- ✅ Source file tracking for each transaction
- ✅ Merge multiple files into single dataset

#### 🔍 Internal Transfer Detection
- ✅ Detect matching opposite amounts between accounts
- ✅ User name-based detection (configurable)
- ✅ Tolerance for rounding differences (default ±0.01)
- ✅ Date proximity checking (within 2 days)
- ✅ Visual highlighting of internal transfers

#### 🤖 AI Classification
- ✅ Local Ollama integration
- ✅ Customizable system prompts
- ✅ Support for multiple models (qwen3, phi4, gemma3, llama3, mistral)
- ✅ Batch processing with progress tracking
- ✅ Category assignment based on description and account
- ✅ Default German categories:
  - Freizeit & Lifestyle
  - Supermarkt
  - Essen unterwegs
  - Mobilität
  - Kleidung & Körperpflege
  - Überschuss
  - Versicherung
  - Wohnen
  - Sonstiges

#### 📊 Analytics & Visualization
- ✅ Total income calculation
- ✅ Total expenses calculation
- ✅ Net balance display
- ✅ Category-wise expense breakdown
- ✅ Bar chart visualization
- ✅ Transaction timeline (daily aggregation)
- ✅ Line chart for trends

#### 💾 Data Export
- ✅ Export unified CSV with all transactions
- ✅ Timestamped filenames
- ✅ Include all metadata (category, internal transfer flag, source)
- ✅ One-click download

#### ⚙️ Configuration Management
- ✅ Persistent configuration via config.json
- ✅ User name storage
- ✅ Custom system prompt storage
- ✅ Category customization
- ✅ Bank profile support (future use)
- ✅ Configuration export

#### 🖥️ User Interface
- ✅ Clean Streamlit-based UI
- ✅ Three-tab layout (Upload, Analysis, Advanced)
- ✅ Sidebar for settings
- ✅ Progress indicators for long operations
- ✅ Color-coded internal transfers
- ✅ Preview tables for all datasets
- ✅ Library status indicators

#### 🔒 Privacy & Security
- ✅ 100% local processing
- ✅ No external API calls (except local Ollama)
- ✅ No data persistence (except user config)
- ✅ No analytics or tracking

#### 🚀 Distribution
- ✅ PyInstaller support for executable creation
- ✅ Windows batch file launcher
- ✅ PowerShell launcher script
- ✅ Installation test script
- ✅ Comprehensive documentation

### Documentation

- ✅ README.md - Project overview
- ✅ SETUP_INSTRUCTIONS.md - Detailed installation guide
- ✅ USAGE_GUIDE.md - Step-by-step usage instructions
- ✅ requirements.txt - Python dependencies
- ✅ app.spec - PyInstaller configuration
- ✅ Inline code comments and docstrings

### Scripts

- ✅ `app.py` - Main application (1000+ lines)
- ✅ `start_app.bat` - Windows launcher
- ✅ `start_app.ps1` - PowerShell launcher
- ✅ `test_install.py` - Dependency verification

### Architecture

- **Modular Design**: Separate functions for each feature
- **Type Hints**: Full typing support for better IDE integration
- **Error Handling**: Comprehensive try-catch blocks
- **Logging**: User-friendly error messages
- **Session State**: Efficient data management in Streamlit

### Supported Formats

#### CSV
- Delimiters: `;`, `,`, `\t`, `|`
- Encodings: UTF-8, ISO-8859-1, cp1252, latin1
- Headers: Auto-detected

#### PDF
- Table-based PDFs (digital)
- Scanned PDFs (with OCR)
- Multi-page documents

#### Export
- CSV (unified format)
- JSON (configuration)

### Known Limitations

1. **PDF Processing**: Complex PDFs may require manual adjustment
2. **Date Formats**: Some exotic date formats may not be detected
3. **OCR Accuracy**: Depends on scan quality and Tesseract configuration
4. **Large Files**: Very large CSVs (>100k rows) may be slow to process
5. **Ollama Dependency**: Requires Ollama to be installed and running

### Future Enhancements (Not Implemented)

- [ ] Excel file support (.xlsx, .xls)
- [ ] Database storage option (SQLite)
- [ ] Multi-user support
- [ ] Recurring transaction detection
- [ ] Budget tracking and alerts
- [ ] Multi-currency conversion
- [ ] Custom export formats (Excel, JSON)
- [ ] Transaction editing in UI
- [ ] Undo/redo functionality
- [ ] Dark mode theme
- [ ] Mobile-responsive design

---

## Development Notes

### Technology Stack

- **Python 3.8+**
- **Streamlit 1.28+** - Web framework
- **Pandas 2.0+** - Data manipulation
- **Ollama** - Local LLM runtime
- **PDFPlumber** - PDF processing
- **Pytesseract** - OCR engine
- **Camelot** - Advanced PDF table extraction

### Code Statistics

- **Lines of Code**: ~1000+
- **Functions**: 25+
- **Classes**: 0 (functional programming style)
- **Documentation**: Extensive comments and docstrings

### Testing

Manual testing performed with:
- ✅ Single CSV file (German format, semicolon delimiter)
- ✅ Multiple CSV files from different banks
- ✅ PDF bank statements
- ✅ Internal transfer detection
- ✅ Classification with multiple Ollama models


---

**Version 1.0.0 Released: October 22, 2025**
