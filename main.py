import csv
import re
from collections import defaultdict
import os
import requests
from transformers import AutoTokenizer, AutoModelForCausalLM

# Function to categorize a transaction and extract logits for probabilities
def categorize_with_probabilities(model, tokenizer, recipient, booking_text, purpose):
    prompt = f"{recipient}, {booking_text}, {purpose}\nKategorie:"
    
    inputs = tokenizer(SYSTEM_PROMPT + "\n" + prompt, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=10, return_dict_in_generate=True, output_scores=True)

    # Extract model response
    response_text = tokenizer.decode(output.sequences[0], skip_special_tokens=True).strip()

    # Find the most likely categories based on logits
    logits = output.scores

    # Probability calculation (Softmax approximation)
    prob_dict = defaultdict(float)
    for logit in logits:
        probs = logit.softmax(dim=-1)
        for token, prob in zip(tokenizer.convert_ids_to_tokens(logit.argmax(dim=-1)), probs):
            token = token.strip()  # Clean token
            if token in CATEGORIES:
                prob_dict[token] += prob.item()

    # Normalize probabilities (sum = 1)
    total_prob = sum(prob_dict.values())
    probabilities = {cat: round(prob / total_prob, 2) for cat, prob in prob_dict.items()}

    return response_text, probabilities

# Read CSV file, categorize and calculate probabilities
def process_csv(file_path):
    categorized_transactions = []

    with open(file_path, mode="r", encoding="latin1") as file:  # Changed encoding to 'latin1'
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            recipient = row["Auftraggeber/Empfänger"]
            booking_text = row["Buchungstext"]
            purpose = row["Verwendungszweck"]

            category, probabilities = categorize_with_probabilities(model, tokenizer, recipient, booking_text, purpose)
            categorized_transactions.append((recipient, booking_text, purpose, category, probabilities))

    # Output results
    for entry in categorized_transactions:
        recipient, booking_text, purpose, category, probabilities = entry
        print(f"{recipient} | {booking_text} | {purpose} -> {category} | Probability: {probabilities}")



if __name__ == "__main__":
    
    # Possible categories (must match exactly with LLM responses!)
    CATEGORIES = [
        "Freizeit & Lifestyle", "Supermarkt", "Essen unterwegs", "Mobilität",
        "Kleidung & Körperpflege", "Überschuss", "Versicherung", "Wohnen", "Sonstiges", "unsicher"
    ]

    # model_name = "microsoft/phi-4"
    # small model
    # model_name = "microsoft/Phi-4-mini-instruct"
    # Qwen2.5-3B-Ins
    # model_name = "Qwen/Qwen2.5-3B-Instruct"
    # model_name = "google-t5/t5-small"
    model_name = "unsloth/phi-4-unsloth-bnb-4bit"




    # Initialize the tokenizer and model
    # tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-4")
    # model = AutoModelForCausalLM.from_pretrained("microsoft/phi-4")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)


    # System prompt for categorization
    SYSTEM_PROMPT = """You receive the sender/recipient, booking text, and purpose of an account. 
    Your task is to assign the output to one of the following categories:
    - Freizeit & Lifestyle
    - Supermarkt
    - Essen unterwegs
    - Mobilität
    - Kleidung & Körperpflege
    - Überschuss
    - Versicherung
    - Wohnen
    - Sonstiges

    Special rules:
    - Mobile phone belongs to Sonstiges.
    - Amazon belongs to Freizeit & Lifestyle.
    - Studierendenwerk belongs to Essen unterwegs.
    - DB (Deutsche Bahn) belongs to Mobilität.
    - Vodafone (WLAN) belongs to Wohnen.
    - Tesla and EnBW belong to Mobilität.
    - Broadcasting fee belongs to Wohnen.
    - Mobile contract belongs to Freizeit & Lifestyle.

    If you are unsure, respond with 'unsicher'.  
    Response format: Only the category without justification!
    """

    process_csv("umsatzanzeige - Kopie.csv")