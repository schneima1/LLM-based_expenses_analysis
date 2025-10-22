import csv
import ollama

# System-Prompt für das Modell
SYSTEM_PROMPT = """/no_think In meiner nächsten Nachricht werde ich dir Auftraggeber/Empfänger, Buchungstext, Verwendungszweck eines Kontos geben. 
Deine Aufgabe ist es, die Ausgabe einer der folgenden Kategorien zuzuordnen:
- Freizeit & Lifestyle
- Supermarkt
- Essen unterwegs
- Mobilität
- Kleidung & Körperpflege
- Überschuss
- Versicherung
- Wohnen
- Sonstiges

Mobilfunk gehört zu Sonstiges. 
Amazon gehört zu Freizeit & Lifestyle. 
Studierendenwerk gehört zu Essen unterwegs. 
DB ist Deutsche Bahn und damit Mobilität. 
Vodafone ist WLAN und damit Wohnen. 
Alles mit Tesla oder EnBW ist Mobilität. 
Rundfunkbeitrag ist bei Wohnen dabei. 
Handyvertrag gehört zu Freizeit & Lifestyle.

Wenn du dir nicht sicher bist, antworte mit 'unsicher'. Antworte nur mit der Kategorie, keine Begründung!"""


def categorize_transaction(model_name, recipient, booking_text, purpose):
    """Categorize a transaction using the specified model."""
    prompt = f"{recipient}, {booking_text}, {purpose}"
    # response = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])
    response = ollama.chat(model=model, messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}])
    # remove "<think>\n\n</think>\n\n" from the response
    response = response["message"]["content"].replace("<think>\n\n</think>\n\n", "").strip()
    return response

def process_csv(file_path, model_name):
    """Process the CSV file with a specific model."""

    with open(file_path, mode="r", encoding="ISO-8859-1") as file:
        reader = csv.DictReader(file, delimiter=";")
        category_name = "Kategorie " + model_name
        # fieldnames = reader.fieldnames + ["Kategorie"] if "Kategorie" not in reader.fieldnames else reader.fieldnames
        fieldnames = reader.fieldnames + [category_name] if category_name not in reader.fieldnames else reader.fieldnames
        rows = []
        row_count = sum(1 for _ in reader)  # Count the number of rows
        file.seek(0)
        row_counter = 1  # Start from 1 for user-friendly output


        # read the CSV file again to process it
        for row in reader:
            # Skip the header row
            if row["Auftraggeber/Empfänger"] == "Auftraggeber/Empfänger":
                continue

            recipient = row["Auftraggeber/Empfänger"]
            booking_text = row["Buchungstext"]
            purpose = row["Verwendungszweck"]

            category = categorize_transaction(model_name, recipient, booking_text, purpose)
            # row["Kategorie"] = category
            row[category_name] = category

            print(f"{row_counter}/{row_count} | {recipient} | {booking_text} | {purpose} -> {category} \n")        
            row_counter = row_counter + 1
            rows.append(row)

    with open(file_path, mode="w", encoding="ISO-8859-1", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    # models = ["qwen3:0.6b","phi4", "qwen3"]
    # models = ["qwen3"]
    # models = ["gemma3", "phi4", "qwen3"]
    models = ["gemma3", "qwen3", "phi4"]
    for model in models:
        print(f"Processing with model: {model}")
        # process_csv("umsatzanzeige - Kopie.csv", model)
        process_csv("umsatzanzeige - Kopie.csv", model)