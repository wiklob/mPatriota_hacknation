#!/usr/bin/env python3
"""
Sejm Document Downloader - Downloads "uzasadnienie" files from Polish Sejm API.

Fetches all "Rządowy" (government) legislative processes and downloads
the uzasadnienie (justification) .docx files.

Usage:
    python download_sejm.py [--limit N] [--dry-run]
"""

import argparse
import json
import os
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import requests

# Configuration
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
DOWNLOAD_LOG = BASE_DIR / "download_log.json"

API_BASE = "https://api.sejm.gov.pl/sejm/term10"
PROCESSES_URL = f"{API_BASE}/processes"
PRINTS_URL = f"{API_BASE}/prints"

# Rate limiting
REQUEST_DELAY = 0.3  # seconds between requests


def get_rzadowy_processes(limit: int = None) -> list:
    """Fetch all processes with 'Rządowy' in title."""
    params = {
        "title": "Rządowy",
        "limit": limit or 1000  # API max
    }

    print(f"Fetching Rządowy processes from API...")
    response = requests.get(PROCESSES_URL, params=params)
    response.raise_for_status()

    processes = response.json()
    print(f"Found {len(processes)} Rządowy processes")
    return processes


def get_print_details(print_number: str) -> dict:
    """Fetch details for a specific print including attachments."""
    url = f"{PRINTS_URL}/{print_number}"
    response = requests.get(url)

    if response.status_code == 404:
        return None

    response.raise_for_status()
    return response.json()


def find_uzasadnienie_attachment(attachments: list, prefer_docx: bool = True) -> str:
    """Find the uzasadnienie file from attachments list.

    Prefers .docx but falls back to .pdf if no docx available.
    """
    docx_file = None
    pdf_file = None

    for attachment in attachments:
        if "uzasadnienie" in attachment.lower():
            if attachment.endswith(".docx"):
                docx_file = attachment
            elif attachment.endswith(".pdf"):
                pdf_file = attachment

    if prefer_docx and docx_file:
        return docx_file
    elif docx_file:
        return docx_file
    elif pdf_file:
        return pdf_file
    return None


def download_attachment(print_number: str, attachment_name: str, output_dir: Path) -> Path:
    """Download an attachment file."""
    url = f"{PRINTS_URL}/{print_number}/{quote(attachment_name)}"
    output_path = output_dir / attachment_name

    # Skip if already exists
    if output_path.exists():
        return output_path

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return output_path


def load_download_log() -> dict:
    """Load existing download log."""
    if DOWNLOAD_LOG.exists():
        with open(DOWNLOAD_LOG, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"downloaded": [], "errors": [], "last_run": None}


def save_download_log(log: dict):
    """Save download log."""
    log["last_run"] = datetime.now().isoformat()
    with open(DOWNLOAD_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Download Sejm uzasadnienie documents")
    parser.add_argument("--limit", type=int, help="Limit number of processes to fetch")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be downloaded without downloading")
    parser.add_argument("--skip-existing", action="store_true", default=True, help="Skip already downloaded files")
    args = parser.parse_args()

    # Ensure directories exist
    INPUT_DIR.mkdir(exist_ok=True)

    # Load download log
    log = load_download_log()
    already_downloaded = set(log["downloaded"])

    # Fetch processes
    processes = get_rzadowy_processes(limit=args.limit)

    downloaded_count = 0
    skipped_count = 0
    error_count = 0
    no_uzasadnienie_count = 0

    print(f"\nProcessing {len(processes)} legislative processes...")
    print("-" * 60)

    for i, process in enumerate(processes, 1):
        print_number = process["number"]
        title = process["title"][:60] + "..." if len(process["title"]) > 60 else process["title"]

        print(f"[{i}/{len(processes)}] Print #{print_number}: {title}")

        # Skip if already downloaded
        if print_number in already_downloaded and args.skip_existing:
            print(f"  → Skipped (already downloaded)")
            skipped_count += 1
            continue

        try:
            # Get print details
            time.sleep(REQUEST_DELAY)
            print_details = get_print_details(print_number)

            if not print_details:
                print(f"  → Print not found")
                error_count += 1
                continue

            attachments = print_details.get("attachments", [])
            uzasadnienie = find_uzasadnienie_attachment(attachments)

            if not uzasadnienie:
                print(f"  → No uzasadnienie.docx found (attachments: {attachments})")
                no_uzasadnienie_count += 1
                continue

            if args.dry_run:
                print(f"  → Would download: {uzasadnienie}")
            else:
                # Download the file
                time.sleep(REQUEST_DELAY)
                output_path = download_attachment(print_number, uzasadnienie, INPUT_DIR)
                print(f"  → Downloaded: {output_path.name}")

                # Update log
                log["downloaded"].append(print_number)
                already_downloaded.add(print_number)
                downloaded_count += 1

                # Save log periodically
                if downloaded_count % 10 == 0:
                    save_download_log(log)

        except requests.RequestException as e:
            print(f"  → Error: {e}")
            log["errors"].append({
                "print_number": print_number,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            error_count += 1
        except Exception as e:
            print(f"  → Unexpected error: {e}")
            error_count += 1

    # Final save
    save_download_log(log)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total processes:        {len(processes)}")
    print(f"Downloaded:             {downloaded_count}")
    print(f"Skipped (existing):     {skipped_count}")
    print(f"No uzasadnienie found:  {no_uzasadnienie_count}")
    print(f"Errors:                 {error_count}")
    print(f"\nFiles saved to: {INPUT_DIR}")
    print(f"Download log: {DOWNLOAD_LOG}")


if __name__ == "__main__":
    main()
