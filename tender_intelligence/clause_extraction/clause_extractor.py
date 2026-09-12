import json

from anthropic import Anthropic  # type: ignore[import-not-found]

from common.enums import RequirementType
from common.exceptions import ClauseExtractionError
from common.logging_config import get_logger


from document_ai.extraction.prompts import build_clause_extraction_prompt

logger = get_logger(__name__)

_client = Anthropic()


def _strip_markdown_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0]
    return text.strip()


def extract_raw_clauses(tender_text: str, tender_id: str | None = None) -> list[dict]:
    
    requirement_types = [t.value for t in RequirementType]
    prompt = build_clause_extraction_prompt(tender_text, requirement_types)

    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text

    try:
        parsed = json.loads(_strip_markdown_fences(raw))
    except json.JSONDecodeError as exc:
        raise ClauseExtractionError(
            f"LLM did not return valid JSON array for tender {tender_id}: {exc}"
        ) from exc

    if not isinstance(parsed, list):
        raise ClauseExtractionError(f"Expected a JSON array, got {type(parsed).__name__}")

    if not parsed:
        logger.warning("Clause extraction returned zero requirements for tender %s", tender_id)

    return parsed
