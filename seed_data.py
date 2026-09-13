"""
seed_data.py — CodeVeil Database Seeder

Seeds the CodeVeil FastAPI backend (http://127.0.0.1:8000/api/v1) with:
  1. Tenders and their requirements from codeveil_tender_requirements.json
  2. Bidders from bidder_archetypes.csv
  3. Submitted documents per bidder from synthetic_documents/<bidder_folder>/*.pdf

No existing files in the repository are modified.
"""

import os
import sys
import json
import csv
import re
from pathlib import Path
import requests

# Base URL for CodeVeil Backend API
API_BASE_URL = os.environ.get("CODEVEIL_API_URL", "http://127.0.0.1:8000/api/v1")

# Locate data paths relative to repo root or integration directory
REPO_ROOT = Path(__file__).resolve().parent
INTEGRATION_DIR = REPO_ROOT / "integration"
if not INTEGRATION_DIR.exists():
    INTEGRATION_DIR = Path.cwd() / "integration"

TENDERS_JSON_PATH = INTEGRATION_DIR / "codeveil_tender_requirements.json"
BIDDERS_CSV_PATH = INTEGRATION_DIR / "bidder_archetypes.csv"
SYNTH_DOCS_DIR = INTEGRATION_DIR / "synthetic_documents"


def get_existing_tenders():
    """Fetch existing tenders from backend to map tender_number -> id."""
    try:
        res = requests.get(f"{API_BASE_URL}/tenders", timeout=10)
        if res.status_code == 200:
            return {t["tender_number"]: t["id"] for t in res.json()}
    except Exception:
        pass
    return {}


def find_bidder_doc_folder(synth_dir: Path, tender_number: str, archetype: str, legal_name: str) -> Path:
    """Locate the bidder's document folder under synthetic_documents/."""
    tender_short = tender_number.split("/")[-1]
    safe_name = re.sub(r"[^A-Za-z0-9]+", "_", legal_name).strip("_")
    expected_folder_name = f"{tender_short}_{archetype}_{safe_name}"
    direct_path = synth_dir / expected_folder_name
    if direct_path.is_dir():
        return direct_path

    # Fallback search if exact sanitized name differs slightly
    if synth_dir.is_dir():
        for item in synth_dir.iterdir():
            if item.is_dir() and item.name.startswith(f"{tender_short}_{archetype}"):
                return item

    return direct_path


def seed_tenders():
    """Reads tenders JSON and POSTs to /api/v1/tenders."""
    print("=" * 60)
    print("Step 1: Seeding Tenders & Requirements")
    print(f"Reading: {TENDERS_JSON_PATH}")
    print("=" * 60)

    if not TENDERS_JSON_PATH.is_file():
        err = f"File not found at {TENDERS_JSON_PATH}"
        print(f"ERROR: {err}")
        return {}, 0, [(str(TENDERS_JSON_PATH), err)]

    with open(TENDERS_JSON_PATH, "r", encoding="utf-8") as f:
        tenders_data = json.load(f)

    existing_tenders = get_existing_tenders()
    tender_id_map = dict(existing_tenders)

    successful = 0
    failures = []

    for tender in tenders_data:
        t_num = tender.get("tender_number")
        print(f"-> POSTing tender: {t_num} ({tender.get('title', '')[:45]}...)")
        try:
            res = requests.post(f"{API_BASE_URL}/tenders", json=tender, timeout=15)
            if res.status_code == 201:
                created = res.json()
                tender_id = created["id"]
                tender_id_map[t_num] = tender_id
                successful += 1
                req_count = len(created.get("requirements", []))
                print(f"   [CREATED] Tender ID: {tender_id} with {req_count} requirements.")
            else:
                err_msg = f"HTTP {res.status_code}: {res.text}"
                failures.append((t_num, err_msg))
                print(f"   [FAILED] {err_msg}")
                # If tender already exists in database, retrieve its ID so bidders can still link
                if t_num in existing_tenders:
                    print(f"   [NOTE] Using already existing Tender ID: {existing_tenders[t_num]}")
        except Exception as ex:
            err_msg = f"Request error: {ex}"
            failures.append((t_num, err_msg))
            print(f"   [ERROR] {err_msg}")

    return tender_id_map, successful, failures


def seed_bidders(tender_id_map):
    """Reads bidder archetypes CSV and POSTs to /api/v1/bidders."""
    print("\n" + "=" * 60)
    print("Step 2: Seeding Bidders")
    print(f"Reading: {BIDDERS_CSV_PATH}")
    print("=" * 60)

    if not BIDDERS_CSV_PATH.is_file():
        err = f"File not found at {BIDDERS_CSV_PATH}"
        print(f"ERROR: {err}")
        return [], 0, [(str(BIDDERS_CSV_PATH), err)]

    with open(BIDDERS_CSV_PATH, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        bidders_data = list(reader)

    created_bidders = []  # List of tuples: (row_dict, bidder_id)
    successful = 0
    failures = []

    for row in bidders_data:
        t_num = row.get("tender_number", "").strip()
        legal_name = row.get("legal_name", "").strip()
        archetype = row.get("archetype", "").strip()

        tender_id = tender_id_map.get(t_num)
        if not tender_id:
            err_msg = f"Tender number '{t_num}' not found in database or ID map."
            failures.append((f"{legal_name} ({t_num})", err_msg))
            print(f"   [SKIPPED] {legal_name}: {err_msg}")
            continue

        payload = {
            "tender_id": tender_id,
            "legal_name": legal_name,
            "pan": row.get("pan", "").strip() or None,
            "gstin": row.get("gstin", "").strip() or None,
            "udyam_number": row.get("udyam_number", "").strip() or None,
        }

        print(f"-> POSTing bidder: {legal_name} [{archetype}] (Tender ID: {tender_id})")
        try:
            res = requests.post(f"{API_BASE_URL}/bidders", json=payload, timeout=15)
            if res.status_code == 201:
                created = res.json()
                bidder_id = created["id"]
                created_bidders.append((row, bidder_id))
                successful += 1
                print(f"   [CREATED] Bidder ID: {bidder_id}")
            else:
                err_msg = f"HTTP {res.status_code}: {res.text}"
                failures.append((f"{legal_name} ({archetype})", err_msg))
                print(f"   [FAILED] {err_msg}")
        except Exception as ex:
            err_msg = f"Request error: {ex}"
            failures.append((f"{legal_name} ({archetype})", err_msg))
            print(f"   [ERROR] {err_msg}")

    return created_bidders, successful, failures


def seed_documents(created_bidders):
    """For each bidder, finds synthetic_documents folder and POSTs each PDF to /api/v1/bidders/{id}/documents."""
    print("\n" + "=" * 60)
    print("Step 3: Seeding Bidder Documents")
    print(f"Directory: {SYNTH_DOCS_DIR}")
    print("=" * 60)

    successful = 0
    failures = []

    for row, bidder_id in created_bidders:
        t_num = row.get("tender_number", "").strip()
        archetype = row.get("archetype", "").strip()
        legal_name = row.get("legal_name", "").strip()

        folder = find_bidder_doc_folder(SYNTH_DOCS_DIR, t_num, archetype, legal_name)
        if not folder.is_dir():
            err_msg = f"Document folder not found: {folder}"
            failures.append((f"Bidder {bidder_id}: {legal_name}", err_msg))
            print(f"   [WARNING] {err_msg}")
            continue

        # Collect unique PDF files in the bidder's directory (case-insensitive deduplication)
        pdf_files = sorted([f for f in folder.iterdir() if f.is_file() and f.suffix.lower() == ".pdf"])
        print(f"-> Bidder ID {bidder_id} ({legal_name} [{archetype}]): found {len(pdf_files)} PDFs in {folder.name}")

        for pdf_path in pdf_files:
            file_name = pdf_path.name
            doc_type = pdf_path.stem  # e.g. PAN, GST_CERTIFICATE, UDYAM_CERTIFICATE

            payload = {
                "document_type": doc_type,
                "file_name": file_name,
                "file_path": str(pdf_path.resolve()),
                "extracted_fields": None,
            }

            try:
                res = requests.post(
                    f"{API_BASE_URL}/bidders/{bidder_id}/documents",
                    json=payload,
                    timeout=15,
                )
                if res.status_code == 201:
                    doc_res = res.json()
                    successful += 1
                    print(f"     [OK] Doc ID {doc_res.get('id')}: {doc_type} ({file_name})")
                else:
                    err_msg = f"HTTP {res.status_code}: {res.text}"
                    failures.append((f"Bidder {bidder_id} doc {file_name}", err_msg))
                    print(f"     [FAILED] {file_name} -> {err_msg}")
            except Exception as ex:
                err_msg = f"Request error: {ex}"
                failures.append((f"Bidder {bidder_id} doc {file_name}", err_msg))
                print(f"     [ERROR] {file_name} -> {err_msg}")

    return successful, failures


def print_summary(tender_stats, bidder_stats, doc_stats):
    """Prints a clear summary of all operations and lists any failures."""
    t_succ, t_fail = tender_stats
    b_succ, b_fail = bidder_stats
    d_succ, d_fail = doc_stats

    print("\n" + "=" * 70)
    print("                      SEEDING SUMMARY")
    print("=" * 70)
    print(f"Tenders   : {t_succ} successfully created | {len(t_fail)} failed")
    print(f"Bidders   : {b_succ} successfully created | {len(b_fail)} failed")
    print(f"Documents : {d_succ} successfully created | {len(d_fail)} failed")
    print("=" * 70)

    total_failures = len(t_fail) + len(b_fail) + len(d_fail)
    if total_failures == 0:
        print("[SUCCESS] All data was seeded successfully without errors!")
    else:
        print(f"[ATTENTION] {total_failures} item(s) encountered failures:")

        if t_fail:
            print("\n--- Failed Tenders ---")
            for item, err in t_fail:
                print(f"  * {item}: {err}")

        if b_fail:
            print("\n--- Failed Bidders ---")
            for item, err in b_fail:
                print(f"  * {item}: {err}")

        if d_fail:
            print("\n--- Failed Documents ---")
            for item, err in d_fail:
                print(f"  * {item}: {err}")

    print("=" * 70 + "\n")


def main():
    print("Checking connection to CodeVeil API at:", API_BASE_URL)
    try:
        health_resp = requests.get(API_BASE_URL.replace("/api/v1", "/"), timeout=5)
        if health_resp.status_code == 200:
            print(f"API is ONLINE: {health_resp.json().get('system')}")
        else:
            print(f"Warning: Root endpoint returned status {health_resp.status_code}")
    except Exception as ex:
        print(f"Connection test to {API_BASE_URL} failed: {ex}")
        print("Please ensure the FastAPI server is running (e.g. uvicorn app.main:app --reload)")
        sys.exit(1)

    tender_id_map, t_succ, t_fail = seed_tenders()
    created_bidders, b_succ, b_fail = seed_bidders(tender_id_map)
    d_succ, d_fail = seed_documents(created_bidders)

    print_summary(
        tender_stats=(t_succ, t_fail),
        bidder_stats=(b_succ, b_fail),
        doc_stats=(d_succ, d_fail),
    )


if __name__ == "__main__":
    main()
