import csv
import random
from faker import Faker
from datetime import datetime
import os

# Output CSV file will have a timestamp attached to it
folder_path = "patient_data"
os.makedirs(folder_path, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
CSV_FILE_PATH = os.path.join(folder_path, f"patient_data_{timestamp}.csv")

# /////////////////////////////////////////////////////////////////////////////
# >>>>>>>>>>>>>>>HOW MANY RECORDS WOULD YOU LIKE TO GENERATE?<<<<<<<<<<<<<<<<<<
NUM_RECORDS = 40
# /////////////////////////////////////////////////////////////////////////////

# All possible values for patients
LOCATIONS = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
    "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
    "Washington", "West Virginia", "Wisconsin", "Wyoming"
]
ILLNESSES = [
    "pancreatic cancer", "lung cancer", "brain tumor", "ALS", "Alzheimer's",
    "Parkinson's", "multiple sclerosis", "heart failure", "COPD",
    "end-stage renal disease", "depression"
]
MENTAL_STATES = ["mentally capable", "not mentally capable"]
PAIN_TYPES = [
    "severe physical pain", "severe mental pain",
    "both physical and mental pain"
]
PROGNOSES = [
    "less than 1 month", "1-3 months", "3-6 months", "6-12 months",
    "1-2 years", "2-5 years"
]

# Initialize the Faker library for fake names
fake = Faker()

# Generate random patient data and write it to the CSV file
with open(CSV_FILE_PATH, "w", newline="") as csv_file:
    fieldnames = [
        "first name", "last name", "age", "gender", "location", "illness", "mental_state",
        "pain_type", "prognosis"
    ]
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    
    for _ in range(NUM_RECORDS):
        full_name = fake.name()
        first_name, last_name = full_name.split(" ", 1)
        age = random.randint(49, 90)
        location = random.choice(LOCATIONS)
        illness = random.choice(ILLNESSES)
        mental_state = random.choice(MENTAL_STATES)
        pain_type = random.choice(PAIN_TYPES)
        prognosis = "N/A" if illness == "depression" else random.choice(PROGNOSES)


        patient_data = {
            "first name": first_name,
            "last name": last_name,
            "age": age,
            "location": location,
            "illness": illness,
            "mental_state": mental_state,
            "pain_type": pain_type,
            "prognosis": prognosis,
        }
        csv_writer.writerow(patient_data)

        # Log the generated values to the console
        print(f"Generated patient record:")
        print(f"  First Name: {first_name}")
        print(f"  Last Name: {last_name}")
        print(f"  Age: {age}")
        print(f"  Location: {location}")
        print(f"  Illness: {illness}")
        print(f"  Mental State: {mental_state}")
        print(f"  Pain Type: {pain_type}")
        print(f"  Prognosis: {prognosis}")
        print("------------------------")

print(
    f"Generated {NUM_RECORDS} random patient records and saved them to {CSV_FILE_PATH}"
)
