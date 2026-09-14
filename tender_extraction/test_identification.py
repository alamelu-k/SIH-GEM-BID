import sys
from pathlib import Path

# Ensure tender_extraction is on sys.path
script_dir = Path(__file__).resolve().parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

from identify_tender import identify_and_extract


def run_tests():
    sample_dir = script_dir / "sample_tenders"
    
    test_cases = [
        {
            "filename": "tender_safety_001.pdf",
            "expected_tender_number": "GEM/2026/B/SAFETY-001",
            "expected_identified": True,
            "expected_req_count": 10,
        },
        {
            "filename": "tender_amc_002.pdf",
            "expected_tender_number": "GEM/2026/S/AMC-002",
            "expected_identified": True,
            "expected_req_count": 10,
        },
        {
            "filename": "tender_msme_003.pdf",
            "expected_tender_number": "GEM/2026/B/MSME-003",
            "expected_identified": True,
            "expected_req_count": 10,
        },
    ]

    print("=" * 80)
    print("TENDER IDENTIFICATION & EXTRACTION TEST SUITE")
    print("=" * 80)
    
    results = []
    all_passed = True

    for tc in test_cases:
        pdf_path = sample_dir / tc["filename"]
        print(f"\nTesting: {tc['filename']} ({pdf_path})")

        if not pdf_path.exists():
            print(f"  [ERROR] File not found: {pdf_path}")
            results.append((tc["filename"], "NOT FOUND", 0, "FAIL (File Missing)"))
            all_passed = False
            continue

        res = identify_and_extract(str(pdf_path))
        identified = res.get("identified", False)
        actual_tender = res.get("tender_number")
        reqs = res.get("requirements", [])
        actual_count = len(reqs)

        print(f"  Identified: {identified}")
        print(f"  Tender Number: {actual_tender} (Expected: {tc['expected_tender_number']})")
        print(f"  Requirements Extracted: {actual_count} (Expected: {tc['expected_req_count']})")
        
        # Check requirement sample
        if reqs:
            codes = [r.get("code") for r in reqs[:3]]
            print(f"  Sample Requirement Codes: {codes} ...")

        passed = (
            identified == tc["expected_identified"]
            and actual_tender == tc["expected_tender_number"]
            and actual_count == tc["expected_req_count"]
        )

        status_str = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
            print(f"  [FAIL] Reason: {res.get('reason', 'Mismatch in results')}")
        else:
            print(f"  [OK] Successfully identified and extracted.")

        results.append((tc["filename"], actual_tender, actual_count, status_str))

    # Optional negative test: non-tender document should return identified == False
    pan_pdf_candidates = [
        script_dir.parent / "synthetic_documents" / "bidder_01" / "pan_card.pdf",
        Path("synthetic_documents/bidder_01/pan_card.pdf"),
    ]
    for pan_pdf in pan_pdf_candidates:
        if pan_pdf.is_file():
            print(f"\nTesting Negative Case (Non-tender document): {pan_pdf.name}")
            neg_res = identify_and_extract(str(pan_pdf))
            neg_passed = (neg_res.get("identified") is False)
            neg_status = "PASS" if neg_passed else "FAIL"
            print(f"  Identified: {neg_res.get('identified')} (Expected: False)")
            print(f"  Reason: {neg_res.get('reason')}")
            results.append((f"{pan_pdf.name} (Negative Test)", "None", 0, neg_status))
            if not neg_passed:
                all_passed = False
            break

    # Summary Table
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    header = f"{'Document File':<32} | {'Identified Tender':<24} | {'Reqs':<5} | {'Status'}"
    print(header)
    print("-" * 80)
    for fname, tender_num, count, status in results:
        t_str = str(tender_num) if tender_num else "N/A"
        print(f"{fname:<32} | {t_str:<24} | {count:<5} | {status}")
    print("=" * 80)

    if all_passed:
        print("OVERALL RESULT: ALL TESTS PASSED (100% SUCCESS)\n")
    else:
        print("OVERALL RESULT: SOME TESTS FAILED\n")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
