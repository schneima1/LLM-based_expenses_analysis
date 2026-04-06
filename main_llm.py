import pandas as pd
import os
from classifiers import LLMClassifier

# The programmatic separator will handle the logic, so the prompt can be simple
SYSTEM_PROMPT = """Du bist ein Finanz-Experte. Deine Aufgabe ist es, Bank-Transaktionen präzise Kategorien zuzuweisen. 
Antworte immer nur mit dem Namen der Kategorie, ohne zusätzliche Erklärung."""

CSV_FILE = "umsatzanzeige medium copy.csv"

def main():
    if not os.path.exists(CSV_FILE):
        print(f"File not found: {CSV_FILE}")
        return

    print(f"Loading data from {CSV_FILE}...")
    df = pd.read_csv(CSV_FILE, sep=';', encoding='utf-8')
    
    # Map raw data to classifier columns
    df['Account'] = df.iloc[:, 2].fillna('')
    df['Description'] = df.iloc[:, 3].fillna('').astype(str) + " " + df.iloc[:, 4].fillna('').astype(str)
    # Convert betrag to float
    df['Amount'] = df.iloc[:, 7].apply(lambda x: float(str(x).replace('.', '').replace(',', '.')) if isinstance(x, str) else x)
    
    # Initialize LLM Classifier (uses defaults from base class)
    print("Initializing LLM Classifier (gemma4:e4b)...")
    classifier = LLMClassifier(
        system_prompt=SYSTEM_PROMPT,
        model_name="gemma4:e4b"
    )
    
    print(f"Classifying {len(df)} transactions...")
    # The classifier will automatically process Expenses then Incomes
    df = classifier.classify(df, batch_size=5, exclude_internal=False)
    
    output_file = "umsatzanzeige_classified_llm.csv"
    df.to_csv(output_file, index=False, sep=';', encoding='utf-8')
    print(f"\nClassification complete. Results saved to {output_file}")

if __name__ == "__main__":
    main()
