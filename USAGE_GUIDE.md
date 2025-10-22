# Quick Usage Guide

## Getting Started in 5 Minutes

### Step 1: Start the App

**Windows:**
```bash
# Double-click start_app.bat
# OR run manually:
streamlit run app.py
```

**Linux/Mac:**
```bash
source venv/bin/activate
streamlit run app.py
```

### Step 2: Configure Your Settings

1. Open the **sidebar** (click `>` if collapsed)
2. Enter your name in **"Your Name"** field (e.g., "Marc Schneider")
3. Select an **Ollama model** (start with `qwen3`)
4. Click **💾 Save Configuration**

### Step 3: Upload Your Files

1. Go to **"📁 Upload & Process"** tab
2. Click **"Browse files"**
3. Select one or more CSV or PDF files
4. Wait for files to load

### Step 4: Verify Column Mapping

For each uploaded file:

1. **Check the preview** - Does the data look correct?
2. **Verify column mappings** - Are Date, Amount, Description detected correctly?
3. **Adjust if needed** - Use dropdowns to manually select columns

### Step 5: Detect Internal Transfers

1. Click **🔍 Detect Internal Transfers**
2. Review highlighted transactions (shown in red)
3. These won't be counted as expenses/income

### Step 6: Classify Transactions

1. Click **🤖 Classify with Ollama**
2. Wait for classification (progress bar shown)
3. Each transaction gets a category

### Step 7: Analyze & Export

1. Switch to **📊 Analysis** tab
2. View your spending breakdown
3. See charts and totals
4. Go back to **Upload & Process** tab
5. Click **📥 Download Unified CSV**

## Common Workflows

### Scenario 1: Single Bank Account

```
1. Upload one CSV file
2. Verify columns
3. Classify transactions
4. Export results
```

### Scenario 2: Multiple Accounts

```
1. Upload all CSV files at once
2. Verify columns for each file
3. Detect internal transfers (important!)
4. Classify transactions
5. Export unified CSV with all accounts
```

### Scenario 3: PDF Bank Statements

```
1. Upload PDF file
2. App extracts table automatically
3. Check preview carefully
4. Map columns manually if needed
5. Process as normal
```

## Understanding the Results

### Transaction Table Columns

- **Date**: Transaction date (parsed automatically)
- **Description**: What the transaction was for
- **Amount**: Transaction amount (negative = expense, positive = income)
- **Account**: Who you paid or received from
- **Currency**: EUR, USD, etc.
- **Source**: Which file this came from
- **Category**: AI-assigned category
- **Internal_Transfer**: True if this is a transfer between your accounts

### Categories Explained

- **Freizeit & Lifestyle**: Entertainment, hobbies, subscriptions (Amazon, Netflix)
- **Supermarkt**: Grocery shopping
- **Essen unterwegs**: Restaurants, cafes, takeout
- **Mobilität**: Transportation (gas, trains, taxis, Tesla)
- **Kleidung & Körperpflege**: Clothing, cosmetics, hygiene
- **Überschuss**: Income, salary, returns
- **Versicherung**: Insurance payments
- **Wohnen**: Rent, utilities, internet (Vodafone, Rundfunkbeitrag)
- **Sonstiges**: Everything else

### Internal Transfers

Internal transfers are automatically detected when:
1. You transfer money between your own accounts
2. The recipient name matches your name
3. Outgoing amount from Account A ≈ Incoming amount to Account B

These are marked separately so you don't count them twice!

## Tips & Tricks

### 🎯 Better Classification Accuracy

**Customize the System Prompt** to match your spending:

```
Edit in sidebar:
"Amazon is always Freizeit & Lifestyle"
"DB is Deutsche Bahn = Mobilität"
"Add your own rules..."
```

### 📊 Export for Excel Analysis

1. Download the unified CSV
2. Open in Excel
3. Create pivot tables
4. Make custom charts

### 🔄 Reprocess with Different Models

Want to compare models?

1. Process with `qwen3`
2. Note the results
3. Upload same files again
4. Process with `phi4`
5. Compare accuracy

### 💾 Save Your Settings

Your configuration is saved in `config.json`:
- User name
- Custom system prompt
- Bank profiles

You can:
- Back it up
- Share it (without sensitive data)
- Edit it directly

### 🚀 Speed Up Processing

For faster classification:
1. Use smaller models (`qwen3:0.6b`)
2. Process fewer transactions at once
3. Simplify your system prompt

## Troubleshooting Common Issues

### ❌ "File encoding error"

**Solution:** The app tries multiple encodings, but if it fails:
1. Open CSV in a text editor
2. Save with UTF-8 encoding
3. Try uploading again

### ❌ "Columns not detected"

**Solution:** Manual mapping required:
1. Look at the preview
2. Identify which column is what
3. Select manually from dropdowns

### ❌ "Ollama is not running"

**Solution:**
```bash
# Start Ollama
ollama serve

# In another terminal, verify
ollama list
```

### ❌ "Classification is very slow"

**Solutions:**
1. Use a smaller/faster model
2. Close other apps using GPU
3. Process in smaller batches

### ❌ "PDF extraction failed"

**Solutions:**
1. Try a different PDF library (install camelot)
2. For scanned PDFs, install Tesseract
3. Convert PDF to CSV manually first

### ❌ "Internal transfers not detected"

**Check:**
1. Did you enter your name correctly?
2. Do the amounts match exactly? (Try adjusting tolerance)
3. Are the dates within 2 days of each other?

## Advanced Features

### Custom Categories

Edit `app.py` to add your own categories:

```python
DEFAULT_CATEGORIES = [
    "Your Custom Category 1",
    "Your Custom Category 2",
    # ... existing categories
]
```

### Tolerance for Internal Transfers

Adjust rounding tolerance in `app.py`:

```python
# Default is 0.01
detect_internal_transfers(df, user_name="...", tolerance=0.05)
```

### Multi-Language Support

The app works with German transactions by default. For other languages:

1. Edit the system prompt
2. Use appropriate Ollama model
3. Translate category names

## Keyboard Shortcuts

- **Ctrl + R**: Refresh the app
- **Ctrl + C**: Stop the app (in terminal)
- **F5**: Reload browser page

## Data Privacy Reminder

✅ **Everything stays on your computer**
- No data uploaded to cloud
- No tracking or analytics
- Your files, your control

## Need Help?

1. Check `SETUP_INSTRUCTIONS.md` for installation issues
2. Review error messages carefully
3. Try with a small sample file first
4. Check Ollama is running and models are available

---

**Happy analyzing! 💰📊**
