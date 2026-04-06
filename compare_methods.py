import pandas as pd
import os
from classifiers import EmbeddingClassifier, LLMClassifier
import time
import argparse

# Reference CSV for testing
DEFAULT_CSV_FILE = "umsatzanzeige medium.csv"
SYSTEM_PROMPT = """Du bist ein Finanz-Experte. Deine Aufgabe ist es, Bank-Transaktionen präzise Kategorien zuzuweisen. 
Antworte immer nur mit dem Namen der Kategorie, ohne zusätzliche Erklärung."""

def main():
    parser = argparse.ArgumentParser(description="Compare Embedding vs LLM Classification accurately.")
    parser.add_argument("--file", type=str, default=DEFAULT_CSV_FILE, help="Path to the CSV file to use.")
    parser.add_argument("--debug", action="store_true", help="Enable detailed debug logging.")
    args = parser.parse_args()

    file_to_use = args.file
    if not os.path.exists(file_to_use):
        # Fallback to any present csv if the specified one is missing
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and 'classified' not in f]
        if not csv_files:
            print(f"No CSV files found. Checked for {file_to_use} and others.")
            return
        file_to_use = csv_files[0]

    print(f"--- Comparison: Embedding vs LLM ---")
    print(f"Loading data from {file_to_use} (Debug: {args.debug})...")
    
    # Simple loader for testing - use latin-1 or iso-8859-1 for German CSVs often containing umlauts
    try:
        df = pd.read_csv(file_to_use, sep=';', encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_to_use, sep=';', encoding='iso-8859-1')
    
    # Ensure standard mapping
    df['Account'] = df.iloc[:, 2].fillna('Unknown')
    df['Description'] = df.iloc[:, 3].fillna('').astype(str) + " " + df.iloc[:, 4].fillna('').astype(str)
    # Convert betrag to float (German format: 1.234,56)
    def clean_amount(val):
        if isinstance(val, str):
            # Remove thousand separators (.) and replace decimal comma (,) with dot
            val_clean = val.replace('.', '').replace(',', '.')
            try:
                return float(val_clean)
            except ValueError:
                return 0.0
        return float(val)
    
    df['Amount'] = df.iloc[:, 7].apply(clean_amount)
    
    # Ensure Internal_Transfer column exists
    df['Internal_Transfer'] = False
    
    # 1. EMBEDDING CLASSIFICATION
    print(f"\n[Method 1] Embedding Classifier (nomic-embed)...")
    start_time = time.time()
    emb_classifier = EmbeddingClassifier() # Uses defaults
    df_emb = df.copy()
    df_emb = emb_classifier.classify(df_emb, debug=args.debug)
    emb_duration = time.time() - start_time
    print(f"Done in {emb_duration:.2f}s")

    # 2. LLM CLASSIFICATION
    print(f"\n[Method 2] LLM Classifier (gemma4:e4b)...")
    start_time = time.time()
    llm_classifier = LLMClassifier(system_prompt=SYSTEM_PROMPT) # Uses defaults
    df_llm = df.copy()
    df_llm = llm_classifier.classify(df_llm, batch_size=5, debug=args.debug)
    llm_duration = time.time() - start_time
    print(f"Done in {llm_duration:.2f}s")

    # 3. COMPARISON
    print("\n--- Results Analysis ---")
    comparison = pd.DataFrame({
        'Text': df['Description'].str[:50],
        'Amount': df['Amount'],
        'Embedding_Cat': df_emb['Category'],
        'LLM_Cat': df_llm['Category']
    })

    # Find Mismatches
    mismatches = comparison[comparison['Embedding_Cat'] != comparison['LLM_Cat']]
    match_count = len(comparison) - len(mismatches)
    accuracy = (match_count / len(comparison)) * 100

    print(f"Total Transactions: {len(comparison)}")
    print(f"Matches: {match_count} ({accuracy:.1f}%)")
    print(f"Mismatches: {len(mismatches)}")
    print(f"\nTiming Performance:")
    print(f"- Embedding: {emb_duration:.2f}s (avg {(emb_duration/len(comparison)):.3f}s/item)")
    print(f"- LLM:       {llm_duration:.2f}s (avg {(llm_duration/len(comparison)):.3f}s/item)")

    if not mismatches.empty:
        print("\nSignificant Mismatches samples:")
        print(mismatches.head(15).to_string(index=False))

    # Save comparison for review
    output_file = "comparison_results.csv"
    comparison.to_csv(output_file, index=False, sep=';', encoding='utf-8')
    print(f"\nDetailed comparison saved to {output_file}")

if __name__ == "__main__":
    main()
