"""
common/text_utils.py

OCR-output cleanup and text-normalization helpers used before
extraction, comparison, or fuzzy matching. OCR output is noisy —
these functions absorb the most common, predictable errors so
downstream modules work with cleaner text.
"""

import re
import unicodedata

# Common OCR misreads for characters relevant to Indian ID documents
# (digits/letters that look alike in scanned/printed text).
_OCR_CHAR_FIXES = {
    "O": "0",  # only applied in digit-expected contexts, see fix_ocr_digits
    "I": "1",
    "l": "1",
    "S": "5",
    "B": "8",
}


def normalize_whitespace(text: str) -> str:
    """Collapse repeated whitespace/newlines from OCR output into
    single spaces, and strip leading/trailing whitespace."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def normalize_unicode(text: str) -> str:
    """Normalize unicode form (handles OCR engines that emit
    decomposed characters) and strip non-printable characters."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    return "".join(ch for ch in text if ch.isprintable() or ch.isspace())


def normalize_company_name(name: str) -> str:
    """Standardize a company name for comparison purposes: uppercase,
    whitespace-collapsed, common suffix punctuation normalized.
    Used before exact-match comparison; fuzzy_match.py handles the
    approximate-match case."""
    if not name:
        return ""
    name = normalize_whitespace(normalize_unicode(name)).upper()
    name = re.sub(r"[.,]", "", name)
    # Standardize common suffix variants
    name = re.sub(r"\bPVT\.?\s*LTD\.?\b", "PRIVATE LIMITED", name)
    name = re.sub(r"\bLTD\.?\b", "LIMITED", name)
    return normalize_whitespace(name)


def fix_ocr_digit_string(raw: str) -> str:
    """Apply common letter-for-digit OCR misread fixes to a string
    that is EXPECTED to be all-digits (e.g. a phone number or a
    digit-only ID segment). Do not apply to free text — this is
    intentionally narrow to avoid corrupting real alphabetic content."""
    fixed = raw
    for wrong, right in _OCR_CHAR_FIXES.items():
        fixed = fixed.replace(wrong, right)
    return fixed


def extract_digits(text: str) -> str:
    """Strip everything except digits — useful for pulling a clean
    numeric value (e.g. turnover figure) out of noisy OCR text."""
    return re.sub(r"\D", "", text or "")
