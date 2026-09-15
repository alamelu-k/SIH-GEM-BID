"""
evaluate_all.py — CodeVeil Live Compliance Evaluation & Accuracy Benchmark

Evaluates all seeded bidders against their tender requirements via the CodeVeil
compliance evaluation endpoint and compares results against full_ground_truth.csv.

Endpoints called:
  - GET  http://127.0.0.1:8000/api/v1/bidders
  - POST http://127.0.0.1:8000/api/v1/compliance/evaluate/{bidder_id}

No existing files in the repository are modified.
"""

import os
import sys
import csv
from pathlib import Path
from typing import Dict, Any, List, Tuple
import requests

# Base URL for CodeVeil Backend API
API_BASE_URL = os.environ.get("CODEVEIL_API_URL", "http://127.0.0.1:8000/api/v1")

# Paths
REPO_ROOT = Path(__file__).resolve().parent
INTEGRATION_DIR = REPO_ROOT / "integration"
if not INTEGRATION_DIR.exists():
    INTEGRATION_DIR = Path.cwd() / "integration"

GROUND_TRUTH_CSV_PATH = REPO_ROOT / "full_ground_truth.csv"
if not GROUND_TRUTH_CSV_PATH.exists():
    GROUND_TRUTH_CSV_PATH = INTEGRATION_DIR / "full_ground_truth.csv"


def check_api_health():
    """Verify backend server connectivity before running evaluations."""
    root_url = API_BASE_URL.replace("/api/v1", "/")
    print(f"Connecting to CodeVeil API at: {API_BASE_URL}")
    try:
        res = requests.get(root_url, timeout=5)
        if res.status_code == 200:
            info = res.json()
            print(f"API is ONLINE: {info.get('system')} (v{info.get('version')})")
        else:
            print(f"Warning: Root endpoint returned HTTP {res.status_code}")
    except Exception as ex:
        print(f"ERROR: Cannot connect to CodeVeil API at {API_BASE_URL}: {ex}")
        print("Please ensure the FastAPI server is running (e.g. uvicorn app.main:app --reload)")
        sys.exit(1)


def get_all_bidders() -> List[Dict[str, Any]]:
    """Step 1: Call GET /api/v1/bidders to get all seeded bidders."""
    url = f"{API_BASE_URL}/bidders"
    print(f"\n[Step 1] Fetching bidders from {url}...")
    res = requests.get(url, timeout=15)
    if res.status_code != 200:
        print(f"ERROR: Failed to fetch bidders: HTTP {res.status_code}: {res.text}")
        sys.exit(1)

    bidders = res.json()
    print(f"Retrieved {len(bidders)} bidders from database.")
    return bidders


def evaluate_bidders(bidders: List[Dict[str, Any]]) -> Tuple[Dict[int, Dict[str, Any]], Dict[Tuple[str, str], str]]:
    """
    Step 2 & 3:
      - Call POST /api/v1/compliance/evaluate/{bidder_id} for each bidder.
      - Store full response.
      - Parse requirement rule_code and resulting status from matrix_results.
    """
    print("\n[Step 2 & 3] Running compliance evaluation for each bidder...")
    full_responses: Dict[int, Dict[str, Any]] = {}
    live_results: Dict[Tuple[str, str], str] = {}  # (legal_name, requirement_code) -> status

    for bidder in bidders:
        bidder_id = bidder["id"]
        legal_name = bidder["legal_name"]
        tender_id = bidder.get("tender_id")

        url = f"{API_BASE_URL}/compliance/evaluate/{bidder_id}"
        try:
            res = requests.post(url, timeout=90)
            if res.status_code == 200:
                data = res.json()
                full_responses[bidder_id] = data
                matrix = data.get("matrix_results", [])
                overall = data.get("overall_status")
                print(f"  -> Bidder {bidder_id:2d}: {legal_name[:38]:<38} | Tender ID: {tender_id} | Overall: {overall:<8} | Req Count: {len(matrix)}")

                for item in matrix:
                    req_code = item.get("rule_code") or item.get("code")
                    status = item.get("status")
                    if req_code:
                        live_results[(legal_name, req_code)] = status
            else:
                print(f"  -> Bidder {bidder_id:2d}: {legal_name} | FAILED HTTP {res.status_code}: {res.text}")
        except Exception as ex:
            print(f"  -> Bidder {bidder_id:2d}: {legal_name} | ERROR: {ex}")

    print(f"Evaluations complete. Extracted {len(live_results)} live requirement verdicts.")
    return full_responses, live_results


def compare_with_ground_truth(live_results: Dict[Tuple[str, str], str]):
    """
    Step 4, 5, 6:
      - Load full_ground_truth.csv.
      - Compare each row (legal_name + requirement_code) against live result.
      - Print summary table and list of all mismatches.
      - Print overall accuracy percentage.
    """
    print(f"\n[Step 4] Loading ground truth from {GROUND_TRUTH_CSV_PATH}...")
    if not GROUND_TRUTH_CSV_PATH.is_file():
        print(f"ERROR: Ground truth file not found at {GROUND_TRUTH_CSV_PATH}")
        sys.exit(1)

    total_compared = 0
    matching_count = 0
    mismatch_count = 0
    mismatches = []

    with open(GROUND_TRUTH_CSV_PATH, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_compared += 1
            # Note: In full_ground_truth.csv, the 'bidder_id' column holds the legal_name
            bidder_name = row.get("bidder_id", "").strip()
            req_code = row.get("requirement_code", "").strip()
            expected_status = row.get("expected_result", "").strip()
            archetype = row.get("archetype", "").strip()

            actual_status = live_results.get((bidder_name, req_code))

            if actual_status == expected_status:
                matching_count += 1
            else:
                mismatch_count += 1
                mismatches.append({
                    "bidder_name": bidder_name,
                    "archetype": archetype,
                    "requirement_code": req_code,
                    "expected_status": expected_status,
                    "actual_status": actual_status if actual_status is not None else "NOT_FOUND",
                })

    # Step 5: Summary Table
    print("\n" + "=" * 80)
    print("                      EVALUATION SUMMARY")
    print("=" * 80)
    print(f"  Total Rows Compared : {total_compared}")
    print(f"  Matching Verdicts   : {matching_count}")
    print(f"  Mismatching Verdicts: {mismatch_count}")

    # Step 6: Overall Accuracy
    accuracy = (matching_count / total_compared * 100.0) if total_compared > 0 else 0.0
    print(f"  Overall Accuracy    : {accuracy:.2f}%")
    print("=" * 80)

    # Detailed list of mismatches
    if mismatches:
        print("\n" + "-" * 92)
        print(f"{'#':<3} | {'Bidder Legal Name':<35} | {'Requirement':<20} | {'Expected':<13} | {'Actual':<13}")
        print("-" * 92)
        for idx, m in enumerate(mismatches, 1):
            print(f"{idx:<3} | {m['bidder_name']:<35} | {m['requirement_code']:<20} | {m['expected_status']:<13} | {m['actual_status']:<13}")
        print("-" * 92)
    else:
        print("\n[PERFECT MATCH] All live API evaluations match ground truth exactly!")

    print(f"\nFinal Overall Accuracy: {accuracy:.2f}%\n")
    return total_compared, matching_count, mismatch_count, accuracy


def main():
    check_api_health()
    bidders = get_all_bidders()
    if not bidders:
        print("ERROR: No bidders found in database. Run seed_data.py first.")
        sys.exit(1)

    full_responses, live_results = evaluate_bidders(bidders)
    compare_with_ground_truth(live_results)


if __name__ == "__main__":
    main()
