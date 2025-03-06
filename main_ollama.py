import csv
import ollama

# System-Prompt für das Modell
SYSTEM_PROMPT = """In meiner nächsten Nachricht werde ich dir Auftraggeber/Empfänger, Buchungstext, Verwendungszweck eines Kontos geben. 
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

# function to categorize a transaction
def categorize_transaction(model, recipient, booking_text, purpose):
    prompt = f"{recipient}, {booking_text}, {purpose}"
    response = ollama.chat(model=model, messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}])
    return response["message"]["content"].strip()

# function to process a CSV file
def process_csv(file_path, model="phi4"):
    categorized_transactions = []

    with open(file_path, mode="r", encoding="ISO-8859-1") as file:  # Changed encoding to ISO-8859-1
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            recipient = row["Auftraggeber/Empfänger"]
            booking_text = row["Buchungstext"]
            purpose = row["Verwendungszweck"]

            category = categorize_transaction(model, recipient, booking_text, purpose)
            categorized_transactions.append((recipient, booking_text, purpose, category))

    # print the categorized transactions
    for entry in categorized_transactions:
        print(f"{entry[0]} | {entry[1]} | {entry[2]} -> {entry[3]} \n")

if __name__ == "__main__":
    process_csv("umsatzanzeige - Kopie.csv")
