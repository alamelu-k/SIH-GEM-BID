"""
common/fuzzy_match.py

Thin, single wrapper around RapidFuzz so every module that needs
name/address similarity comparison calls the same tuned function
instead of each reimplementing its own RapidFuzz call with different
settings. Used by:
  - document_ai/validation: name consistency across one bidder's own
    documents (e.g. does the GST cert name match the PAN card name?)
  - graph_intelligence/relationship_detection: shared-director/address
    matching ACROSS different bidders (collusion signal)
"""

from difflib import SequenceMatcher

try:
    from rapidfuzz import fuzz  # type: ignore[import-not-found]
except ImportError:
    class _FallbackFuzz:
        @staticmethod
        def token_sort_ratio(a: str, b: str) -> float:
            if not a or not b:
                return 0.0
            a_tokens = sorted(a.split())
            b_tokens = sorted(b.split())
            return SequenceMatcher(None, " ".join(a_tokens), " ".join(b_tokens)).ratio() * 100.0

        @staticmethod
        def partial_ratio(a: str, b: str) -> float:
            if not a or not b:
                return 0.0
            return SequenceMatcher(None, a, b).ratio() * 100.0

    fuzz = _FallbackFuzz()

from .text_utils import normalize_company_name

# Default similarity threshold (0-100 scale) above which two strings
# are considered a likely match. Kept here rather than in
# config/thresholds.py since it's a matching-sensitivity setting, not
# a risk/compliance decision threshold — tune independently.
DEFAULT_NAME_MATCH_THRESHOLD = 85.0


def name_similarity(name_a: str, name_b: str) -> float:
    """Return a 0-100 similarity score between two company names,
    after normalizing common suffix/formatting variance
    (Pvt Ltd vs Private Limited, punctuation, whitespace)."""
    if not name_a or not name_b:
        return 0.0
    a = normalize_company_name(name_a)
    b = normalize_company_name(name_b)
    return fuzz.token_sort_ratio(a, b)


def is_likely_same_name(
    name_a: str, name_b: str, threshold: float = DEFAULT_NAME_MATCH_THRESHOLD
) -> bool:
    """True if two names are similar enough to likely refer to the
    same entity — catches near-duplicates like 'ABC Safety Pvt Ltd'
    vs 'ABC Safety Industries Pvt Ltd' that exact string comparison
    would miss."""
    return name_similarity(name_a, name_b) >= threshold


def address_similarity(address_a: str, address_b: str) -> float:
    """Similarity score for free-text addresses. Uses partial_ratio
    since addresses often differ in formatting/ordering but share a
    core substring (same building/street)."""
    if not address_a or not address_b:
        return 0.0
    return fuzz.partial_ratio(address_a.strip().upper(), address_b.strip().upper())


def best_match(query: str, candidates: list[str]) -> tuple[str | None, float]:
    """Return the (candidate, score) pair with the highest similarity
    to query. Useful for matching an extracted name against a known
    debarment/blacklist name list."""
    if not candidates:
        return None, 0.0
    scored = [(c, name_similarity(query, c)) for c in candidates]
    return max(scored, key=lambda pair: pair[1])
