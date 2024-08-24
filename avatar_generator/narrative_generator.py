import csv
import os
import anthropic
import random
import json

# Retrieve the API key from environment variables
my_secret = os.environ['ANTHROPIC_KEY']

# Initialize the Anthropoid client with the API key
client = anthropic.Client(api_key=my_secret)

# Input CSV file path
patient_csv = "patient_data_20240616_220815"
CSV_FILE_PATH = f"patient_data/{patient_csv}.csv"

# Output CSV file path
OUTPUT_CSV_FILE_PATH = f"patient_data/{patient_csv}_with_narratives.csv"


# Function to generate patient narrative using Claude's API
def generate_patient_narrative(patient_data, max_retries=3):
    for attempt in range(max_retries):
        # Generate a random temperature value between 0.1 and 1.0
        temperature = round(random.uniform(0.1, 1.0), 1)

        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=500,
            temperature=temperature,
            system=
            "You are an AI assistant helping with a psychological study that analyzes the moral convictions of medical practitioners confronted with the possibility of administering assisted dying to patients. The study involves presenting participants with patient narratives seeking assisted dying. Your task is to generate a short, realistic narrative for each patient based on their information, which includes their name, age, gender, location, illness, mental state, pain type, and prognosis. The narrative should be written in the first person from the patient's perspective, explaining their situation, the severity of their condition, and their desire to pursue assisted dying. Ensure that the narrative accurately reflects the patient's information and maintains a serious and compassionate tone appropriate for the sensitive topic of assisted dying. Please also determine the patient's gender based on their name. The output content should be in JSON format with separate classes for 'gender', 'narrative', and 'temperature'. Make sure to provide the complete JSON string without truncation. Please do not return any other response other than then content within the JSON",
            messages=[{
                "role": "user",
                "content": [{
                    "type": "text",
                    "text":
                    f"""Please generate a patient narrative for assisted dying based on the following information:\n\n"
                    "First Name: {patient_data['first name']}\n"
                    "Last Name: {patient_data['last name']}\n"
                    "Age: {patient_data['age']}\n"
                    "Location: {patient_data['location']}\n"
                    "Illness: {patient_data['illness']}\n"
                    "Mental State: {patient_data['mental_state']}\n"
                    "Pain Type: {patient_data['pain_type']}\n"
                    "Prognosis: {patient_data['prognosis']}"""
                }]
            }])
        print(message.content)
        response_text = message.content[0].text
        try:
            json_data = json.loads(response_text)
            json_data["temperature"] = temperature
            return json.dumps(json_data)
        except json.JSONDecodeError:
            print(f"Attempt {attempt + 1} failed. Retrying...")
            continue
    raise ValueError("Failed to generate a valid JSON response after multiple attempts.")

# Read patient data from the input CSV file
with open(CSV_FILE_PATH, "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    patient_data_list = list(csv_reader)

# Generate narratives for each patient and store them in a dictionary
narratives = {}
for patient_data in patient_data_list:
    narrative_json = generate_patient_narrative(patient_data)
    narratives[patient_data["first name"]] = narrative_json

# Write the updated patient data with narratives to the output CSV file
with open(OUTPUT_CSV_FILE_PATH, "w", newline="") as csv_file:
    fieldnames = [
        "first name", "last name", "age", "gender", "location", "illness", "mental_state",
        "pain_type", "prognosis", "narrative", "temperature"
    ]
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

    for patient_data in patient_data_list:
        response_json = narratives[patient_data["first name"]]
        response_data = json.loads(response_json)
        patient_data["gender"] = response_data["gender"]
        patient_data["narrative"] = response_data["narrative"]
        patient_data["temperature"] = response_data["temperature"]
        csv_writer.writerow(patient_data)

print(f"Generated narratives for {len(patient_data_list)} patients and saved them to {OUTPUT_CSV_FILE_PATH}")
