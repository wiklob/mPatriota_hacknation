
import json
from pathlib import Path
import re

# Find the latest results file
OUTPUT_DIR = Path("output")
results_files = sorted(OUTPUT_DIR.glob("results_*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
if not results_files:
    print("No results file found.")
    exit(1)

LATEST_RESULTS = results_files[0]
print(f"Updating {LATEST_RESULTS}...")

with open(LATEST_RESULTS, "r", encoding="utf-8") as f:
    data = json.load(f)

# Manual mapping based on research
MAPPING = {
    "2026": "UD330",
    "2027": "UD152",
    "1951": "UD297",
    "2028": "UD197",
    "1995": "UD331",
    "1996": "UD319" # Best guess based on search
}

updated_count = 0

for result in data["results"]:
    filename = result["source_file"]
    match = re.match(r"(\d+)-", filename)
    if match:
        print_number = match.group(1)
        
        # Check if we have a mapping and NO existing codes
        if print_number in MAPPING and result.get("codes", {}).get("total_matches", 0) == 0:
            code = MAPPING[print_number]
            print(f"Linking {filename} -> {code}")
            
            # Update the structure
            if "manual_link" not in result:
                result["manual_link"] = {}
            
            result["manual_link"]["rcl_code"] = code
            result["manual_link"]["source"] = "Inferred from Title Search"
            updated_count += 1

# Save to new file
OUTPUT_FILE = OUTPUT_DIR / f"results_linked_{LATEST_RESULTS.stem.split('_')[1]}.json"
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Saved linked results to {OUTPUT_FILE}")
print(f"Updated {updated_count} files.")
