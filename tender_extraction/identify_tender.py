import json
import os
import sys
from pathlib import Path

# Attempt to import extract_text from sadhana-ml/document_ai/ocr/pdf_text_extractor.py
try:
    sadhana_ml_path = Path(__file__).resolve().parent.parent / "sadhana-ml"
    if sadhana_ml_path.exists() and str(sadhana_ml_path) not in sys.path:
        sys.path.insert(0, str(sadhana_ml_path))
    from document_ai.ocr.pdf_text_extractor import extract_text
except Exception:
    # Ported from sadhana-ml/document_ai/ocr/pdf_text_extractor.py:
    # Dual-engine extractor using pdfplumber primary with PyMuPDF fallback
    import fitz  # PyMuPDF
    import pdfplumber

    def _normalize_text(text: str) -> str:
        return " ".join(text.split())

    def extract_text(pdf_path: str | Path):
        class PageText:
            def __init__(self, page_number: int, text: str):
                self.page_number = page_number
                self.text = text

        pdf_path = Path(pdf_path)
        primary = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                raw = page.extract_text() or ""
                primary.append(PageText(page_number=i, text=_normalize_text(raw)))

        empty_pages = [p.page_number for p in primary if len(p.text) < 10]
        if not empty_pages:
            return primary

        # PyMuPDF fallback
        doc = fitz.open(str(pdf_path))
        backup = {}
        try:
            for i, page in enumerate(doc, start=1):
                raw = page.get_text() or ""
                backup[i] = PageText(page_number=i, text=_normalize_text(raw))
        finally:
            doc.close()

        merged = [
            backup[p.page_number] if p.page_number in empty_pages and p.page_number in backup else p
            for p in primary
        ]
        return merged


def load_tenders_lookup() -> dict:
    """Load tenders.json keyed by tender_number."""
    script_dir = Path(__file__).resolve().parent
    candidates = [
        script_dir / "tenders.json",
        script_dir.parent / "tender_extraction" / "tenders.json",
        script_dir.parent / "integration" / "tender_extraction" / "tenders.json",
        Path("tenders.json"),
        Path("tender_extraction/tenders.json"),
    ]
    for p in candidates:
        if p.is_file():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    raise FileNotFoundError("Could not locate tenders.json")


def identify_and_extract(pdf_path: str) -> dict:
    """
    Identifies the tender from a PDF document and extracts its requirements.
    
    1. Extracts text from the PDF using pdfplumber/PyMuPDF.
    2. Searches extracted text for known tender_number strings from tenders.json.
    3. If exactly one matches, returns:
       {
           "tender_number": "...",
           "identified": True,
           "requirements": [ ...full requirement list... ]
       }
    4. If zero or more than one match, returns:
       {
           "identified": False,
           "reason": "..."
       }
    """
    path = Path(pdf_path)
    if not path.is_file():
        return {
            "identified": False,
            "reason": f"File does not exist: {pdf_path}",
        }

    # 1. Extract text from PDF
    try:
        pages = extract_text(path)
        full_text = "\n".join(page.text for page in pages)
    except Exception as exc:
        return {
            "identified": False,
            "reason": f"PDF extraction failed for {pdf_path}: {exc}",
        }

    # 2. Load known tenders
    tenders = load_tenders_lookup()

    # 3. Exact substring match for known tender numbers
    matched_tenders = [
        tender_num for tender_num in tenders.keys()
        if tender_num in full_text
    ]

    # 4. Check matches
    if len(matched_tenders) == 1:
        matched_num = matched_tenders[0]
        tender_data = tenders[matched_num]
        return {
            "tender_number": matched_num,
            "identified": True,
            "requirements": tender_data.get("requirements", []),
        }
    elif len(matched_tenders) == 0:
        return {
            "identified": False,
            "reason": f"No known tender number found in {path.name}. Checked candidates: {list(tenders.keys())}",
        }
    else:
        return {
            "identified": False,
            "reason": f"Ambiguous match: multiple tender numbers found in {path.name}: {matched_tenders}",
        }
