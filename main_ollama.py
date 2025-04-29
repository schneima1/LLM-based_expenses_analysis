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

# function to categorize a transaction
def categorize_transaction(model, recipient, booking_text, purpose):
    prompt = f"{recipient}, {booking_text}, {purpose}"
    response = ollama.chat(model=model, messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}])
    # remove "<think>\n\n</think>\n\n" from the response
    response = response["message"]["content"].replace("<think>\n\n</think>\n\n", "").strip()
    return response

# function to process a CSV file
# def process_csv(file_path, model="phi4"):
# def process_csv(file_path, model="qwen3:0.6b"):
def process_csv(file_path, model="qwen3"):
    # categorized_transactions = []

    with open(file_path, mode="r", encoding="ISO-8859-1") as file:
        reader = csv.DictReader(file, delimiter=";")
        # add the column "Kategorie" to the CSV file if it doesn't exist
        fieldnames = reader.fieldnames + ["Kategorie"] if "Kategorie" not in reader.fieldnames else reader.fieldnames
        rows = []

        # count the number of rows in the CSV file
        row_count = sum(1 for _ in reader)
        file.seek(0)  # Reset the file pointer to the beginning of the file

        row_counter = 0
        for row in reader:
            recipient = row["Auftraggeber/Empfänger"]
            booking_text = row["Buchungstext"]
            purpose = row["Verwendungszweck"]

            category = categorize_transaction(model, recipient, booking_text, purpose)
            row["Kategorie"] = category  # Add the category to the row
            rows.append(row)

            # Print the categorized transactions
            # print(f"{recipient} | {booking_text} | {purpose} -> {category} \n")
            print(f"{row_counter}/{row_count} | {recipient} | {booking_text} | {purpose} -> {category} \n")

            row_counter = row_counter + 1

    # Write the updated rows back to the CSV file
    with open(file_path, mode="w", encoding="ISO-8859-1", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    process_csv("umsatzanzeige - Kopie.csv")
