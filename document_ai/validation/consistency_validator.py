from dataclasses import dataclass, field

from common.fuzzy_match import DEFAULT_NAME_MATCH_THRESHOLD, is_likely_same_name
from common.id_validators import validate_bidder_id_bundle
from common.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class ConsistencyIssue:
    field_name: str
    issue_type: str  # "invalid_format" | "cross_document_mismatch"
    detail: str


@dataclass
class ConsistencyReport:
    bidder_id: str
    issues: list[ConsistencyIssue] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        return len(self.issues) == 0


def validate_id_formats(bidder_id: str, gstin: str | None, pan: str | None, udyam: str | None) -> ConsistencyReport:
    
    report = ConsistencyReport(bidder_id=bidder_id)
    results = validate_bidder_id_bundle(gstin, pan, udyam)

    for key, is_valid in results.items():
        if key == "gstin_pan_consistent" and not is_valid:
            report.issues.append(
                ConsistencyIssue(
                    field_name="gstin/pan",
                    issue_type="cross_document_mismatch",
                    detail="PAN embedded in GSTIN does not match submitted PAN",
                )
            )
        elif key.endswith("_format_valid") and not is_valid:
            id_type = key.replace("_format_valid", "")
            report.issues.append(
                ConsistencyIssue(
                    field_name=id_type,
                    issue_type="invalid_format",
                    detail=f"{id_type.upper()} does not match expected format",
                )
            )

    return report


def validate_name_consistency(
    bidder_id: str,
    document_names: dict[str, str],
    threshold: float = DEFAULT_NAME_MATCH_THRESHOLD,
) -> ConsistencyReport:
    
    report = ConsistencyReport(bidder_id=bidder_id)
    entries = list(document_names.items())

    for i in range(len(entries)):
        for j in range(i + 1, len(entries)):
            doc_a, name_a = entries[i]
            doc_b, name_b = entries[j]
            if not is_likely_same_name(name_a, name_b, threshold=threshold):
                report.issues.append(
                    ConsistencyIssue(
                        field_name="legal_name",
                        issue_type="cross_document_mismatch",
                        detail=f"Name on {doc_a} ('{name_a}') does not match name on {doc_b} ('{name_b}')",
                    )
                )

    return report


def full_consistency_check(
    bidder_id: str,
    gstin: str | None,
    pan: str | None,
    udyam: str | None,
    document_names: dict[str, str],
) -> ConsistencyReport:
    
    format_report = validate_id_formats(bidder_id, gstin, pan, udyam)
    name_report = validate_name_consistency(bidder_id, document_names)

    return ConsistencyReport(
        bidder_id=bidder_id,
        issues=format_report.issues + name_report.issues,
    )
