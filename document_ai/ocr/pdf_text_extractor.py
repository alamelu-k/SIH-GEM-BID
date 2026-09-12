from dataclasses import dataclass
from pathlib import Path

import fitz  # PyMuPDF  # type: ignore[import-not-found]
import pdfplumber  # type: ignore[import-not-found]

from common.logging_config import get_logger
from common.text_utils import normalize_unicode, normalize_whitespace

logger = get_logger(__name__)


@dataclass
class PageText:
    page_number: int  # 1-indexed
    text: str


def extract_text_pdfplumber(pdf_path: str | Path) -> list[PageText]:
    
    pages: list[PageText] = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            raw = page.extract_text() or ""
            pages.append(PageText(page_number=i, text=normalize_whitespace(normalize_unicode(raw))))
    return pages


def extract_text_pymupdf(pdf_path: str | Path) -> list[PageText]:
    
    pages: list[PageText] = []
    doc = fitz.open(str(pdf_path))
    try:
        for i, page in enumerate(doc, start=1):
            raw = page.get_text() or ""
            pages.append(PageText(page_number=i, text=normalize_whitespace(normalize_unicode(raw))))
    finally:
        doc.close()
    return pages


def extract_text(pdf_path: str | Path) -> list[PageText]:
    
    pdf_path = Path(pdf_path)
    primary = extract_text_pdfplumber(pdf_path)

    empty_pages = [p.page_number for p in primary if len(p.text) < 10]
    if not empty_pages:
        return primary

    logger.info("Falling back to PyMuPDF for %d empty-looking page(s)", len(empty_pages))
    backup = {p.page_number: p for p in extract_text_pymupdf(pdf_path)}

    merged = [
        backup[p.page_number] if p.page_number in empty_pages and p.page_number in backup else p
        for p in primary
    ]
    return merged


def full_text(pdf_path: str | Path) -> str:
    
    pages = extract_text(pdf_path)
    return "\n\n".join(f"[Page {p.page_number}]\n{p.text}" for p in pages)
