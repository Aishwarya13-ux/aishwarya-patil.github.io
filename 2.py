import json
import datetime
import os

DATA_FILE = "patient_data.json"

# --- Data Storage ---
patient_data = {
    "profile": {},
    "prescriptions": [], # list of dicts: {"name": "", "dosage": "", "frequency": "", "instructions": "", "last_taken": None}
    "condition_log": [], # list of dicts: {"timestamp": "", "entry": ""}
    "doctor_advice": {}, # dict: {"topic/condition": "advice string"}
    "emergency_info": {
        "doctor_name": "",
        "doctor_contact": "",
        "emergency_contact_name": "",
        "emergency_contact_phone": ""
    }
}

# --- Pre-defined Home Remedies (can be expanded) ---
HOME_REMEDIES_DB = {
    "mild headache": [
        "Drink plenty of water.",
        "Rest in a quiet, dark room.",
        "Apply a cool compress to your forehead."
    ],
    "mild cough": [
        "Drink warm water with honey and lemon (not for infants under 1).",
        "Use a humidifier or take a steamy shower.",
        "Sip on herbal tea like ginger or thyme tea."
    ],
    "mild nausea": [
        "Sip clear fluids like water or ginger ale.",
        "Eat bland foods like crackers or toast.",
        "Avoid strong smells."
    ]
}

# --- Helper Functions ---
def save_data():
    """Saves the current patient_data to a JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(patient_data, f, indent=4)
        print("Data saved.")
    except IOError:
        print(f"Error: Could not save data to {DATA_FILE}")

def load_data():
    """Loads patient_data from a JSON file if it exists."""
    global patient_data
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                patient_data = json.load(f)
            print("Data loaded.")
        except (IOError, json.JSONDecodeError):
            print(f"Error: Could not load data from {DATA_FILE}. Using default empty data.")
            # Initialize with default structure if file is corrupt
            patient_data = {
                "profile": {}, "prescriptions": [], "condition_log": [],
                "doctor_advice": {}, "emergency_info": {
                    "doctor_name": "", "doctor_contact": "",
                    "emergency_contact_name": "", "emergency_contact_phone": ""
                }
            }
    else:
        print("No existing data file found. Starting fresh.")

def get_timestamp():
    """Returns a formatted current timestamp."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def print_disclaimer():
    print("\nIMPORTANT DISCLAIMER:")
    print("This chatbot is an informational tool and NOT a substitute for professional medical advice, diagnosis, or treatment.")
    print("Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.")
    print("If you think you may have a medical emergency, call your doctor or emergency services immediately.")
    print("-" * 30)

# --- Chatbot Feature Functions ---

def setup_profile():
    """Guides user to set up their basic profile and emergency info."""
    print("\n--- Patient Profile Setup ---")
    patient_data["profile"]["name"] = input("What is your name? ")
    patient_data["profile"]["main_condition"] = input("What is your primary diagnosed condition (e.g., Hypertension, Diabetes)? ")
    patient_data["profile"]["allergies"] = input("Any known allergies (comma-separated, or 'None')? ")

    print("\n--- Emergency Information Setup ---")
    patient_data["emergency_info"]["doctor_name"] = input("Doctor's Name: ")
    patient_data["emergency_info"]["doctor_contact"] = input("Doctor's Contact Number: ")
    patient_data["emergency_info"]["emergency_contact_name"] = input("Emergency Contact Person's Name: ")
    patient_data["emergency_info"]["emergency_contact_phone"] = input("Emergency Contact Person's Phone: ")
    save_data()
    print("Profile and emergency information updated.")

def add_prescription():
    """Adds a new prescription to the list."""
    print("\n--- Add New Prescription ---")
    name = input("Medication Name: ")
    dosage = input("Dosage (e.g., 10mg, 1 tablet): ")
    frequency = input("Frequency (e.g., twice a day, once before bed): ")
    instructions = input("Special Instructions (e.g., with food, empty stomach): ")
    patient_data["prescriptions"].append({
        "name": name,
        "dosage": dosage,
        "frequency": frequency,
        "instructions": instructions,
        "last_taken": None # Will be updated when logged
    })
    save_data()
    print(f"Prescription for {name} added.")

def view_prescriptions():
    """Displays current prescriptions."""
    print("\n--- Your Prescriptions ---")
    if not patient_data["prescriptions"]:
        print("No prescriptions found.")
        return
    for i, p in enumerate(patient_data["prescriptions"]):
        print(f"{i+1}. {p['name']}")
        print(f"   Dosage: {p['dosage']}")
        print(f"   Frequency: {p['frequency']}")
        print(f"   Instructions: {p['instructions']}")
        last_taken_str = p['last_taken'] if p['last_taken'] else "Not yet recorded"
        print(f"   Last Taken: {last_taken_str}")
        print("-" * 10)

def log_medication_taken():
    """Logs when a medication was taken."""
    view_prescriptions()
    if not patient_data["prescriptions"]:
        return
    try:
        choice = int(input("Enter the number of the medication you took: ")) - 1
        if 0 <= choice < len(patient_data["prescriptions"]):
            medication = patient_data["prescriptions"][choice]
            medication["last_taken"] = get_timestamp()
            save_data()
            print(f"Logged {medication['name']} as taken at {medication['last_taken']}.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def log_condition():
    """Logs current symptoms or readings."""
    print("\n--- Log Current Condition ---")
    entry = input("Describe your current condition, symptoms, or readings (e.g., 'Feeling tired, BP 130/85'): ")
    patient_data["condition_log"].append({
        "timestamp": get_timestamp(),
        "entry": entry
    })
    save_data()
    print("Condition logged.")

def view_condition_log():
    """Displays the condition log."""
    print("\n--- Condition Log ---")
    if not patient_data["condition_log"]:
        print("No condition entries logged yet.")
        return
    for log in reversed(patient_data["condition_log"]): # Show most recent first
        print(f"[{log['timestamp']}] {log['entry']}")

def add_doctor_advice():
    """Allows user to add specific advice from their doctor."""
    print("\n--- Add Doctor's Advice ---")
    topic = input("What is this advice about (e.g., 'Diet for Diabetes', 'Hypertension Exercise')? ").lower()
    advice = input(f"Enter the advice Dr. {patient_data['emergency_info'].get('doctor_name', '')} gave for '{topic}':\n")
    patient_data["doctor_advice"][topic] = advice
    save_data()
    print("Doctor's advice added/updated.")

def view_doctor_advice():
    """Displays stored doctor's advice."""
    print("\n--- Doctor's Advice ---")
    if not patient_data["doctor_advice"]:
        print("No specific doctor's advice has been recorded yet.")
        print("You can add some using the 'Add Doctor's Advice' option.")
        return
    
    if patient_data["profile"].get("main_condition"):
        main_cond_advice = patient_data["doctor_advice"].get(patient_data["profile"]["main_condition"].lower())
        if main_cond_advice:
            print(f"\nAdvice for your main condition ({patient_data['profile']['main_condition']}):")
            print(f"- {main_cond_advice}")

    print("\nAll recorded advice:")
    for topic, advice in patient_data["doctor_advice"].items():
        print(f"- For '{topic.capitalize()}': {advice}")

    query = input("Search for advice on a specific topic (or press Enter to skip): ").lower()
    if query and query in patient_data["doctor_advice"]:
        print(f"\nAdvice for '{query.capitalize()}':")
        print(patient_data["doctor_advice"][query])
    elif query:
        print(f"No specific advice found for '{query}'.")


def view_home_remedies():
    """Displays pre-defined home remedies."""
    print("\n--- Home Remedies (for MILD issues - always consult your doctor for serious conditions) ---")
    for ailment, remedies in HOME_REMEDIES_DB.items():
        print(f"\nFor {ailment}:")
        for i, remedy in enumerate(remedies):
            print(f"  {i+1}. {remedy}")
    print_disclaimer()

def show_emergency_info():
    """Displays emergency contact information."""
    print("\n--- EMERGENCY INFORMATION ---")
    print("IF THIS IS A MEDICAL EMERGENCY, CALL YOUR LOCAL EMERGENCY NUMBER (e.g., 911, 112, 999) IMMEDIATELY!")
    print("-" * 20)
    info = patient_data["emergency_info"]
    print(f"Your Doctor: Dr. {info.get('doctor_name', 'N/A')}")
    print(f"Doctor's Contact: {info.get('doctor_contact', 'N/A')}")
    print("-" * 20)
    print(f"Emergency Contact Person: {info.get('emergency_contact_name', 'N/A')}")
    print(f"Emergency Contact Phone: {info.get('emergency_contact_phone', 'N/A')}")
    print("-" * 20)
    print("Remember your known allergies:", patient_data.get("profile", {}).get("allergies", "N/A"))
    print("Your primary condition:", patient_data.get("profile", {}).get("main_condition", "N/A"))
    print_disclaimer()

# --- Main Chatbot Loop ---
def main():
    load_data()

    if not patient_data["profile"] or not patient_data["emergency_info"]["doctor_name"]:
        print("Welcome! It looks like this is your first time or your profile is incomplete.")
        setup_profile()

    print_disclaimer()
    patient_name = patient_data.get("profile", {}).get("name", "User")
    print(f"\nHello, {patient_name}! How can I help you today?")

    while True:
        print("\nOffline Patient Monitor Menu:")
        print("1.  View/Update Profile & Emergency Info")
        print("2.  Add New Prescription")
        print("3.  View My Prescriptions")
        print("4.  Log Medication Taken")
        print("5.  Log My Current Condition/Symptoms")
        print("6.  View Condition Log")
        print("7.  Add Doctor's Specific Advice")
        print("8.  View Doctor's Advice")
        print("9.  View General Home Remedies")
        print("10. Show Emergency Information")
        print("0.  Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            setup_profile()
        elif choice == '2':
            add_prescription()
        elif choice == '3':
            view_prescriptions()
        elif choice == '4':
            log_medication_taken()
        elif choice == '5':
            log_condition()
        elif choice == '6':
            view_condition_log()
        elif choice == '7':
            add_doctor_advice()
        elif choice == '8':
            view_doctor_advice()
        elif choice == '9':
            view_home_remedies()
        elif choice == '10':
            show_emergency_info()
        elif choice == '0':
            print("Exiting. Stay healthy!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()