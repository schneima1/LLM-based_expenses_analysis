import pandas as pd
import os
from classifiers import EmbeddingClassifier

CSV_FILE = "umsatzanzeige medium copy.csv"

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Classify transactions using embeddings.")
    parser.add_argument("--file", type=str, default=CSV_FILE, help="Path to the CSV file to use.")
    args = parser.parse_args()

    file_to_use = args.file
    if not os.path.exists(file_to_use):
        print(f"File not found: {file_to_use}")
        return

    print(f"Loading data from {file_to_use}...")
    df = pd.read_csv(file_to_use, sep=';', encoding='utf-8')
    
    # Map raw data to classifier columns
    df['Account'] = df.iloc[:, 2]
    df['Description'] = df.iloc[:, 3].fillna('') + " " + df.iloc[:, 4].fillna('')
    # Assuming amount is in column 7 based on previous knowledge
    df['Amount'] = df.iloc[:, 7].apply(lambda x: float(str(x).replace('.', '').replace(',', '.')) if isinstance(x, str) else x)
    
    # Initialize Embedding Classifier (uses defaults from base class)
    print("Initializing Embedding Classifier (ollama by default)...")
    classifier = EmbeddingClassifier(
        model_name="nomic-embed-text-v2-moe"
    )
    
    print(f"Classifying {len(df)} transactions...")
    df = classifier.classify(df, exclude_internal=False)
    
    output_file = "umsatzanzeige_classified_embeddings.csv"
    df.to_csv(output_file, index=False, sep=';', encoding='utf-8')
    print(f"\nClassification complete. Results saved to {output_file}")

if __name__ == "__main__":
    main()
