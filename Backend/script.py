import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --- PATH & GOOGLE SHEETS SETUP ---
# BASE_DIR dynamic path dynamically file location detect karta hai
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")

# Apne Google Sheet ka exact Title ya Name yahan check karke likhein
SPREADSHEET_NAME = "bigquery"  

def get_sheet_client():
    """
    Service AccountCredentials load karta hai aur Google Sheets client return karta hai.
    """
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
    return gspread.authorize(creds)

# --- PANDAS & WORD EXTRACTION LOGIC ---
def extract_main_word(term):
    """
    Extracts the most relevant word from a search phrase.
    Priority list check hoti hai, warna longest word return hota hai.
    """
    if not isinstance(term, str) or not term.strip():
        return ""
    
    # Text cleaning: Lowercase aur basic cleaning
    words = term.lower().split()
    
    # Priority Keywords Hierarchy
    priority_words = [
        "franchise", "business", "marketing", "preschool", 
        "currency", "school", "company", "ideas", "cost"
    ]
    
    # 1. First priority check
    for p in priority_words:
        if p in words:
            return p
            
    # 2. Fallback: Filter short stop words and pick the longest relevant word
    stop_words = {"the", "a", "an", "in", "of", "for", "and", "or", "to", "is", "best", "top", "near", "me"}
    filtered_words = [w for w in words if w not in stop_words]
    
    if filtered_words:
        filtered_words.sort(key=len, reverse=True)
        return filtered_words[0]
        
    return words[0] if words else ""

# --- MAIN EXECUTION PIPELINE ---
def process_data():
    print("Connecting to Google Sheet...")
    try:
        client = get_sheet_client()
        sheet = client.open(SPREADSHEET_NAME).sheet1
    except Exception as e:
        print(f"\n[ERROR] Sheet Connection Failed: {e}")
        print("Tip: Check karein ki SPREADSHEET_NAME exact match hai aur Google Sheet ko Service Account Email ke sath 'Editor' access diya hua hai.\n")
        return

    # 1. Google Sheet se Data load karein
    records = sheet.get_all_records()
    if not records:
        print("No data found in Google Sheet.")
        return

    df = pd.DataFrame(records)
    print(f"Loaded {len(df)} rows from Google Sheet.")

    # Validate column presence
    if 'Search term' not in df.columns:
        print("Error: 'Search term' column missing in Google Sheet.")
        return

    # 2. Extract Logic Apply karein
    print("Processing logic via Pandas...")
    df['One Word'] = df['Search term'].apply(extract_main_word)

    # 3. Google Sheet Updates (Clear and write back)
    print("Updating Google Sheet...")
    updated_data = [df.columns.tolist()] + df.values.tolist()
    sheet.clear()
    sheet.update(range_name="A1", values=updated_data)

    # 4. Local CSV Backup Save karein
    output_dir = os.path.join(BASE_DIR, "..", "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "processed_output.csv")
    df.to_csv(output_path, index=False)
    
    print(f"\n[SUCCESS] Google Sheet updated successfully!")
    print(f"Local backup file saved at: {os.path.abspath(output_path)}\n")

if __name__ == "__main__":
    process_data()