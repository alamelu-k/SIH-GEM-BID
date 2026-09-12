import hashlib

from common.enums import RequirementType
from common.logging_config import get_logger
from common.schemas import TenderRequirement

logger = get_logger(__name__)


def _generate_requirement_id(tender_id: str, clause_text: str, index: int) -> str:
    
    digest = hashlib.sha1(f"{tender_id}:{clause_text}".encode("utf-8")).hexdigest()[:8]
    return f"REQ-{tender_id}-{index:03d}-{digest}"


def _parse_requirement_type(raw_type: str) -> RequirementType:
    try:
        return RequirementType(raw_type.strip().lower())
    except ValueError:
        logger.warning("Unrecognized requirement type '%s'; defaulting to OTHER", raw_type)
        return RequirementType.OTHER


def parse_raw_clauses(raw_clauses: list[dict], tender_id: str) -> list[TenderRequirement]:
    
    requirements: list[TenderRequirement] = []

    for i, raw in enumerate(raw_clauses, start=1):
        clause_text = raw.get("source_clause_text")
        if not clause_text or not clause_text.strip():
            logger.warning("Skipping requirement %d for tender %s: missing source_clause_text", i, tender_id)
            continue

        requirement = TenderRequirement(
            requirement_id=_generate_requirement_id(tender_id, clause_text, i),
            type=_parse_requirement_type(raw.get("type", "other")),
            mandatory=bool(raw.get("mandatory", False)),
            threshold_value=raw.get("threshold_value"),
            source_clause_text=clause_text.strip(),
            source_page=raw.get("source_page"),
        )
        requirements.append(requirement)

    logger.info("Parsed %d/%d raw clauses into valid requirements for tender %s", len(requirements), len(raw_clauses), tender_id)
    return requirements


def deduplicate_requirements(requirements: list[TenderRequirement]) -> list[TenderRequirement]:
    
    seen: set[tuple[RequirementType, str]] = set()
    deduped: list[TenderRequirement] = []

    for req in requirements:
        key = (req.type, req.source_clause_text)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(req)

    return deduped
