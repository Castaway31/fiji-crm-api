# import_excel_to_api.py
import pandas as pd
import requests
import time

# 🔥 Replace with your actual Render API URL
API_URL = "https://fiji-crm-api.onrender.com/clients"

# Read your Excel file
try:
    df = pd.read_excel("leads.xlsx", dtype=str)
    df.fillna("", inplace=True)
    print(f"✅ Loaded {len(df)} leads from Excel")
except Exception as e:
    print(f"❌ Could not read leads.xlsx: {e}")
    exit()

# Map islands (basic)
def get_island(resort_name):
    if "Mana" in resort_name: return "Yasawa"
    elif "Radisson" in resort_name: return "Nadi"
    elif "Club Whyndam" in resort_name: return "Denarau"
    elif "Plantation" in resort_name: return "Mamanuca"
    elif "Crowne Plaza" in resort_name: return "Nadi"
    else: return ""

# Send each client to the API
for index, row in df.iterrows():
    client_data = {
        "name": row["Lead Name"].strip(),
        "island": get_island(row["Lead Name"]),
        "contact_person": row["Contact Information"].split("-")[0].strip() if "-" in row["Contact Information"] else "",
        "phone": "".join([c for c in row["Contact Information"] if c.isdigit() and len(c) <= 10]),
        "email": [word for word in row["Contact Information"].split() if "@" in word][0] if "@" in row["Contact Information"] else "",
        "sales_manager": row["Sales Manager"],
        "goal": row["Goal"],
        "notes": row["Notes"]
    }

    try:
        response = requests.post(API_URL, json=client_data)
        if response.status_code in [200, 201]:
            print(f"✅ Added: {client_data['name']}")
        else:
            print(f"❌ Failed: {client_data['name']} -> {response.status_code} {response.text}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

    time.sleep(0.5)  # Be gentle with free-tier API

print("🎉 All done! Check your CRM at https://fiji-crm-api.onrender.com/clients")
