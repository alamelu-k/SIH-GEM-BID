from dataclasses import dataclass

from common.enums import VerificationSourceType
from common.logging_config import get_logger
from common.schemas import EvidenceReference, TenderRequirement
from common.text_utils import normalize_whitespace

from document_ai.ocr.pdf_text_extractor import PageText

logger = get_logger(__name__)


@dataclass
class VerifiedRequirement:
    requirement: TenderRequirement
    evidence: EvidenceReference
    citation_verified: bool  # True if source_clause_text was found in the tender's actual text


def _clause_found_on_page(clause_text: str, page_text: str) -> bool:
    
    needle = normalize_whitespace(clause_text).upper()
    haystack = normalize_whitespace(page_text).upper()
    return needle in haystack


def verify_and_map_evidence(
    requirements: list[TenderRequirement],
    tender_pages: list[PageText],
    tender_id: str,
) -> list[VerifiedRequirement]:
    
    pages_by_number = {p.page_number: p.text for p in tender_pages}
    full_text_by_page = {p.page_number: p.text for p in tender_pages}
    all_text_joined = "\n".join(p.text for p in tender_pages)

    results: list[VerifiedRequirement] = []

    for req in requirements:
        verified = False

        if req.source_page is not None and req.source_page in pages_by_number:
            verified = _clause_found_on_page(req.source_clause_text, pages_by_number[req.source_page])

        if not verified:
            # Cited page didn't match — check the whole document before
            # giving up, and correct the page number if found elsewhere.
            for page_num, text in full_text_by_page.items():
                if _clause_found_on_page(req.source_clause_text, text):
                    verified = True
                    if req.source_page != page_num:
                        logger.info(
                            "Requirement %s: correcting source_page %s -> %s after verification",
                            req.requirement_id, req.source_page, page_num,
                        )
                        req.source_page = page_num
                    break

        if not verified:
            logger.warning(
                "Requirement %s: cited clause NOT found in tender %s text — possible hallucination, flag for manual review",
                req.requirement_id, tender_id,
            )

        evidence = EvidenceReference(
            document_id=tender_id,
            page_number=req.source_page,
            clause_text=req.source_clause_text,
            source_type=VerificationSourceType.SYNTHETIC,  # override at call site for real tenders
            source_name="Tender clause extraction",
        )

        results.append(VerifiedRequirement(requirement=req, evidence=evidence, citation_verified=verified))

    unverified_count = sum(1 for r in results if not r.citation_verified)
    if unverified_count:
        logger.warning("%d/%d requirements have unverified citations for tender %s", unverified_count, len(results), tender_id)

    return results


def filter_verified_only(verified_requirements: list[VerifiedRequirement]) -> list[TenderRequirement]:
    return [vr.requirement for vr in verified_requirements if vr.citation_verified]
