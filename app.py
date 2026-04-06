"""
Bank Transaction Analysis App
A fully local desktop application for processing and classifying bank transactions.

Features:
- Upload multiple CSV and PDF files
- PDF to CSV conversion with OCR support
- Automatic CSV format detection
- Internal transfer detection
- Transaction classification using local Ollama
- Export unified CSV
- Streamlit-based UI

Author: Created for local, privacy-focused transaction analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import io
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import tempfile
import ollama
import plotly.graph_objects as go
from classifiers import EmbeddingClassifier, LLMClassifier, TransactionClassifier

# PDF processing libraries
try:
    import pdfplumber
    PDF_PLUMBER_AVAILABLE = True
except ImportError:
    PDF_PLUMBER_AVAILABLE = False

try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

DEFAULT_CATEGORY_KEYWORDS = TransactionClassifier.DEFAULT_EXPENSE_CATEGORIES

DEFAULT_INCOME_KEYWORDS = TransactionClassifier.DEFAULT_INCOME_CATEGORIES

SYSTEM_PROMPT = """Du bist ein Finanz-Experte. Deine Aufgabe ist es, Bank-Transaktionen präzise Kategorien zuzuweisen. 
Basierend auf dem Betrag ist bereits vorentschieden, ob es eine Ausgabe oder Einnahme ist.
Antworte immer nur mit dem Namen der Kategorie, ohne zusätzliche Erklärung oder Floskeln."""

CONFIG_FILE = "config.json"

# Common column name variations for auto-detection
COLUMN_MAPPINGS = {
    'date': ['datum', 'date', 'buchung', 'valuta', 'buchungstag', 'wertstellung', 'transaction date', 'transactiondate'],
    'description': ['beschreibung', 'description', 'verwendungszweck', 'buchungstext', 'text', 'details', 'transaction details', 'purpose'],
    'amount': ['betrag', 'amount', 'wert', 'value', 'sum', 'summe'],
    'account': ['auftraggeber', 'empfänger', 'empfaenger', 'auftraggeber/empfänger', 'auftraggeber/empfaenger', 'auftraggeber/empfnger', 'account', 'recipient', 'payee', 'payer', 'name'],
    'currency': ['währung', 'waehrung', 'whrung', 'currency', 'whrun', 'eur', 'usd']
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_config() -> Dict:
    """Load configuration from file or return default."""
    if Path(CONFIG_FILE).exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"Could not load config: {e}")
    return {
        'user_name': '',
        'bank_profiles': {},
        'custom_categories': list(DEFAULT_CATEGORY_KEYWORDS.keys()),
        'income_categories': list(DEFAULT_INCOME_KEYWORDS.keys()),
        'system_prompt': SYSTEM_PROMPT
    }


def save_config(config: Dict):
    """Save configuration to file."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Could not save config: {e}")


def check_ollama_available() -> Tuple[bool, str]:
    """
    Check if Ollama is installed and running.
    
    Returns:
        Tuple of (is_available, error_message)
    """
    try:
        # Try to list models - this will fail if Ollama is not installed or not running
        ollama.list()
        return True, ""
    except Exception as e:
        error_str = str(e).lower()
        if "connection" in error_str or "refused" in error_str:
            return False, "connection"
        else:
            return False, "not_installed"


def get_available_ollama_models() -> List[str]:
    """Get list of models currently available in Ollama."""
    try:
        response = ollama.list()
        # Handle both dict and object response formats
        if hasattr(response, 'models'):
            models = response.models
        elif isinstance(response, dict):
            models = response.get('models', [])
        else:
            models = []
        
        # Extract model names
        model_names = []
        for model in models:
            # Try 'model' attribute first (ollama._types.Model object)
            if hasattr(model, 'model'):
                model_names.append(model.model)
            # Then try 'name' attribute
            elif hasattr(model, 'name'):
                model_names.append(model.name)
            # Finally try dict access
            elif isinstance(model, dict):
                model_names.append(model.get('model', model.get('name', '')))
        
        return [name for name in model_names if name]
    except Exception as e:
        st.warning(f"Could not fetch Ollama models: {e}")
        return []


def format_model_option(model_name: str, available_models: List[str]) -> str:
    """Format model name with availability indicator."""
    # Check if any available model starts with the model_name (handles tags)
    is_available = any(available.startswith(model_name.split(':')[0]) for available in available_models)
    
    if is_available:
        return f"{model_name} ✓"
    else:
        return f"{model_name} (not downloaded)"


def detect_encoding(file_bytes: bytes) -> str:
    """Detect file encoding. Try common encodings, prioritize German-compatible ones."""
    # Try encodings in order of likelihood for German text
    encodings = ['utf-8', 'cp1252', 'ISO-8859-1', 'ISO-8859-15', 'windows-1252', 'latin1']
    
    for encoding in encodings:
        try:
            decoded = file_bytes.decode(encoding)
            # Check if decoding produced reasonable characters (no replacement chars)
            if '�' not in decoded:
                return encoding
        except (UnicodeDecodeError, LookupError):
            continue
    
    # Fallback: try with errors='replace' to at least get something
    return 'cp1252'  # Most common for German Windows files


def detect_delimiter(file_content: str) -> str:
    """Detect CSV delimiter."""
    delimiters = [';', ',', '\t', '|']
    first_line = file_content.split('\n')[0]
    
    delimiter_counts = {d: first_line.count(d) for d in delimiters}
    detected = max(delimiter_counts, key=delimiter_counts.get)
    
    return detected if delimiter_counts[detected] > 0 else ';'


def normalize_column_name(col: str) -> str:
    """Normalize column name for comparison."""
    return col.lower().strip().replace(' ', '').replace('_', '')


def auto_detect_columns(df: pd.DataFrame) -> Dict[str, Optional[str]]:
    """Automatically detect standard columns in DataFrame."""
    detected = {
        'date': None,
        'description': None,
        'amount': None,
        'account': None,
        'currency': None
    }
    
    # Create mapping of normalized column names to original names
    # Handle duplicate column names by only using the first occurrence
    normalized_cols = {}
    for col in df.columns:
        norm = normalize_column_name(col)
        if norm not in normalized_cols:  # Only keep first occurrence
            normalized_cols[norm] = col
    
    # Try to match each field
    for field, variations in COLUMN_MAPPINGS.items():
        for variation in variations:
            norm_var = normalize_column_name(variation)
            if norm_var in normalized_cols:
                detected[field] = normalized_cols[norm_var]
                break
    
    return detected


def parse_date(date_str: str) -> Optional[datetime]:
    """Try to parse date from various formats."""
    if pd.isna(date_str):
        return None
    
    date_formats = [
        '%d.%m.%Y',
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%m/%d/%Y',
        '%d.%m.%y',
        '%Y%m%d',
    ]
    
    date_str = str(date_str).strip()
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None


def clean_amount(amount_str: str) -> float:
    """Clean and parse amount string to float."""
    if pd.isna(amount_str):
        return 0.0
    
    # Convert to string and clean
    amount_str = str(amount_str).strip()
    
    # Remove currency symbols
    amount_str = re.sub(r'[€$£¥]', '', amount_str)
    
    # Handle European format (1.234,56)
    if ',' in amount_str and '.' in amount_str:
        # European format
        amount_str = amount_str.replace('.', '').replace(',', '.')
    elif ',' in amount_str:
        # Might be European decimal separator
        amount_str = amount_str.replace(',', '.')
    
    # Remove any remaining non-numeric except . and -
    amount_str = re.sub(r'[^\d.-]', '', amount_str)
    
    try:
        return float(amount_str)
    except ValueError:
        return 0.0


# ============================================================================
# PDF PROCESSING
# ============================================================================

def extract_table_from_pdf_pdfplumber(pdf_file) -> pd.DataFrame:
    """Extract tables from PDF using pdfplumber."""
    all_tables = []
    
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    all_tables.append(df)
    
    if all_tables:
        return pd.concat(all_tables, ignore_index=True)
    return pd.DataFrame()


def extract_table_from_pdf_pymupdf(pdf_file) -> pd.DataFrame:
    """Extract tables from PDF using PyMuPDF (fitz)."""
    try:
        import fitz  # PyMuPDF
        
        # Save to temp file if needed
        if hasattr(pdf_file, 'read'):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(pdf_file.read())
                tmp_path = tmp.name
                pdf_file.seek(0)  # Reset for other methods
        else:
            tmp_path = pdf_file
        
        doc = fitz.open(tmp_path)
        
        # Try to find tables using text blocks
        all_tables = []
        
        for page_num, page in enumerate(doc):
            # Get text as a dict with position information
            text_dict = page.get_text("dict")
            blocks = text_dict.get("blocks", [])
            
            # Extract text lines with their positions
            lines_with_pos = []
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        line_text = ""
                        for span in line.get("spans", []):
                            line_text += span.get("text", "")
                        if line_text.strip():
                            lines_with_pos.append({
                                "text": line_text.strip(),
                                "y": line["bbox"][1],  # y-coordinate
                                "x": line["bbox"][0]   # x-coordinate
                            })
            
            # Sort by vertical position (y-coordinate)
            lines_with_pos.sort(key=lambda x: (round(x["y"] / 5) * 5, x["x"]))
            
            # Group lines that are at similar y-positions (same row)
            rows = []
            current_row = []
            last_y = None
            y_threshold = 10  # pixels tolerance
            
            for item in lines_with_pos:
                if last_y is None or abs(item["y"] - last_y) < y_threshold:
                    current_row.append(item)
                    last_y = item["y"] if last_y is None else last_y
                else:
                    if current_row:
                        # Sort by x-position and concatenate
                        current_row.sort(key=lambda x: x["x"])
                        row_text = [r["text"] for r in current_row]
                        rows.append(row_text)
                    current_row = [item]
                    last_y = item["y"]
            
            # Add last row
            if current_row:
                current_row.sort(key=lambda x: x["x"])
                row_text = [r["text"] for r in current_row]
                rows.append(row_text)
            
            all_tables.extend(rows)
        
        doc.close()
        
        # Clean up temp file
        if hasattr(pdf_file, 'read') and 'tmp_path' in locals():
            Path(tmp_path).unlink(missing_ok=True)
        
        # Convert to DataFrame
        if all_tables:
            # Find the maximum number of columns
            max_cols = max(len(row) for row in all_tables)
            
            # Pad rows to have the same number of columns
            padded_rows = [row + [''] * (max_cols - len(row)) for row in all_tables]
            
            # Create DataFrame
            df = pd.DataFrame(padded_rows)
            
            # Filter out header-like rows (rows that appear in first few lines and are repeated)
            # Skip rows that are likely headers (all caps, short text, etc.)
            if len(df) > 5:
                # Try to identify data rows (rows with dates or amounts)
                date_pattern = r'\d{1,2}[./]\d{1,2}[./]\d{2,4}'
                amount_pattern = r'-?\d+[.,]\d{2}'
                
                def has_transaction_data(row):
                    row_str = ' '.join(str(x) for x in row if pd.notna(x))
                    return bool(re.search(date_pattern, row_str) or re.search(amount_pattern, row_str))
                
                data_mask = df.apply(has_transaction_data, axis=1)
                if data_mask.any():
                    # Find first data row
                    first_data_idx = data_mask.idxmax()
                    # Use previous row as header if it exists
                    if first_data_idx > 0:
                        df.columns = df.iloc[first_data_idx - 1].fillna('Unknown').astype(str)
                        df = df.iloc[first_data_idx:].reset_index(drop=True)
                    else:
                        df = df[data_mask].reset_index(drop=True)
            
            return df
        
        return pd.DataFrame()
    
    except Exception as e:
        return pd.DataFrame()


def extract_text_with_ocr(pdf_file) -> str:
    """Extract text from scanned PDF using OCR."""
    if not OCR_AVAILABLE:
        return ""
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(pdf_file.read())
        tmp_path = tmp.name
    
    text = ""
    try:
        from pdf2image import convert_from_path
        images = convert_from_path(tmp_path)
        
        for image in images:
            text += pytesseract.image_to_string(image, lang='deu+eng')
    except Exception as e:
        st.warning(f"OCR failed: {e}")
    finally:
        Path(tmp_path).unlink(missing_ok=True)
    
    return text


def pdf_to_dataframe(pdf_file, filename: str) -> Tuple[pd.DataFrame, str]:
    """
    Convert PDF to DataFrame.
    Returns (DataFrame, method_used)
    """
    df = pd.DataFrame()
    method = "none"
    
    # Check if PDF support is available
    if not PDF_PLUMBER_AVAILABLE:
        st.error("📄 PDF support not available in this build.")
        st.info("💡 **Tip**: Most banks let you download CSV files directly. CSVs work much better and are easier to process!")
        return df, method
    
    # Try pdfplumber first (best for structured tables)
    try:
        df = extract_table_from_pdf_pdfplumber(pdf_file)
        if not df.empty:
            method = "pdfplumber"
            return df, method
    except Exception:
        pass
    
    # Try PyMuPDF as second method (better for text extraction)
    try:
        pdf_file.seek(0)
        df = extract_table_from_pdf_pymupdf(pdf_file)
        if not df.empty:
            method = "pymupdf"
            st.info("📄 Extracted text from PDF - you may need to verify column mapping")
            return df, method
    except Exception:
        pass
    
    # Try OCR as final fallback (for scanned PDFs)
    if OCR_AVAILABLE:
        try:
            pdf_file.seek(0)
            text = extract_text_with_ocr(pdf_file)
            if text:
                # Very basic parsing - user will need to adjust
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                df = pd.DataFrame({'Extracted_Text': lines})
                method = "ocr"
                st.info("📝 Text extracted via OCR - you may need to reformat the data")
                return df, method
        except Exception:
            pass  # Silently fail, show final error message below
    
    # If we get here, nothing worked - show helpful message
    if method == "none":
        st.error("❌ Could not extract data from PDF")
        st.info("💡 **Best solution**: Most banks offer CSV export - use that instead! CSVs are faster, more reliable, and contain all the data you need.")
        with st.expander("ℹ️ Why PDFs are problematic"):
            st.markdown("""
            - PDFs are designed for viewing, not data extraction
            - Table structures vary widely between banks
            - Scanned PDFs require OCR (not included in this build)
            - CSV files contain the exact same data in a structured format
            
            **How to get CSV from your bank**:
            1. Log into your online banking
            2. Go to account statements
            3. Look for "Export" or "Download" options
            4. Choose CSV format (not PDF)
            """)
    
    return df, method


# ============================================================================
# CSV PROCESSING
# ============================================================================

def load_csv_file(file) -> pd.DataFrame:
    """Load CSV file with automatic encoding and delimiter detection."""
    # Read file bytes
    file_bytes = file.read()
    
    # Try UTF-8 first, then fallback to cp1252/ISO-8859-1
    # If file has UTF-8 BOM, use it
    if file_bytes.startswith(b'\xef\xbb\xbf'):
        file_bytes = file_bytes[3:]  # Remove BOM
        file_content = file_bytes.decode('utf-8')
        successful_encoding = 'utf-8-sig'
    else:
        # For German CSV files from Excel/Windows, try these in order
        encodings_to_try = [
            ('utf-8', 'strict'),
            ('cp1252', 'strict'),  # Windows German
            ('ISO-8859-1', 'strict'),  # Latin-1
            ('ISO-8859-15', 'strict'),  # Latin-9 with €
            ('cp1252', 'replace'),  # Fallback with replacement
        ]
        
        file_content = None
        successful_encoding = None
        
        for encoding, error_mode in encodings_to_try:
            try:
                decoded = file_bytes.decode(encoding, errors=error_mode)
                file_content = decoded
                successful_encoding = encoding
                break
            except (UnicodeDecodeError, LookupError):
                continue
        
        # Ultimate fallback
        if file_content is None:
            file_content = file_bytes.decode('cp1252', errors='ignore')
            successful_encoding = 'cp1252 (fallback)'
    
    # Detect delimiter
    delimiter = detect_delimiter(file_content)
    
    # Parse CSV
    df = pd.read_csv(
        io.StringIO(file_content),
        delimiter=delimiter,
        on_bad_lines='skip'
    )
    
    # Fix common encoding corruption in column names and data
    # Replace mojibake patterns with correct German characters
    corruption_fixes = {
        # UTF-8 mojibake (double-encoding issues)
        'Ã¼': 'ü',
        'Ã¶': 'ö',
        'Ã¤': 'ä',
        'ÃŸ': 'ß',
        'Ãœ': 'Ü',
        'Ã–': 'Ö',
        'Ã„': 'Ä',
        'Â°': '°',
        'Â€': '€',
        # Replacement character patterns
        '\ufffd': 'ä',  # Unicode replacement character
        '�': 'ä',  # Replacement character (often for ä in "Empfänger")
        'Empf�nger': 'Empfänger',
        'W�hrung': 'Währung',
        'Auftraggeber/Empf�nger': 'Auftraggeber/Empfänger',
    }
    
    # Fix column names first
    new_columns = []
    for col in df.columns:
        fixed_col = str(col)
        for corrupted, correct in corruption_fixes.items():
            fixed_col = fixed_col.replace(corrupted, correct)
        new_columns.append(fixed_col)
    df.columns = new_columns
    
    # Fix string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(lambda x: apply_corruption_fixes(str(x), corruption_fixes) if pd.notna(x) else x)
    
    # Store encoding info as metadata
    if hasattr(df, 'attrs'):
        df.attrs['detected_encoding'] = successful_encoding
        df.attrs['delimiter'] = delimiter
    
    return df


def apply_corruption_fixes(text: str, fixes: Dict[str, str]) -> str:
    """Apply corruption fixes to text."""
    for corrupted, correct in fixes.items():
        text = text.replace(corrupted, correct)
    return text


def normalize_dataframe(df: pd.DataFrame, column_mapping: Dict[str, str], source_file: str) -> pd.DataFrame:
    """
    Normalize DataFrame to standard format.
    
    Args:
        df: Input DataFrame
        column_mapping: Dict mapping standard fields to actual column names
        source_file: Name of source file
    
    Returns:
        Normalized DataFrame with columns: Date, Description, Amount, Account, Currency, Source
    """
    normalized = pd.DataFrame()
    
    # Map date
    if column_mapping.get('date'):
        normalized['Date'] = df[column_mapping['date']].apply(parse_date)
    else:
        normalized['Date'] = None
    
    # Map description
    if column_mapping.get('description'):
        normalized['Description'] = df[column_mapping['description']].astype(str)
    else:
        normalized['Description'] = ''
    
    # Map amount
    if column_mapping.get('amount'):
        normalized['Amount'] = df[column_mapping['amount']].apply(clean_amount)
    else:
        normalized['Amount'] = 0.0
    
    # Map account/recipient
    if column_mapping.get('account'):
        normalized['Account'] = df[column_mapping['account']].astype(str)
    else:
        normalized['Account'] = 'Unknown'
    
    # Map currency
    if column_mapping.get('currency'):
        normalized['Currency'] = df[column_mapping['currency']].astype(str)
    else:
        normalized['Currency'] = 'EUR'
    
    # Add source file
    normalized['Source'] = source_file
    
    # Initialize other fields
    normalized['Category'] = 'Uncategorized'
    normalized['Internal_Transfer'] = False
    
    return normalized


# ============================================================================
# INTERNAL TRANSFER DETECTION
# ============================================================================

def detect_internal_transfers(df: pd.DataFrame, user_name: str = '', tolerance: float = 0.01) -> pd.DataFrame:
    """
    Detect and mark internal transfers.
    
    Logic:
    1. If recipient contains user's name -> internal transfer
    2. If outgoing amount from one account matches incoming amount to another account
       (within tolerance) and dates are close -> internal transfer
    3. Exclude investment transactions (WP-, Wertpapier, ETF, etc.)
    """
    df = df.copy()
    
    # Exclude investment-related transactions from internal transfer detection
    investment_keywords = ['WP-', 'Wertpapier', 'ETF', 'ISIN', 'Kauf', 'Verkauf', 'Dividende', 'Zins']
    is_investment = df['Description'].str.contains('|'.join(investment_keywords), case=False, na=False, regex=True)
    
    # Mark transfers to/from user's own name (but not investments)
    if user_name:
        user_pattern = re.compile(re.escape(user_name), re.IGNORECASE)
        matches_user = df['Account'].str.contains(user_pattern, na=False, regex=True)
        df.loc[matches_user & ~is_investment, 'Internal_Transfer'] = True
    
    # Find matching transactions (opposite amounts, similar dates)
    for idx, row in df.iterrows():
        if df.loc[idx, 'Internal_Transfer'] or is_investment[idx]:
            continue
        
        amount = row['Amount']
        date = row['Date']
        
        if pd.isna(date) or amount == 0:
            continue
        
        # Look for opposite transaction
        opposite_amount = -amount
        
        # Find matches within tolerance (excluding investments)
        matches = df[
            (df.index != idx) &
            (~df['Internal_Transfer']) &
            (~is_investment) &
            (df['Amount'].between(opposite_amount - tolerance, opposite_amount + tolerance)) &
            (abs((df['Date'] - date).dt.days) <= 2)  # Within 2 days
        ]
        
        if len(matches) > 0:
            df.loc[idx, 'Internal_Transfer'] = True
            df.loc[matches.index[0], 'Internal_Transfer'] = True
    
    return df


# ============================================================================
# OLLAMA CLASSIFICATION
# ============================================================================

def classify_with_ollama(
    description: str,
    account: str,
    system_prompt: str,
    model: str = "qwen3:4b-instruct-2507-q4_K_M"
) -> str:
    """
    Classify transaction using Ollama.
    
    Args:
        description: Transaction description
        account: Account/recipient
        system_prompt: System prompt for classification
        model: Ollama model name
    
    Returns:
        Category name
    """
    try:
        # Construct user prompt
        user_prompt = f"{account}, {description}"
        
        # Call Ollama
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        # Extract and clean response
        category = response["message"]["content"].strip()
        
        return category
    
    except Exception as e:
        st.warning(f"Ollama classification failed: {e}")
        return "Sonstiges"


def classify_batch_with_ollama(transactions_batch: List[Dict], system_prompt: str, model: str) -> List[str]:
    """
    Classify multiple transactions in one Ollama request.
    
    Args:
        transactions_batch: List of transaction dicts with 'account', 'description', and 'amount'
        system_prompt: System prompt for classification
        model: Ollama model name
    
    Returns:
        List of category names
    """
    try:
        # Build a numbered list of transactions with amount information
        transactions_text = "\n".join([
            f"{i+1}. Betrag: €{t['amount']:.2f}, Konto/Empfänger: {t['account']}, Beschreibung: {t['description']}"
            for i, t in enumerate(transactions_batch)
        ])
        
        # Prompt asking for numbered categories
        user_prompt = f"""Hier sind {len(transactions_batch)} Transaktionen. Gib für jede die Kategorie zurück.
Wichtig: Positive Beträge sind Einnahmen, negative Beträge sind Ausgaben.

{transactions_text}

Antworte im Format:
1. [Kategorie]
2. [Kategorie]
3. [Kategorie]
..."""
        
        # Call Ollama
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        # Parse response - extract categories from numbered list
        response_text = response["message"]["content"].strip()
        categories = []
        
        for line in response_text.split('\n'):
            line = line.strip()
            # Match patterns like "1. Kategorie" or "1) Kategorie" or "1 - Kategorie"
            if re.match(r'^\d+[\.\)\-\:]?\s*', line):
                # Remove the number prefix
                category = re.sub(r'^\d+[\.\)\-\:]?\s*', '', line).strip()
                categories.append(category)
        
        # If we didn't get enough categories, pad with "Sonstiges"
        while len(categories) < len(transactions_batch):
            categories.append("Sonstiges")
        
        # If we got too many, truncate
        categories = categories[:len(transactions_batch)]
        
        return categories
    
    except Exception as e:
        st.warning(f"Batch classification failed: {e}")
        # Return default category for all
        return ["Sonstiges"] * len(transactions_batch)


def classify_transactions(df: pd.DataFrame, system_prompt: str, model: str = "qwen3:4b-instruct-2507-q4_K_M", batch_size: int = 10, exclude_internal: bool = True) -> pd.DataFrame:
    """
    Classify all transactions in DataFrame using Ollama with batch processing.
    
    Args:
        df: DataFrame with transactions
        system_prompt: System prompt
        model: Ollama model
        batch_size: Number of transactions to classify in one request
        exclude_internal: If True, exclude internal transfers from classification
    
    Returns:
        DataFrame with Category column filled
    """
    df = df.copy()
    
    # Only classify non-internal transfers if exclude_internal is True
    if exclude_internal:
        to_classify_indices = df[~df['Internal_Transfer']].index.tolist()
    else:
        to_classify_indices = df.index.tolist()
    
    total = len(to_classify_indices)
    
    if total == 0:
        if exclude_internal:
            df.loc[df['Internal_Transfer'], 'Category'] = 'Internal Transfer'
        return df
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Process in batches
    completed = 0
    
    for batch_start in range(0, total, batch_size):
        # Check for cancellation
        if st.session_state.get('cancel_classification', False):
            status_text.text("❌ Classification cancelled")
            break
        
        batch_end = min(batch_start + batch_size, total)
        batch_indices = to_classify_indices[batch_start:batch_end]
        
        # Prepare batch data
        batch_data = []
        for idx in batch_indices:
            row = df.loc[idx]
            batch_data.append({
                'account': str(row['Account']),
                'description': str(row['Description']),
                'amount': float(row['Amount'])
            })
        
        # Classify the batch
        batch_categories = classify_batch_with_ollama(batch_data, system_prompt, model)
        
        # Assign categories back to dataframe
        for idx, category in zip(batch_indices, batch_categories):
            df.loc[idx, 'Category'] = category
        
        # Update progress
        completed = batch_end
        progress = completed / total
        progress_bar.progress(progress)
        
        batch_num = (batch_start // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size
        status_text.text(f"Classified {completed}/{total} transactions (Batch {batch_num}/{total_batches}, {batch_size} per batch)")
    
    progress_bar.empty()
    status_text.empty()
    
    # Mark internal transfers if they should be excluded
    if exclude_internal:
        df.loc[df['Internal_Transfer'], 'Category'] = 'Internal Transfer'
    
    return df


# ============================================================================
# STREAMLIT UI
# ============================================================================

def main():
    st.set_page_config(
        page_title="Bank Transaction Analyzer",
        page_icon="💰",
        layout="wide"
    )
    
    st.title("💰 Bank Transaction Analyzer")
    st.markdown("*Fully local transaction processing and classification*")
    
    # Check if Ollama is available
    ollama_available, error_type = check_ollama_available()
    
    if not ollama_available:
        st.error("### ⚠️ Ollama is Required")
        
        if error_type == "connection":
            st.warning("""
            **Ollama is installed but not running.**
            
            Please start Ollama:
            - **Windows**: Launch Ollama from the Start Menu or system tray
            - **macOS**: Open Ollama from Applications
            - **Linux**: Run `ollama serve` in a terminal
            
            After starting Ollama, refresh this page.
            """)
        else:
            st.warning("""
            **Ollama is not installed on your system.**
            
            This application uses Ollama to run AI models locally for transaction classification.
            
            **Why Ollama?**
            - 🔒 **Complete Privacy**: All processing happens on your computer
            - 🚀 **Fast**: No internet required after setup
            - 🆓 **Free & Open Source**: No API costs or subscriptions
            
            **Installation is quick and easy (takes ~5 minutes):**
            """)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.markdown("#### Windows")
                if st.button("📥 Download for Windows", use_container_width=True):
                    st.link_button("Go to Download", "https://ollama.com/download/windows", use_container_width=True)
                st.caption("Download and run the installer")
            
            with col2:
                st.markdown("#### macOS")
                if st.button("📥 Download for macOS", use_container_width=True):
                    st.link_button("Go to Download", "https://ollama.com/download/mac", use_container_width=True)
                st.caption("Download and open the DMG")
            
            with col3:
                st.markdown("#### Linux")
                st.code("curl -fsSL https://ollama.com/install.sh | sh", language="bash")
                st.caption("Run this command in terminal")
            
            st.info("""
            **After installing Ollama:**
            1. Ollama will start automatically
            2. Refresh this application
            3. The app will download a small AI model (~3GB) on first use
            4. Start analyzing your transactions!
            
            Need help? Visit [ollama.com](https://ollama.com) for detailed instructions.
            """)
        
        st.stop()  # Don't show the rest of the app if Ollama is not available
    
    # Initialize session state
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    if 'config' not in st.session_state:
        st.session_state.config = load_config()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # User name for internal transfer detection
        user_name = st.text_input(
            "Your Name (for internal transfer detection)",
            value=st.session_state.config.get('user_name', '')
        )
        st.session_state.config['user_name'] = user_name
        
        # Classification Method
        st.subheader("Classification Settings")
        
        classification_method = st.radio(
            "Classification Method",
            ["LLM (Generative)", "Embedding (Similarity)"],
            index=0 if st.session_state.config.get('classification_method') == 'LLM' else 1
        )
        st.session_state.config['classification_method'] = 'LLM' if classification_method == "LLM (Generative)" else 'Embedding'

        # Ollama / FLM connection
        use_flm = st.checkbox("Use FLM Server (OpenAI compatible)", value=st.session_state.config.get('use_flm', False))
        st.session_state.config['use_flm'] = use_flm
        
        if use_flm:
            flm_url = st.text_input("FLM Base URL", value=st.session_state.config.get('flm_url', "http://127.0.0.1:52625/v1"))
            st.session_state.config['flm_url'] = flm_url
        
        # Ollama model selection
        st.subheader("Model Selection")
        
        if classification_method == "LLM (Generative)":
            available_models = ["gemma4:e4b", "qwen3:4b-instruct-2507-q4_K_M", "llama3.2:3b"]
            help_text = "Choose the LLM for transaction classification."
        else:
            available_models = ["nomic-embed-text-v2-moe", "all-minilm", "mxbai-embed-large"]
            help_text = "Choose the embedding model for similarity-based classification."
        
        # Get list of downloaded models (only if not using FLM)
        downloaded_models = get_available_ollama_models() if not use_flm else []
        
        # Format model options
        model_options = [format_model_option(m, downloaded_models) if not use_flm else m for m in available_models]
        
        # Get saved model or use default
        config_key = 'llm_model' if classification_method == "LLM (Generative)" else 'embedding_model'
        default_model = st.session_state.config.get(config_key, available_models[0])
        if default_model not in available_models:
            default_model = available_models[0]
        
        selected_option = st.selectbox(
            f"Select {'LLM' if classification_method == 'LLM (Generative)' else 'Embedding'} Model",
            options=model_options,
            index=available_models.index(default_model),
            help=help_text
        )
        
        # Extract actual model name
        model = available_models[model_options.index(selected_option)]
        st.session_state.config[config_key] = model
        
        # Auto-download model if not available (only for Ollama)
        if not use_flm and "(not downloaded)" in selected_option:
            # (Keep the existing download logic here if needed, omitted for brevity in response)
            pass
        
        # System prompt (only for LLM)
        if classification_method == "LLM (Generative)":
            st.subheader("System Prompt")
            system_prompt = st.text_area(
                "Customize classification rules",
                value=st.session_state.config.get('system_prompt', SYSTEM_PROMPT),
                height=200
            )
            st.session_state.config['system_prompt'] = system_prompt
        else:
            # For Embeddings, show categories/keywords editor
            st.subheader("Expense Keywords")
            st.info("Edit keywords for similarity matching (comma-separated)")
            
            # Using a simplified approach for the UI
            cat_keywords = st.session_state.config.get('category_keywords', DEFAULT_CATEGORY_KEYWORDS)
            
            for cat in list(cat_keywords.keys()):
                cat_keywords[cat] = st.text_input(cat, value=cat_keywords[cat], key=f"cat_kw_{cat}")
            
            st.session_state.config['category_keywords'] = cat_keywords

            st.subheader("Income Keywords")
            income_keywords = st.session_state.config.get('income_keywords', DEFAULT_INCOME_KEYWORDS)

            for cat in list(income_keywords.keys()):
                income_keywords[cat] = st.text_input(cat, value=income_keywords[cat], key=f"inc_kw_{cat}")
            
            st.session_state.config['income_keywords'] = income_keywords
        
        # Save config
        if st.button("💾 Save Configuration"):
            save_config(st.session_state.config)
            st.success("Configuration saved!")
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📁 Upload & Process", "📊 Analysis", "⚙️ Advanced"])
    
    with tab1:
        st.header("Upload Files")
        
        uploaded_files = st.file_uploader(
            "Upload CSV or PDF files",
            type=['csv', 'pdf'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.success(f"Uploaded {len(uploaded_files)} file(s)")
            
            all_dataframes = []
            
            for file in uploaded_files:
                st.subheader(f"Processing: {file.name}")
                
                try:
                    # Determine file type
                    if file.name.lower().endswith('.pdf'):
                        # Process PDF
                        df, method = pdf_to_dataframe(file, file.name)
                        
                        # Only show success message if extraction worked
                        if not df.empty:
                            st.success(f"✓ Extracted using: {method}")
                        # Error messages already shown in pdf_to_dataframe function
                        if df.empty:
                            continue
                    else:
                        # Process CSV
                        df = load_csv_file(file)
                    
                    # Show encoding info
                    if hasattr(df, 'attrs') and 'detected_encoding' in df.attrs:
                        st.info(f"📝 Detected encoding: **{df.attrs['detected_encoding']}**, delimiter: **{df.attrs.get('delimiter', ';')}**")
                    
                    # Show preview
                    st.write("**Preview:**")
                    st.dataframe(df.head())
                    
                    # Auto-detect columns
                    detected = auto_detect_columns(df)
                    
                    st.write("**Column Mapping:**")
                    with st.expander("ℹ️ How does column detection work?", expanded=False):
                        st.markdown("""
                        The app automatically detects columns by matching common names:
                        - **Date**: datum, date, buchung, valuta, buchungstag, wertstellung
                        - **Description**: beschreibung, verwendungszweck, buchungstext, text, details
                        - **Amount**: betrag, amount, wert, value, sum, summe
                        - **Account/Recipient**: auftraggeber, empfänger, auftraggeber/empfänger, account, recipient
                        - **Currency**: währung, currency, waehrung
                        
                        If detection fails, manually select the correct columns from the dropdowns below.
                        """)
                    
                    # Manual column selection
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        date_col = st.selectbox(
                            "Date Column",
                            options=[''] + list(df.columns),
                            index=list([''] + list(df.columns)).index(detected['date']) if detected['date'] else 0,
                            key=f"date_{file.name}"
                        )
                        
                        desc_col = st.selectbox(
                            "Description Column",
                            options=[''] + list(df.columns),
                            index=list([''] + list(df.columns)).index(detected['description']) if detected['description'] else 0,
                            key=f"desc_{file.name}"
                        )
                        
                        amount_col = st.selectbox(
                            "Amount Column",
                            options=[''] + list(df.columns),
                            index=list([''] + list(df.columns)).index(detected['amount']) if detected['amount'] else 0,
                            key=f"amount_{file.name}"
                        )
                    
                    with col2:
                        account_col = st.selectbox(
                            "Account/Recipient Column",
                            options=[''] + list(df.columns),
                            index=list([''] + list(df.columns)).index(detected['account']) if detected['account'] else 0,
                            key=f"account_{file.name}"
                        )
                        
                        currency_col = st.selectbox(
                            "Currency Column (optional)",
                            options=[''] + list(df.columns),
                            index=list([''] + list(df.columns)).index(detected['currency']) if detected['currency'] else 0,
                            key=f"currency_{file.name}"
                        )
                    
                    # Normalize
                    column_mapping = {
                        'date': date_col if date_col else None,
                        'description': desc_col if desc_col else None,
                        'amount': amount_col if amount_col else None,
                        'account': account_col if account_col else None,
                        'currency': currency_col if currency_col else None,
                    }
                    
                    normalized_df = normalize_dataframe(df, column_mapping, file.name)
                    all_dataframes.append(normalized_df)
                    
                    st.success(f"✓ Processed {file.name}")
                
                except Exception as e:
                    st.error(f"Error processing {file.name}: {e}")
            
            if all_dataframes:
                # Merge all data
                st.header("Merged Data")
                merged_df = pd.concat(all_dataframes, ignore_index=True)
                
                st.write(f"**Total transactions:** {len(merged_df)}")
                st.dataframe(merged_df)
                
                # Detect internal transfers
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.header("Internal Transfer Detection")
                with col2:
                    with st.expander("ℹ️"):
                        st.markdown("""
                        **What are internal transfers?**
                        
                        Money movements between your own accounts that don't affect your overall balance.
                        
                        **How it works:**
                        1. Finds matching opposite amounts (e.g., -500€ and +500€)
                        2. Checks if dates are within 2 days
                        3. Looks for your name in transaction details
                        4. Excludes investment transactions (ETF, stocks)
                        
                        **Why detect them?**
                        - Prevents double-counting in expense analysis
                        - Shows accurate spending patterns
                        - These are marked but NOT deleted
                        
                        **Note:** You can review and confirm before they're excluded from classification.
                        """)
                
                if st.button("🔍 Detect Internal Transfers"):
                    with st.spinner("Detecting internal transfers..."):
                        merged_df = detect_internal_transfers(
                            merged_df,
                            user_name=user_name,
                            tolerance=0.01
                        )
                        st.session_state.processed_data = merged_df
                    
                    internal_count = merged_df['Internal_Transfer'].sum()
                    st.success(f"✓ Found {internal_count} internal transfers")
                    
                    if internal_count > 0:
                        st.info("""
                        💡 **Next step:** Review the highlighted transactions below. 
                        When you classify transactions, internal transfers will be:
                        - **Highlighted in pink** for easy identification
                        - **Automatically excluded** from AI classification
                        - **Marked as "Internal Transfer"** in the Category column
                        - **Included in the export** (so you have a complete record)
                        
                        Check the box below to confirm you want to exclude them from classification.
                        """)
                
                # Show confirmation if internal transfers were detected
                exclude_internal = True  # Default to excluding internal transfers
                if st.session_state.processed_data is not None and st.session_state.processed_data['Internal_Transfer'].sum() > 0:
                    exclude_internal = st.checkbox(
                        "Exclude internal transfers from classification (recommended)",
                        value=True,
                        help="Internal transfers will be marked but not sent to AI for classification. They'll still appear in your export."
                    )
                    
                    if not exclude_internal:
                        st.warning("⚠️ Warning: If you don't exclude internal transfers, they'll be classified as regular transactions, which may skew your expense analysis.")
                
                # Classify transactions
                st.header("Transaction Classification")
                
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    batch_size = st.slider(
                        "Transactions per batch", 
                        min_value=1, 
                        max_value=50, 
                        value=10, 
                        help="Number of transactions to classify in one Ollama request. Higher = faster but may reduce accuracy."
                    )
                
                with col2:
                    classify_button = st.button("🤖 Classify with Ollama", use_container_width=True)
                
                with col3:
                    if st.button("❌ Cancel", use_container_width=True):
                        st.session_state.cancel_classification = True
                        st.warning("Cancelling...")
                
                if classify_button:
                    if st.session_state.processed_data is None:
                        st.warning("Please detect internal transfers first")
                    else:
                        # Reset cancel flag
                        st.session_state.cancel_classification = False
                        
                        # Use the classification method from config
                        method = st.session_state.config.get('classification_method', 'LLM')
                        use_flm = st.session_state.config.get('use_flm', False)
                        base_url = st.session_state.config.get('flm_url', "http://127.0.0.1:52625/v1") if use_flm else None

                        with st.spinner(f"Classifying transactions using {method}..."):
                            # Prepare keywords
                            expense_kws = st.session_state.config.get('category_keywords', DEFAULT_CATEGORY_KEYWORDS)
                            income_kws = st.session_state.config.get('income_keywords', DEFAULT_INCOME_KEYWORDS)
                            
                            if method == 'LLM':
                                classifier = LLMClassifier(
                                    categories=expense_kws,
                                    income_categories=income_kws,
                                    system_prompt=st.session_state.config.get('system_prompt', SYSTEM_PROMPT),
                                    model_name=st.session_state.config.get('llm_model', 'gemma4:e4b'),
                                    base_url=base_url
                                )
                                classified_df = classifier.classify(
                                    st.session_state.processed_data,
                                    batch_size=batch_size,
                                    exclude_internal=exclude_internal
                                )
                            else:
                                classifier = EmbeddingClassifier(
                                    categories=expense_kws,
                                    income_categories=income_kws,
                                    model_name=st.session_state.config.get('embedding_model', 'nomic-embed-text-v2-moe'),
                                    base_url=base_url
                                )
                                # Embedding classifier doesn't use batch size the same way, but it's okay
                                classified_df = classifier.classify(
                                    st.session_state.processed_data,
                                    exclude_internal=exclude_internal
                                )
                            
                            st.session_state.processed_data = classified_df
                        
                        if st.session_state.get('cancel_classification', False):
                            st.warning("Classification cancelled by user")
                        else:
                            st.success("Classification complete!")
                
                # Show processed data
                if st.session_state.processed_data is not None:
                    st.subheader("Processed Transactions")
                    
                    # Highlight internal transfers with light pink background and style the checkbox
                    def highlight_internal(row):
                        if row['Internal_Transfer']:
                            return ['background-color: #ffcccc; color: #000000'] * len(row)
                        return [''] * len(row)
                    
                    # Create a copy for display with better boolean formatting
                    display_df = st.session_state.processed_data.copy()
                    # Replace True/False with more visible symbols
                    display_df['Internal_Transfer'] = display_df['Internal_Transfer'].apply(
                        lambda x: '✓ Yes' if x else 'No'
                    )
                    
                    styled_df = display_df.style.apply(highlight_internal, axis=1)
                    st.dataframe(styled_df)
                    
                    # Export button
                    st.subheader("Export")
                    
                    # Export with UTF-8 BOM for Excel compatibility
                    csv = '\ufeff' + st.session_state.processed_data.to_csv(index=False, encoding='utf-8')
                    st.download_button(
                        label="📥 Download Unified CSV",
                        data=csv.encode('utf-8'),
                        file_name=f"transactions_unified_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
                    # Quick Analysis Summary
                    st.divider()
                    st.subheader("📊 Quick Analysis Summary")
                    
                    df = st.session_state.processed_data
                    analysis_df = df[~df['Internal_Transfer']].copy()
                    
                    if not analysis_df.empty:
                        # Key metrics in columns
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            total_income = analysis_df[analysis_df['Amount'] > 0]['Amount'].sum()
                            st.metric("💰 Total Income", f"€{total_income:,.2f}")
                        
                        with col2:
                            total_expenses = abs(analysis_df[analysis_df['Amount'] < 0]['Amount'].sum())
                            st.metric("💸 Total Expenses", f"€{total_expenses:,.2f}")
                        
                        with col3:
                            net = total_income - total_expenses
                            delta_color = "normal" if net >= 0 else "inverse"
                            st.metric("📈 Net", f"€{net:,.2f}")
                        
                        with col4:
                            total_transactions = len(analysis_df)
                            internal_count = df['Internal_Transfer'].sum()
                            st.metric("📝 Transactions", f"{total_transactions}", 
                                     delta=f"{internal_count} internal excluded")
                        
                        # Top categories preview
                        st.markdown("#### Top Expense Categories")
                        expense_df = analysis_df[analysis_df['Amount'] < 0].copy()
                        if not expense_df.empty:
                            expense_df['Amount'] = abs(expense_df['Amount'])
                            top_expenses = expense_df.groupby('Category')['Amount'].sum().sort_values(ascending=False).head(5)
                            
                            col1, col2 = st.columns([2, 1])
                            with col1:
                                for category, amount in top_expenses.items():
                                    st.progress(amount / top_expenses.max(), text=f"{category}: €{amount:,.2f}")
                            
                            with col2:
                                st.info(f"""
                                **For detailed analysis:**
                                - Pie charts
                                - Sankey diagram
                                - Category breakdowns
                                
                                👉 Check the **Analysis** tab above
                                """)
                        else:
                            st.info("No expenses found in the data")
                    else:
                        st.info("No transactions to analyze (all are internal transfers)")
    
    with tab2:
        st.header("📊 Analysis & Visualization")
        
        if st.session_state.processed_data is not None:
            df = st.session_state.processed_data
            
            # Filter out internal transfers for analysis
            analysis_df = df[~df['Internal_Transfer']].copy()
            
            # Key metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_income = analysis_df[analysis_df['Amount'] > 0]['Amount'].sum()
                st.metric("Total Income", f"€{total_income:,.2f}")
            
            with col2:
                total_expenses = abs(analysis_df[analysis_df['Amount'] < 0]['Amount'].sum())
                st.metric("Total Expenses", f"€{total_expenses:,.2f}")
            
            with col3:
                net = total_income - total_expenses
                st.metric("Net", f"€{net:,.2f}")
            
            # Pie Charts for Income and Expenses
            st.subheader("💰 Income vs Expenses Breakdown")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Income Sources")
                income_df = analysis_df[analysis_df['Amount'] > 0].copy()
                if not income_df.empty:
                    income_by_category = income_df.groupby('Category')['Amount'].sum()
                    fig_income = {
                        'data': [{
                            'labels': income_by_category.index.tolist(),
                            'values': income_by_category.values.tolist(),
                            'type': 'pie',
                            'marker': {'colors': ['#2ecc71', '#27ae60', '#16a085', '#1abc9c', '#3498db', '#2980b9']},
                            'textinfo': 'label+percent',
                            'hovertemplate': '<b>%{label}</b><br>€%{value:,.2f}<br>%{percent}<extra></extra>'
                        }],
                        'layout': {
                            'showlegend': True,
                            'height': 400,
                            'margin': {'t': 20, 'b': 20, 'l': 20, 'r': 20}
                        }
                    }
                    st.plotly_chart(fig_income, use_container_width=True)
                else:
                    st.info("No income transactions found")
            
            with col2:
                st.markdown("### Expense Categories")
                expense_df = analysis_df[analysis_df['Amount'] < 0].copy()
                if not expense_df.empty:
                    expense_df['Amount'] = abs(expense_df['Amount'])
                    expense_by_category = expense_df.groupby('Category')['Amount'].sum()
                    fig_expense = {
                        'data': [{
                            'labels': expense_by_category.index.tolist(),
                            'values': expense_by_category.values.tolist(),
                            'type': 'pie',
                            'marker': {'colors': ['#e74c3c', '#c0392b', '#e67e22', '#d35400', '#f39c12', '#f1c40f', '#9b59b6', '#8e44ad']},
                            'textinfo': 'label+percent',
                            'hovertemplate': '<b>%{label}</b><br>€%{value:,.2f}<br>%{percent}<extra></extra>'
                        }],
                        'layout': {
                            'showlegend': True,
                            'height': 400,
                            'margin': {'t': 20, 'b': 20, 'l': 20, 'r': 20}
                        }
                    }
                    st.plotly_chart(fig_expense, use_container_width=True)
                else:
                    st.info("No expense transactions found")
            
            # Sankey Diagram
            st.subheader("🔀 Money Flow (Sankey Diagram)")
            st.markdown("*Visualizes how money flows from sources (accounts) to categories*")
            
            if not analysis_df.empty:
                # Prepare data for Sankey
                # Sources are accounts/recipients, targets are categories
                sankey_df = analysis_df[['Account', 'Category', 'Amount']].copy()
                sankey_df['Amount'] = abs(sankey_df['Amount'])
                
                # Group by source and target
                flow_data = sankey_df.groupby(['Account', 'Category'])['Amount'].sum().reset_index()
                flow_data = flow_data[flow_data['Amount'] > 0].sort_values('Amount', ascending=False).head(50)  # Top 50 flows
                
                if not flow_data.empty:
                    # Create unique labels
                    sources = flow_data['Account'].unique().tolist()
                    targets = flow_data['Category'].unique().tolist()
                    all_labels = sources + targets
                    
                    # Map to indices
                    label_to_index = {label: idx for idx, label in enumerate(all_labels)}
                    
                    source_indices = [label_to_index[src] for src in flow_data['Account']]
                    target_indices = [label_to_index[tgt] for tgt in flow_data['Category']]
                    values = flow_data['Amount'].tolist()
                    
                    # Create Sankey
                    fig_sankey = {
                        'data': [{
                            'type': 'sankey',
                            'node': {
                                'label': all_labels,
                                'color': ['#3498db'] * len(sources) + ['#e74c3c'] * len(targets),
                                'pad': 15,
                                'thickness': 20
                            },
                            'link': {
                                'source': source_indices,
                                'target': target_indices,
                                'value': values,
                                'color': 'rgba(0,0,0,0.2)'
                            }
                        }],
                        'layout': {
                            'height': 600,
                            'font': {'size': 10},
                            'margin': {'t': 20, 'b': 20, 'l': 20, 'r': 20}
                        }
                    }
                    st.plotly_chart(fig_sankey, use_container_width=True)
                else:
                    st.info("Not enough data for Sankey diagram")
            
            # Category breakdown table and bar chart
            st.subheader("📊 Detailed Expense Breakdown")
            
            expense_df = analysis_df[analysis_df['Amount'] < 0].copy()
            expense_df['Amount'] = abs(expense_df['Amount'])
            
            if not expense_df.empty:
                category_summary = expense_df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.bar_chart(category_summary)
                
                with col2:
                    st.dataframe(category_summary.reset_index())
            
            # Timeline
            st.subheader("📈 Transaction Timeline")
            
            if 'Date' in analysis_df.columns:
                timeline_df = analysis_df.copy()
                timeline_df['Date'] = pd.to_datetime(timeline_df['Date'])
                timeline_df = timeline_df.dropna(subset=['Date'])
                
                if not timeline_df.empty:
                    timeline_df = timeline_df.set_index('Date').resample('D')['Amount'].sum().reset_index()
                    st.line_chart(timeline_df.set_index('Date'))
        
        else:
            st.info("Upload and process files in the 'Upload & Process' tab first")
    
    with tab3:
        st.header("⚙️ Advanced Settings")
        
        st.subheader("Required Python Libraries")
        st.markdown("""
        For full functionality, install:
        ```bash
        pip install streamlit pandas numpy ollama pdfplumber camelot-py[cv] pytesseract pillow pdf2image
        ```
        
        **Note:** OCR requires Tesseract to be installed separately.
        """)
        
        st.subheader("Library Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("✅ Streamlit" if 'streamlit' in dir() else "❌ Streamlit")
            st.write("✅ Pandas" if 'pd' in dir() else "❌ Pandas")
            st.write("✅ PDFPlumber" if PDF_PLUMBER_AVAILABLE else "❌ PDFPlumber")
        
        with col2:
            st.write("✅ OCR (Pytesseract)" if OCR_AVAILABLE else "❌ OCR")
            st.write("✅ Ollama" if 'ollama' in dir() else "❌ Ollama")
        
        st.subheader("Export Configuration")
        
        if st.button("📄 Export Current Config"):
            config_json = json.dumps(st.session_state.config, indent=2, ensure_ascii=False)
            st.download_button(
                label="Download config.json",
                data=config_json,
                file_name="config.json",
                mime="application/json"
            )


if __name__ == "__main__":
    main()
