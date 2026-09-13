from common.enums import DocumentType


EXPECTED_FIELDS: dict[DocumentType, list[str]] = {
    DocumentType.GST_CERTIFICATE: ["legal_name", "gstin", "registration_date", "business_address"],
    DocumentType.PAN_CARD: ["legal_name", "pan", "date_of_incorporation_or_birth"],
    DocumentType.UDYAM_CERTIFICATE: ["legal_name", "udyam_number", "enterprise_category", "registration_date"],
    DocumentType.TURNOVER_STATEMENT: ["legal_name", "turnover_amount", "financial_year"],
    DocumentType.OEM_AUTHORIZATION_LETTER: ["oem_name", "authorized_dealer_name", "product_category", "validity_date"],
    DocumentType.EPFO_ESIC_CERTIFICATE: ["legal_name", "establishment_code", "registration_date"],
    DocumentType.STARTUP_INDIA_CERTIFICATE: ["legal_name", "dpiit_number", "recognition_date"],
    DocumentType.NSIC_CERTIFICATE: ["legal_name", "nsic_registration_number", "validity_date"],
    DocumentType.BIS_LICENSE: ["legal_name", "bis_license_number", "product_category", "valid_from", "valid_to", "status"],
}

_BASE_INSTRUCTIONS = """You are extracting structured fields from an Indian \
government/business document. Return ONLY a valid JSON object — no prose, \
no markdown fences, no explanation.

Rules:
- If a field is not present in the text, use null for its value.
- Do not invent, guess, or infer any value not explicitly present in the text.
- Preserve values exactly as written (do not reformat dates, numbers, or names).
- Output must be a flat JSON object with exactly these keys: {fields}
"""


def build_extraction_prompt(document_type: DocumentType, ocr_text: str) -> str:
    fields = EXPECTED_FIELDS.get(document_type)
    if fields is None:
        raise ValueError(f"No field schema defined for document type: {document_type}")

    instructions = _BASE_INSTRUCTIONS.format(fields=", ".join(fields))
    return f"""{instructions}

Document text:
---
{ocr_text}
---

JSON:"""


_CLAUSE_EXTRACTION_INSTRUCTIONS = """You are extracting bidder eligibility \
requirements from a government tender document. Return ONLY a valid JSON \
array — no prose, no markdown fences.

Each array item must be an object with exactly these keys:
- "type": one of {requirement_types}
- "mandatory": true or false
- "threshold_value": the specific numeric/text threshold if the clause \
  states one (e.g. minimum turnover amount), else null
- "source_clause_text": the exact sentence(s) from the tender that state \
  this requirement (do not paraphrase)
- "source_page": the page number the clause appears on, if determinable, else null

Only extract requirements that are explicitly stated in the text. Do not \
infer requirements that are common in other tenders but not stated here.
"""


def build_clause_extraction_prompt(tender_text: str, requirement_types: list[str]) -> str:
    
    instructions = _CLAUSE_EXTRACTION_INSTRUCTIONS.format(
        requirement_types=", ".join(requirement_types)
    )
    return f"""{instructions}

Tender document text:
---
{tender_text}
---

JSON array:"""
