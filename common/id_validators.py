"""
common/id_validators.py

Validation FUNCTIONS for GSTIN/PAN/Udyam shape checks. The regex
PATTERNS themselves live in config/thresholds.py (single source of
truth); this module just wraps them in reusable, testable functions.

These checks are purely offline/local — no API call, no internet
required. They confirm a value is SHAPED correctly, not that it's
currently active/valid in a government database (that's the
verification connectors' job, in the main backend).
"""

import re

from config.thresholds import GSTIN_PATTERN, PAN_PATTERN, UDYAM_PATTERN


def is_valid_gstin(value: str) -> bool:
    """Check a GSTIN matches the 15-character structural pattern.
    Does NOT confirm the GSTIN is currently active — format only."""
    if not value:
        return False
    return bool(re.match(GSTIN_PATTERN, value.strip().upper()))


def is_valid_pan(value: str) -> bool:
    """Check a PAN matches the 10-character structural pattern."""
    if not value:
        return False
    return bool(re.match(PAN_PATTERN, value.strip().upper()))


def is_valid_udyam(value: str) -> bool:
    """Check a Udyam registration number matches the
    UDYAM-XX-00-0000000 structural pattern."""
    if not value:
        return False
    return bool(re.match(UDYAM_PATTERN, value.strip().upper()))


def extract_pan_from_gstin(gstin: str) -> str | None:
    """A valid GSTIN embeds the holder's PAN as characters 3-12.
    Useful for cross-checking a bidder's separately-submitted PAN
    document against the PAN implied by their GSTIN."""
    if not is_valid_gstin(gstin):
        return None
    return gstin[2:12]


def validate_bidder_id_bundle(
    gstin: str | None, pan: str | None, udyam: str | None
) -> dict[str, bool]:
    """Run all applicable format checks on a bidder's ID set in one
    call, plus a cross-consistency check between GSTIN and PAN when
    both are present."""
    results: dict[str, bool] = {}

    if gstin is not None:
        results["gstin_format_valid"] = is_valid_gstin(gstin)
    if pan is not None:
        results["pan_format_valid"] = is_valid_pan(pan)
    if udyam is not None:
        results["udyam_format_valid"] = is_valid_udyam(udyam)

    if gstin and pan and results.get("gstin_format_valid") and results.get("pan_format_valid"):
        embedded_pan = extract_pan_from_gstin(gstin)
        results["gstin_pan_consistent"] = embedded_pan == pan.strip().upper()

    return results
