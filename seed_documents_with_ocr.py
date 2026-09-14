"""
seed_documents_with_ocr.py — CodeVeil Document OCR & Field Extraction Seeder

Reads existing documents for all bidders from the backend, runs PDF text
extraction (pdf_text_extractor) and LLM field extraction (field_extractor),
and posts new document records containing populated extracted_fields.

This script only touches documents — it does not modify tenders or bidders.
No existing codebase files are modified.
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, Any, Optional
import dotenv
import requests

# Base URL for CodeVeil Backend API
API_BASE_URL = os.environ.get("CODEVEIL_API_URL", "http://127.0.0.1:8000/api/v1")

# Paths
REPO_ROOT = Path(__file__).resolve().parent
SADHANA_ML_DIR = REPO_ROOT / "sadhana-ml"
if not SADHANA_ML_DIR.exists():
    SADHANA_ML_DIR = REPO_ROOT.parent / "sadhana-ml"
ENV_PATH = SADHANA_ML_DIR / ".env"

# 1. Load environment variables from sadhana-ml/.env
if ENV_PATH.is_file():
    dotenv.load_dotenv(ENV_PATH)

# Clean any whitespace or newline artifacts that Notepad might have introduced
raw_key = os.environ.get("ANTHROPIC_API_KEY", "")
cleaned_key = re.sub(r"\s+", "", raw_key)
if cleaned_key:
    os.environ["ANTHROPIC_API_KEY"] = cleaned_key

# 2. Add sadhana-ml to sys.path so document_ai and common modules import
sys.path.insert(0, str(SADHANA_ML_DIR))

try:
    import anthropic
    from common.enums import DocumentType
    from document_ai.ocr import pdf_text_extractor
    from document_ai.extraction import field_extractor
    from document_ai.extraction.prompts import EXPECTED_FIELDS

    # Ensure field_extractor client uses the cleaned Anthropic key
    if cleaned_key:
        field_extractor._client = anthropic.Anthropic(api_key=cleaned_key)
except Exception as import_err:
    print(f"ERROR: Failed to import sadhana-ml modules: {import_err}")
    sys.exit(1)


# 4a. Mapping from database document_type strings to DocumentType enum
DOCUMENT_TYPE_MAP: Dict[str, DocumentType] = {
    "BIS_LICENSE": getattr(DocumentType, "BIS_LICENSE", None),
    "PAN": getattr(DocumentType, "PAN_CARD", None),
    "GST_CERTIFICATE": getattr(DocumentType, "GST_CERTIFICATE", None),
    "UDYAM_CERTIFICATE": getattr(DocumentType, "UDYAM_CERTIFICATE", None),
    "OEM_AUTH_LETTER": getattr(DocumentType, "OEM_AUTHORIZATION_LETTER", None),
    "EPFO_ESI_CERT": getattr(DocumentType, "EPFO_ESIC_CERTIFICATE", None),
    "FINANCIAL_STATEMENT": getattr(DocumentType, "TURNOVER_STATEMENT", None),
    # Schemas added 2026-09-14 — now active:
    "EMD_INSTRUMENT": getattr(DocumentType, "EMD_INSTRUMENT", None),
    "EXPERIENCE_CERT": getattr(DocumentType, "EXPERIENCE_CERT", None),
    "MANPOWER_LIST": getattr(DocumentType, "MANPOWER_LIST", None),
    "MII_DECLARATION": getattr(DocumentType, "MII_DECLARATION", None),
    "SLA_ACCEPTANCE": getattr(DocumentType, "SLA_ACCEPTANCE", None),
    "QUALITY_CERT": getattr(DocumentType, "QUALITY_CERT", None),
}


def resolve_file_path(file_path_str: str) -> Optional[Path]:
    """Resolves document file path from string, with fallback to repo root."""
    p = Path(file_path_str)
    if p.is_file():
        return p

    # Fallback to possible relative locations
    for candidate in [REPO_ROOT / file_path_str, REPO_ROOT.parent / file_path_str, REPO_ROOT / "integration" / file_path_str]:
        if candidate.is_file():
            return candidate

    return None


# Safety constants
BATCH_LIMIT = 20          # Hard cap: max documents to process in a single run
COST_PER_DOC = 0.0018    # USD — based on actual rate: 34 docs = $0.06 on 2026-09-13


def main():
    print("=" * 80)
    print("CodeVeil: Seeding Documents with OCR & Field Extraction")
    print(f"Backend API URL: {API_BASE_URL}")
    print(f"Anthropic API Key configured: {'Yes' if bool(cleaned_key) else 'No'}")
    print(f"Batch limit this run      : {BATCH_LIMIT} documents")
    print(f"Estimated cost per doc    : ${COST_PER_DOC:.4f}")
    print("=" * 80)

    if not cleaned_key:
        print("ERROR: ANTHROPIC_API_KEY is not set. Check c:\\SIH-Audit\\sadhana-ml\\.env.")
        sys.exit(1)

    # 3. Query GET /api/v1/bidders to get all bidders and existing documents
    try:
        res = requests.get(f"{API_BASE_URL}/bidders", timeout=15)
        if res.status_code != 200:
            print(f"ERROR: Failed to fetch bidders: HTTP {res.status_code}: {res.text}")
            sys.exit(1)
        bidders = res.json()
    except Exception as ex:
        print(f"ERROR: Could not connect to backend at {API_BASE_URL}: {ex}")
        sys.exit(1)

    total_docs = sum(len(b.get("documents", [])) for b in bidders)
    print(f"Retrieved {len(bidders)} bidders with {total_docs} existing document records.\n")

    successful_count = 0
    skipped_already_done_count = 0  # (1) already had extracted_fields — skip
    skipped_no_schema_count = 0
    skipped_doc_types = set()
    failed_other_count = 0
    failures = []

    batch_processed_this_run = 0   # (2) number of LLM calls made this run
    total_cost_this_run = 0.0      # (3) running cost accumulator

    doc_counter = 0

    batch_limit_hit = False
    for bidder in bidders:
        if batch_limit_hit:
            break

        bidder_id = bidder["id"]
        legal_name = bidder["legal_name"]
        documents = bidder.get("documents", [])

        print(f"--- Bidder ID {bidder_id}: {legal_name} ({len(documents)} docs) ---")

        for doc in documents:
            doc_counter += 1
            raw_doc_type = doc["document_type"]
            file_name = doc["file_name"]
            file_path_str = doc["file_path"]

            doc_type_enum = DOCUMENT_TYPE_MAP.get(raw_doc_type)

            # (1) Skip if ANY document for this bidder with the same document_type already has non-empty extracted_fields
            already_done_for_bidder = any(
                d.get("document_type") == raw_doc_type
                and d.get("extracted_fields")
                and isinstance(d["extracted_fields"], dict)
                and len(d["extracted_fields"]) > 0
                for d in documents
            )
            if already_done_for_bidder:
                skipped_already_done_count += 1
                print(f"  [{doc_counter:3d}/{total_docs:3d}] SKIP (done)      : {raw_doc_type:<20} | {file_name} (already populated for bidder)")
                continue

            # 4b. Check if schema is available
            if not doc_type_enum or doc_type_enum not in EXPECTED_FIELDS:
                skipped_no_schema_count += 1
                skipped_doc_types.add(raw_doc_type)
                print(f"  [{doc_counter:3d}/{total_docs:3d}] SKIP (no schema) : {raw_doc_type:<20} | {file_name}")
                continue

            # (2) Hard cap: stop if batch limit reached
            if batch_processed_this_run >= BATCH_LIMIT:
                # Count remaining eligible distinct doc types per bidder
                remaining = sum(
                    1
                    for b2 in bidders
                    for dt in {d2["document_type"] for d2 in b2.get("documents", []) if DOCUMENT_TYPE_MAP.get(d2["document_type"]) in EXPECTED_FIELDS}
                    if not any(
                        d2.get("document_type") == dt
                        and d2.get("extracted_fields")
                        and isinstance(d2["extracted_fields"], dict)
                        and len(d2["extracted_fields"]) > 0
                        for d2 in b2.get("documents", [])
                    )
                ) - batch_processed_this_run
                print(f"\n{'=' * 80}")
                print(f"  BATCH LIMIT REACHED — {max(0, remaining)} documents remaining, run again to continue.")
                print(f"{'=' * 80}\n")
                batch_limit_hit = True
                break

            # Resolve file path
            file_path = resolve_file_path(file_path_str)
            if not file_path:
                failed_other_count += 1
                err = f"File not found on disk: {file_path_str}"
                failures.append((f"{legal_name} - {file_name}", err))
                print(f"  [{doc_counter:3d}/{total_docs:3d}] FAIL (file missing): {raw_doc_type:<20} | {file_name} -> {err}")
                continue

            # 4c. Extract text using pdf_text_extractor
            try:
                text = pdf_text_extractor.full_text(file_path)
            except Exception as ex:
                failed_other_count += 1
                err = f"Text extraction failed: {ex}"
                failures.append((f"{legal_name} - {file_name}", err))
                print(f"  [{doc_counter:3d}/{total_docs:3d}] FAIL (text extract): {raw_doc_type:<20} | {file_name} -> {err}")
                continue

            # 4d & 4e. Run field_extractor.extract_fields() and convert to dict
            try:
                extracted = field_extractor.extract_fields(
                    document_type=doc_type_enum,
                    ocr_text=text,
                    document_id=f"bidder-{bidder_id}-{file_name}",
                )
                fields_dict = {f.field_name: f.value for f in extracted}
            except Exception as ex:
                failed_other_count += 1
                err = f"Field extraction LLM error: {ex}"
                failures.append((f"{legal_name} - {file_name}", err))
                print(f"  [{doc_counter:3d}/{total_docs:3d}] FAIL (LLM error)   : {raw_doc_type:<20} | {file_name} -> {err}")
                continue

            # 5. POST new document record with populated extracted_fields
            payload = {
                "document_type": raw_doc_type,
                "file_name": file_name,
                "file_path": str(file_path.resolve()),
                "extracted_fields": fields_dict,
            }

            batch_processed_this_run += 1

            try:
                post_res = requests.post(
                    f"{API_BASE_URL}/bidders/{bidder_id}/documents",
                    json=payload,
                    timeout=15,
                )
                if post_res.status_code == 201:
                    new_doc = post_res.json()
                    successful_count += 1
                    total_cost_this_run += COST_PER_DOC
                    preview = ", ".join(f"{k}={v}" for k, v in list(fields_dict.items())[:2])
                    # (3) Running count and cost after each success
                    print(
                        f"  [{doc_counter:3d}/{total_docs:3d}] SUCCESS (Doc ID {new_doc.get('id')}): "
                        f"{raw_doc_type:<20} | {len(fields_dict)} fields ({preview}...) "
                        f"[run: {successful_count} done, ~${total_cost_this_run:.4f}]"
                    )
                else:
                    failed_other_count += 1
                    err = f"HTTP {post_res.status_code}: {post_res.text}"
                    failures.append((f"{legal_name} - {file_name}", err))
                    print(f"  [{doc_counter:3d}/{total_docs:3d}] FAIL (API error)   : {raw_doc_type:<20} | {file_name} -> {err}")
            except Exception as ex:
                failed_other_count += 1
                err = f"API request error: {ex}"
                failures.append((f"{legal_name} - {file_name}", err))
                print(f"  [{doc_counter:3d}/{total_docs:3d}] FAIL (API request) : {raw_doc_type:<20} | {file_name} -> {err}")

    # (4) Print enriched summary at the end
    # Count how many eligible documents are still unprocessed overall
    remaining_overall = sum(
        1
        for b2 in bidders
        for dt in {d2["document_type"] for d2 in b2.get("documents", []) if DOCUMENT_TYPE_MAP.get(d2["document_type"]) in EXPECTED_FIELDS}
        if not any(
            d2.get("document_type") == dt
            and d2.get("extracted_fields")
            and isinstance(d2["extracted_fields"], dict)
            and len(d2["extracted_fields"]) > 0
            for d2 in b2.get("documents", [])
        )
    ) - successful_count  # subtract what we just processed
    remaining_overall = max(0, remaining_overall)

    print("\n" + "=" * 80)
    print("                     DOCUMENT SEEDING SUMMARY")
    print("=" * 80)
    print(f"  Total Document Records (DB)   : {total_docs}")
    print(f"  Already Done (skipped)        : {skipped_already_done_count}")
    print(f"  Skipped (Missing Schema)      : {skipped_no_schema_count}")
    print(f"  Processed This Run            : {batch_processed_this_run}")
    print(f"    of which Succeeded          : {successful_count}")
    print(f"    of which Failed             : {failed_other_count}")
    print(f"  Estimated Cost This Run       : ~${total_cost_this_run:.4f} USD")
    print(f"  Still Unprocessed Overall     : {remaining_overall} documents")
    print("=" * 80)

    if skipped_doc_types:
        print("\nDocument types with NO schema in prompts.py (candidate for addition):")
        for st in sorted(skipped_doc_types):
            print(f"  * {st}")

    if failures:
        print("\nOther Failures:")
        for item, err in failures:
            print(f"  * {item}: {err}")

    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
