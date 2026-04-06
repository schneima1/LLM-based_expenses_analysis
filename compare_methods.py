import pandas as pd
import os
from classifiers import EmbeddingClassifier, LLMClassifier
import time

# Reference CSV for testing
CSV_FILE = "umsatzanzeige medium.csv"
SYSTEM_PROMPT = """Du bist ein Finanz-Experte. Deine Aufgabe ist es, Bank-Transaktionen präzise Kategorien zuzuweisen. 
Antworte immer nur mit dem Namen der Kategorie, ohne zusätzliche Erklärung."""

def main():
    if not os.path.exists(CSV_FILE):
        # Fallback to any present csv if the medium one is missing
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and 'classified' not in f]
        if not csv_files:
            print("No CSV files found for comparison.")
            return
        file_to_use = csv_files[0]
    else:
        file_to_use = CSV_FILE

    print(f"--- Comparison: Embedding vs LLM ---")
    print(f"Loading data from {file_to_use}...")
    
    # Simple loader for testing
    df = pd.read_csv(file_to_use, sep=';', encoding='utf-8')
    
    # Ensure standard mapping
    df['Account'] = df.iloc[:, 2].fillna('Unknown')
    df['Description'] = df.iloc[:, 3].fillna('').astype(str) + " " + df.iloc[:, 4].fillna('').astype(str)
    # Convert betrag to float (German format: 1.234,56)
    def clean_amount(val):
        if isinstance(val, str):
            return float(val.replace('.', '').replace(',', '.'))
        return float(val)
    
    df['Amount'] = df.iloc[:, 7].apply(clean_amount)
    # Ensure Internal_Transfer column exists
    df['Internal_Transfer'] = False
    
    # 1. EMBEDDING CLASSIFICATION
    print("\n[Method 1] Embedding Classifier (nomic-embed)...")
    start_time = time.time()
    emb_classifier = EmbeddingClassifier() # Uses defaults
    df_emb = df.copy()
    df_emb = emb_classifier.classify(df_emb)
    emb_duration = time.time() - start_time
    print(f"Done in {emb_duration:.2f}s")

    # 2. LLM CLASSIFICATION
    print("\n[Method 2] LLM Classifier (gemma4:e4b)...")
    start_time = time.time()
    llm_classifier = LLMClassifier(system_prompt=SYSTEM_PROMPT) # Uses defaults
    df_llm = df.copy()
    df_llm = llm_classifier.classify(df_llm, batch_size=5)
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
