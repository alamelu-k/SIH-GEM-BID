import json

from anthropic import Anthropic  # type: ignore[import-not-found]

from common.enums import DocumentType, VerificationSourceType
from common.exceptions import ExtractionError
from common.logging_config import get_logger
from common.schemas import EvidenceReference, ExtractedField

from .prompts import EXPECTED_FIELDS, build_extraction_prompt

logger = get_logger(__name__)

_client = Anthropic()


def _strip_markdown_fences(text: str) -> str:
    
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0]
    return text.strip()


def extract_fields(
    document_type: DocumentType,
    ocr_text: str,
    document_id: str | None = None,
    ocr_confidence: float | None = None,
) -> list[ExtractedField]:
   
    expected = EXPECTED_FIELDS.get(document_type)
    if expected is None:
        raise ExtractionError(f"No extraction schema defined for document type: {document_type}")

    prompt = build_extraction_prompt(document_type, ocr_text)

    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text

    try:
        parsed = json.loads(_strip_markdown_fences(raw))
    except json.JSONDecodeError as exc:
        raise ExtractionError(
            f"LLM did not return valid JSON for document {document_id}: {exc}"
        ) from exc

    if not isinstance(parsed, dict):
        raise ExtractionError(f"Expected a JSON object, got {type(parsed).__name__}")

    missing_keys = set(expected) - set(parsed.keys())
    if missing_keys:
        logger.warning("Extraction response missing expected keys: %s", missing_keys)

    evidence = EvidenceReference(
        document_id=document_id,
        source_type=VerificationSourceType.SYNTHETIC,  # override at call site for real docs
        source_name="Claude field extraction",
    )

    fields: list[ExtractedField] = []
    for field_name in expected:
        value = parsed.get(field_name)
        if value is None:
            continue  # field genuinely absent from the document — not an extraction failure
        fields.append(
            ExtractedField(
                field_name=field_name,
                value=str(value),
                confidence=ocr_confidence,
                evidence=evidence,
            )
        )

    return fields


def extract_fields_as_dict(
    document_type: DocumentType, ocr_text: str, document_id: str | None = None
) -> dict[str, str]:
    fields = extract_fields(document_type, ocr_text, document_id=document_id)
    return {f.field_name: f.value for f in fields}
