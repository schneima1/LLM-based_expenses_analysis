# 💰 Bank Transaction Analyzer - User Guide

**Categorize your bank transactions automatically using AI - 100% local & private**

---

## 🚀 Quick Start (First Time Only)

### Step 1: Install Ollama (5 minutes)

Ollama is the AI engine that classifies your transactions locally on your computer.

1. **Download**: Go to https://ollama.com/download
2. **Install**: Run the installer (it's simple, like installing any program)
3. **Download AI Model**: 
   - Open Command Prompt (Windows Key + R, type `cmd`, press Enter)
   - Type: `ollama pull qwen3:4b-instruct-2507-q4_K_M`
   - Press Enter and wait (downloads ~2.5 GB, takes 5-10 minutes)

That's it! Ollama runs in the background automatically.

---

## 🎯 Using the App

### Every Time You Want to Analyze Transactions:

1. **Double-click** `BankTransactionAnalyzer.exe`
2. Your browser opens automatically with the app
3. **Upload** your bank CSV files (drag & drop or click to browse)
4. **Optional**: Enter your name for internal transfer detection
5. Click **"🔍 Detect Internal Transfers"** (finds money moved between your accounts)
6. Click **"🤖 Classify with Ollama"** (AI categorizes everything)
7. View the results and click **"📥 Download Unified CSV"**

**Done!** Your transactions are now categorized.

---

## 📁 Supported File Types

### ✅ Works Great:
- **CSV files** from your bank (most common format)
- **Excel exports** saved as CSV
- Multiple files at once

### ⚠️ Limited Support:
- **PDF bank statements** with tables (basic extraction only)
- **Scanned PDFs** don't work (no OCR included)

**Tip**: Most banks let you download CSV files - use those for best results!

---

## 🎨 Features

- **Auto-detect** your bank's format (columns, encoding, delimiter)
- **Internal transfers** highlighted in pink (money between your accounts)
- **AI categorization** into: 
  - Supermarkt (Groceries)
  - Essen unterwegs (Dining Out)
  - Mobilität (Transportation)
  - Wohnen (Housing)
  - Freizeit & Lifestyle (Entertainment)
  - And more...
- **Customizable** rules in the System Prompt
- **Export** everything to one unified CSV file

---

## 🔒 Privacy & Security

- ✅ **100% Local**: All processing happens on your computer
- ✅ **No Internet**: Your transaction data never leaves your machine
- ✅ **No Cloud**: No uploads to any server
- ✅ **Private**: Only you see your data
- ✅ **Secure**: Ollama AI runs entirely offline

---

## ⚙️ Settings

### Your Name
Enter your name to help detect internal transfers (e.g., "Marc Schneider")

### AI Model
Choose which AI model to use:
- **qwen3:4b** - Fast and accurate (recommended)
- **gemma3:4b** - Alternative model
- **llama3.2:3b** - Another option

Click the "Browse Models" link to see all available models at ollama.com/library

### System Prompt
Customize how transactions are categorized. The default works well for German bank accounts.

---

## 🆘 Troubleshooting

### "Model not found" error
**Solution**: Open Command Prompt and run:
```
ollama pull qwen3:4b-instruct-2507-q4_K_M
```

### "Cannot connect to Ollama"
**Solution**: 
1. Make sure Ollama is installed
2. Check if it's running (should start automatically)
3. Restart your computer if needed

### Windows Firewall Warning
**Solution**: Click "Allow Access" - the app needs local network access for Streamlit

### App is slow to start
**Normal**: First launch takes 10-20 seconds while files are extracted
Subsequent launches are faster

### Classification takes a long time
**Normal**: AI processing takes time, especially for many transactions
- ~10 transactions per batch
- Watch the progress bar
- Click "Cancel" if you need to stop

### PDF extraction fails
**Solution**: 
1. Try downloading CSV from your bank instead
2. Or manually convert PDF to CSV online
3. CSVs work much better than PDFs

---

## 💡 Tips & Tricks

1. **Batch Processing**: Upload all your CSV files at once
2. **Review Categories**: Check the results before exporting
3. **Adjust System Prompt**: Customize categories to your needs
4. **Save Configuration**: Click "💾 Save Configuration" to remember settings
5. **Regular Updates**: Check for new .exe versions periodically

---

## 📊 What Gets Classified

### Included:
- All regular expenses and income
- Transfers to/from other people
- Online payments
- Card transactions

### Excluded (Marked as "Internal Transfer"):
- Transfers between your own accounts
- Matches based on your name
- Investment transactions (ETF, stocks, etc.)

---

## 🎯 Example Workflow

**Scenario**: You have 3 bank accounts and want to see all expenses categorized

1. Export CSV files from each bank
2. Open BankTransactionAnalyzer.exe
3. Upload all 3 CSV files
4. Enter your name: "Your Name"
5. Click "Detect Internal Transfers"
6. Click "Classify with Ollama"
7. Wait ~2-3 minutes for processing
8. Review results (internal transfers are pink)
9. Download unified CSV
10. Open in Excel/Google Sheets for analysis

**Result**: All transactions from all accounts in one file, properly categorized!

---

## 📞 Support

### Common Issues
Check the Troubleshooting section above first.

### Getting Help
1. Read this guide carefully
2. Check if Ollama is properly installed
3. Make sure you downloaded the AI model
4. Try with a smaller test file first

---

## 📋 System Requirements

- **Windows 10 or 11** (64-bit)
- **4 GB RAM** minimum (8 GB recommended)
- **5 GB disk space** (for Ollama + AI model)
- **Internet** (only for initial Ollama download)

---

## 🎉 You're All Set!

That's everything you need to know. The app is designed to be simple:

1. Install Ollama (one time)
2. Download model (one time)  
3. Double-click .exe (every time)
4. Upload CSVs
5. Classify
6. Download results

**Enjoy automatic transaction categorization!** 💰✨

---

**Version**: 1.0  
**Updated**: October 2025  
**License**: Open Source
