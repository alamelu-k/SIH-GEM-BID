import re
from dataclasses import dataclass

from common.logging_config import get_logger

logger = get_logger(__name__)

# Indian numbering units -> multiplier
_UNIT_MULTIPLIERS = {
    "lakh": 100_000,
    "lakhs": 100_000,
    "crore": 10_000_000,
    "crores": 10_000_000,
}

_OPERATOR_PATTERNS = [
    (re.compile(r"\b(at least|minimum|not less than|>=)\b", re.IGNORECASE), ">="),
    (re.compile(r"\b(at most|maximum|not more than|<=)\b", re.IGNORECASE), "<="),
    (re.compile(r"\b(more than|greater than|>)\b", re.IGNORECASE), ">"),
    (re.compile(r"\b(less than|fewer than|<)\b", re.IGNORECASE), "<"),
    (re.compile(r"\b(exactly|equal to|=)\b", re.IGNORECASE), "="),
]

_NUMBER_UNIT_PATTERN = re.compile(
    r"(?:rs\.?|inr|₹)?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lakhs|crore|crores)?",
    re.IGNORECASE,
)

_YEARS_PATTERN = re.compile(r"([\d]+)\s*(?:\+)?\s*years?", re.IGNORECASE)
_PERCENT_PATTERN = re.compile(r"([\d]+(?:\.\d+)?)\s*%")


@dataclass
class StructuredThreshold:
    operator: str | None  # ">=", "<=", ">", "<", "=", or None if undetermined
    value: float | None
    unit: str | None  # "INR", "years", "percent", or None
    raw_text: str
    parse_confidence: str  # "high" | "low" | "unparsed"


def _detect_operator(text: str) -> str | None:
    for pattern, operator in _OPERATOR_PATTERNS:
        if pattern.search(text):
            return operator
    return None


def _extract_currency_value(text: str) -> float | None:
    match = _NUMBER_UNIT_PATTERN.search(text)
    if not match or not match.group(1):
        return None
    number_str = match.group(1).replace(",", "")
    try:
        number = float(number_str)
    except ValueError:
        return None
    unit_word = (match.group(2) or "").lower()
    multiplier = _UNIT_MULTIPLIERS.get(unit_word, 1)
    return number * multiplier


def parse_threshold(raw_text: str | None) -> StructuredThreshold:
    
    if not raw_text or not raw_text.strip():
        return StructuredThreshold(operator=None, value=None, unit=None, raw_text="", parse_confidence="unparsed")

    text = raw_text.strip()
    operator = _detect_operator(text)

    years_match = _YEARS_PATTERN.search(text)
    if years_match:
        return StructuredThreshold(
            operator=operator or ">=",
            value=float(years_match.group(1)),
            unit="years",
            raw_text=raw_text,
            parse_confidence="high",
        )

    percent_match = _PERCENT_PATTERN.search(text)
    if percent_match:
        return StructuredThreshold(
            operator=operator or ">=",
            value=float(percent_match.group(1)),
            unit="percent",
            raw_text=raw_text,
            parse_confidence="high",
        )

    currency_value = _extract_currency_value(text)
    if currency_value is not None:
        return StructuredThreshold(
            operator=operator or ">=",
            value=currency_value,
            unit="INR",
            raw_text=raw_text,
            parse_confidence="high" if operator else "low",
        )

    logger.warning("Could not parse threshold text: '%s' — routing as unparsed", raw_text)
    return StructuredThreshold(operator=None, value=None, unit=None, raw_text=raw_text, parse_confidence="unparsed")


def parse_thresholds_batch(threshold_texts: list[str | None]) -> list[StructuredThreshold]:
    return [parse_threshold(t) for t in threshold_texts]
