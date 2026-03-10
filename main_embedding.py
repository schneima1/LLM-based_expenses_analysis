import pandas as pd
import numpy as np
from openai import OpenAI
import os
import sys

# Configuration for FLM OpenAI-compatible API
FLM_BASE_URL = "http://127.0.0.1:52625/v1"
MODEL_NAME = "embed-gemma"

CSV_FILE = "umsatzanzeige medium copy.csv"

# Define the categories with descriptive keywords
CATEGORIES = {
    "Wohnen": "Miete, Strom, Internet, Heizung, Nebenkosten, Vodafone, immergruen",
    "Mobilität": "Bahn, Auto, Tankstelle, Bus, Flug",
    "Essen unterwegs": "Restaurant, Lieferdienst, Fast Food",
    "Essen daheim": "Supermarkt, Lebensmittel, REWE, Aldi, Lidl",
    "Investments": "ETF, Aktie, Trade Republic, Depot, Kryptowährung",
    "Freizeit & Lifestyle": "Kino, Konzert, Reisen, Sport, Amazon, Handy, Mobilfunk, Lebara, sim.de",
    "Urlaub": "Reise, Hotel, Flug, Mietwagen, booking, airbnb",
    "Versicherungen": "Lebensversicherung, Hausratversicherung, Kfz-Versicherung, Allianz, Getsafe, Itzehoer, Tesla, EnBW mobility",
    "Kleidung & Körperpflege": "Friseur, Kosmetik, Mode, Klamotten, Fashion",
    "Miscellaneous": "Sonstiges, diverse, unbekannt, Bargeldauszahlung"
}

# Initialize OpenAI client
client = OpenAI(base_url=FLM_BASE_URL, api_key="flm")

def get_embedding(text):
    """Fetches embedding for a given text using FLM server."""
    try:
        response = client.embeddings.create(
            model=MODEL_NAME,
            input=text
        )
        if response.data:
            return np.array(response.data[0].embedding)
        else:
            print(f"Warning: No embedding returned for '{text[:50]}...'")
            return None
    except Exception as e:
        print(f"Error getting embedding for '{text[:50]}...': {e}")
        return None

def cosine_similarity(a, b):
    """Calculates cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def main():
    if not os.path.exists(CSV_FILE):
        print(f"File not found: {CSV_FILE}")
        return

    print(f"Loading data from {CSV_FILE}...")
    # Read CSV with semicolon delimiter, using UTF-8 encoding
    df = pd.read_csv(CSV_FILE, sep=';', encoding='utf-8')

    # Pre-calculate embeddings for categories (name + descriptive keywords)
    print("Calculating category embeddings...")
    category_embeddings = {}
    for cat_name, cat_desc in CATEGORIES.items():
        # Combine category name with its descriptive keywords
        cat_text = f"{cat_name}: {cat_desc}"
        emb = get_embedding(cat_text)
        if emb is not None:
            category_embeddings[cat_name] = emb
    
    if not category_embeddings:
        print("Failed to get embeddings for categories. Is the FLM server running?")
        return

    results = []

    print(f"Classifying {len(df)} expenses...")
    for index, row in df.iterrows():
        # Use column indices to avoid encoding issues with column names
        # Columns: 0=Buchung, 1=Valuta, 2=Auftraggeber/Empfänger, 3=Buchungstext, 4=Verwendungszweck, ...
        empfaenger = row.iloc[2] if len(row) > 2 else ''
        buchungstext = row.iloc[3] if len(row) > 3 else ''
        verwendungszweck = row.iloc[4] if len(row) > 4 else ''
        
        # Convert to string, handling NaN/None
        empfaenger = '' if pd.isna(empfaenger) else str(empfaenger)
        buchungstext = '' if pd.isna(buchungstext) else str(buchungstext)
        verwendungszweck = '' if pd.isna(verwendungszweck) else str(verwendungszweck)
        
        description = f"{empfaenger} {buchungstext} {verwendungszweck}".strip()

        print(f"Processing row {index+1}: {description[:50]}...")
        
        if not description:
            results.append("Miscellaneous")
            continue

        expense_emb = get_embedding(description)
        
        if expense_emb is None:
            results.append("Error")
            continue

        # Find category with highest similarity
        best_cat = "Miscellaneous"
        max_sim = -1.0
        
        for cat, cat_emb in category_embeddings.items():
            sim = cosine_similarity(expense_emb, cat_emb)
            if sim > max_sim:
                max_sim = sim
                best_cat = cat
        
        results.append(best_cat)
        print(f"Row {index+1}: {description[:50]}... -> {best_cat} (sim: {max_sim:.4f})")

    df['Category'] = results
    
    output_file = "umsatzanzeige_classified_embeddings.csv"
    df.to_csv(output_file, index=False, sep=';', encoding='utf-8')
    print(f"\nClassification complete. Results saved to {output_file}")

if __name__ == "__main__":
    main()
