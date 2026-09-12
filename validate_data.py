"""
CodeVeil ground-truth validator.

Checks:
1. Every requirement_code in full_ground_truth.csv exists in
   codeveil_tender_requirements.json for that tender.
2. Every bidder has a ground-truth row for every requirement of their tender
   (no gaps).
3. Every MANDATORY requirement has an expected_result that is not blank.
4. Flags any bidder whose expected_result for a mandatory requirement is not
   one of the 5 known statuses.

Run: python3 validate_data.py
Exits with code 1 if any error is found (useful in CI).
"""
import csv
import json
import sys

REQUIREMENTS_JSON = "codeveil_tender_requirements.json"
GROUND_TRUTH_CSV = "full_ground_truth.csv"
BIDDERS_CSV = "bidder_archetypes.csv"

VALID_STATUSES = {"PASS", "FAIL", "MISSING", "MISMATCH", "MANUAL_REVIEW"}


def load_requirements():
    with open(REQUIREMENTS_JSON, encoding="utf-8") as f:
        tenders = json.load(f)
    # tender_number -> {code: mandatory}
    req_map = {}
    for t in tenders:
        req_map[t["tender_number"]] = {
            r["code"]: r["mandatory"] for r in t["requirements"]
        }
    return req_map


def load_ground_truth():
    with open(GROUND_TRUTH_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_bidders():
    with open(BIDDERS_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    errors = []
    warnings = []

    req_map = load_requirements()
    ground_truth = load_ground_truth()
    bidders = load_bidders()

    # Index ground truth by (bidder_id, tender_number) -> {code: row}
    gt_index = {}
    for row in ground_truth:
        key = (row["bidder_id"], row["tender_number"])
        gt_index.setdefault(key, {})[row["requirement_code"]] = row

    # 1 & 2: every bidder has every requirement code for their tender, and
    # every code that IS present is a real code.
    for b in bidders:
        tn = b["tender_number"]
        legal_name = b["legal_name"]
        if tn not in req_map:
            errors.append(f"[{legal_name}] references unknown tender_number '{tn}'")
            continue

        expected_codes = set(req_map[tn].keys())
        bidder_rows = gt_index.get((legal_name, tn), {})
        present_codes = set(bidder_rows.keys())

        missing_codes = expected_codes - present_codes
        for code in missing_codes:
            mandatory = req_map[tn][code]
            msg = f"[{legal_name}] missing ground-truth row for '{code}' (mandatory={mandatory})"
            if mandatory:
                errors.append(msg)
            else:
                warnings.append(msg)

        unknown_codes = present_codes - expected_codes
        for code in unknown_codes:
            errors.append(
                f"[{legal_name}] ground-truth references '{code}', which does not "
                f"exist in requirements JSON for tender '{tn}'"
            )

    # 3 & 4: every row's expected_result is valid, and mandatory rows aren't blank.
    for row in ground_truth:
        code = row["requirement_code"]
        tn = row["tender_number"]
        legal_name = row["bidder_id"]
        result = row["expected_result"].strip()
        mandatory = req_map.get(tn, {}).get(code)

        if not result:
            msg = f"[{legal_name}] blank expected_result for '{code}'"
            if mandatory:
                errors.append(msg)
            else:
                warnings.append(msg)
            continue

        if result not in VALID_STATUSES:
            errors.append(
                f"[{legal_name}] '{code}' has expected_result='{result}', "
                f"not one of {sorted(VALID_STATUSES)}"
            )

    # Report
    print(f"Checked {len(ground_truth)} ground-truth rows across {len(bidders)} bidders.\n")

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(" -", w)
        print()

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(" -", e)
        print("\nFAILED.")
        sys.exit(1)

    print("All checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
