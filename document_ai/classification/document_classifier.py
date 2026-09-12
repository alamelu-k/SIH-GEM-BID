import re

from anthropic import Anthropic  # type: ignore[import-not-found]

from common.enums import DocumentType
from common.exceptions import DocumentClassificationError
from common.logging_config import get_logger
from common.schemas import DocumentClassificationResult

logger = get_logger(__name__)

_client = Anthropic()


_KEYWORD_SIGNALS: dict[DocumentType, list[str]] = {
    DocumentType.GST_CERTIFICATE: ["GOODS AND SERVICES TAX", "GSTIN", "CERTIFICATE OF REGISTRATION"],
    DocumentType.PAN_CARD: ["PERMANENT ACCOUNT NUMBER", "INCOME TAX DEPARTMENT"],
    DocumentType.UDYAM_CERTIFICATE: ["UDYAM REGISTRATION", "MINISTRY OF MICRO, SMALL AND MEDIUM"],
    DocumentType.TURNOVER_STATEMENT: ["TURNOVER", "ANNUAL TURNOVER", "CHARTERED ACCOUNTANT"],
    DocumentType.OEM_AUTHORIZATION_LETTER: ["AUTHORIZATION LETTER", "ORIGINAL EQUIPMENT MANUFACTURER", "OEM"],
    DocumentType.EPFO_ESIC_CERTIFICATE: ["EMPLOYEES' PROVIDENT FUND", "EPFO", "ESIC"],
    DocumentType.STARTUP_INDIA_CERTIFICATE: ["STARTUP INDIA", "DPIIT"],
    DocumentType.NSIC_CERTIFICATE: ["NATIONAL SMALL INDUSTRIES CORPORATION", "NSIC"],
}

_LLM_FALLBACK_PROMPT = """You are classifying a scanned Indian government/business \
document by type. Based on the text below, respond with EXACTLY ONE of these \
labels and nothing else: {labels}

Document text:
---
{text}
---

Label:"""


def _keyword_classify(text: str) -> tuple[DocumentType | None, float]:
    
    upper = text.upper()
    scores: dict[DocumentType, int] = {}
    for doc_type, keywords in _KEYWORD_SIGNALS.items():
        hits = sum(1 for kw in keywords if kw in upper)
        if hits:
            scores[doc_type] = hits

    if not scores:
        return None, 0.0

    best_type = max(scores, key=lambda t: scores[t])
    max_possible = len(_KEYWORD_SIGNALS[best_type])
    confidence = scores[best_type] / max_possible
    return best_type, confidence


def _llm_classify(text: str) -> DocumentClassificationResult:
    
    labels = [t.value for t in DocumentType if t != DocumentType.UNKNOWN]
    prompt = _LLM_FALLBACK_PROMPT.format(labels=", ".join(labels), text=text[:3000])

    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=20,
        messages=[{"role": "user", "content": prompt}],
    )
    label = response.content[0].text.strip().lower()

    try:
        doc_type = DocumentType(label)
    except ValueError:
        logger.warning("LLM returned unrecognized label '%s'; marking UNKNOWN", label)
        doc_type = DocumentType.UNKNOWN

    
    confidence = 0.65 if doc_type != DocumentType.UNKNOWN else 0.0
    return DocumentClassificationResult(document_type=doc_type, confidence=confidence)


_KEYWORD_CONFIDENCE_FLOOR = 0.34


def classify_document(text: str) -> DocumentClassificationResult:
    
    if not text or not text.strip():
        raise DocumentClassificationError("Cannot classify empty document text")

    doc_type, confidence = _keyword_classify(text)
    if doc_type is not None and confidence >= _KEYWORD_CONFIDENCE_FLOOR:
        return DocumentClassificationResult(document_type=doc_type, confidence=confidence)

    logger.info("Keyword classification inconclusive (best confidence %.2f); falling back to LLM", confidence)
    return _llm_classify(text)
