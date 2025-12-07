
import json
import requests
import re
from pathlib import Path

RESULTS_FILE = "output/results_20251206_141442.json"
OUTPUT_FILE = "orphan_titles.json"
API_PRINTS = "https://api.sejm.gov.pl/sejm/term10/prints"

def get_print_title(print_number):
    try:
        response = requests.get(f"{API_PRINTS}/{print_number}")
        if response.status_code == 200:
            data = response.json()
            return data.get("title")
    except Exception as e:
        print(f"Error fetching title for {print_number}: {e}")
    return None

def main():
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    orphans = []
    for result in data.get("results", []):
        # Check if no codes were found
        if result.get("codes", {}).get("total_matches", 0) == 0:
            filename = result["source_file"]
            # Extract print number (assuming format number-uzasadnienie...)
            match = re.match(r"(\d+)-", filename)
            if match:
                print_number = match.group(1)
                title = get_print_title(print_number)
                if title:
                    orphans.append({
                        "filename": filename,
                        "print_number": print_number,
                        "title": title
                    })
                    print(f"Found title for {filename}: {title[:50]}...")
            else:
                print(f"Could not parse print number from {filename}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(orphans, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(orphans)} orphan titles to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
