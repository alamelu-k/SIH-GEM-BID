from pathlib import Path

import pytest  # type: ignore[import-not-found]

from config.thresholds import (
    CLASSIFIER_PROBABILITY_THRESHOLD,
    CV_SUSPICIOUS_THRESHOLD,
    SKEWNESS_SUSPICIOUS_THRESHOLD,
    MIN_FIELD_EXTRACTION_ACCURACY,
    get_risk_level,
)

from common.enums import (
    DocumentType,
    RequirementType,
    VerificationSourceType,
)

from common.exceptions import (
    ExtractionError,
    LowConfidenceOCRError,
    InvalidIDFormatError,
    ClauseExtractionError,
    InsufficientDataError,
    ModelNotTrainedError,
    GraphConstructionError,
    AggregationError,
)

from document_ai.extraction.prompts import (
    EXPECTED_FIELDS,
    build_extraction_prompt,
    build_clause_extraction_prompt,
)

from document_ai.evaluation.accuracy_evaluator import (
    evaluate_extraction,
)

from document_ai.validation.consistency_validator import (
    validate_id_formats,
    validate_name_consistency,
    full_consistency_check,
)

from tender_intelligence.requirement_parser.requirement_parser import (
    parse_raw_clauses,
    deduplicate_requirements,
)

from tender_intelligence.threshold_extraction.threshold_extractor import (
    parse_threshold,
    parse_thresholds_batch,
)

from tender_intelligence.evidence_mapping.evidence_mapper import (
    verify_and_map_evidence,
    filter_verified_only,
)

from tender_intelligence.clause_extraction.clause_extractor import (
    _strip_markdown_fences,
)


def test_threshold_configuration():
    assert 0.0 < CLASSIFIER_PROBABILITY_THRESHOLD < 1.0
    assert 0.0 < CV_SUSPICIOUS_THRESHOLD < 1.0
    assert SKEWNESS_SUSPICIOUS_THRESHOLD > 0.0
    assert 0.0 < MIN_FIELD_EXTRACTION_ACCURACY <= 1.0


def test_risk_level_mapping():
    assert get_risk_level(0.10).value == "Low"
    assert get_risk_level(0.50).value == "Medium"
    assert get_risk_level(0.80).value == "High"


def test_document_types():
    assert DocumentType.GST_CERTIFICATE.value == "gst_certificate"
    assert DocumentType.PAN_CARD.value == "pan_card"
    assert DocumentType.UDYAM_CERTIFICATE.value == "udyam_certificate"
    assert DocumentType.TENDER_PDF.value == "tender_pdf"


def test_requirement_types():
    assert RequirementType.UDYAM_MSME.value == "udyam_msme"
    assert RequirementType.GST_REGISTRATION.value == "gst_registration"
    assert RequirementType.OEM_AUTHORIZATION.value == "oem_authorization"


def test_verification_source_types():
    assert VerificationSourceType.OFFICIAL.value == "official"
    assert VerificationSourceType.LICENSED_SANDBOX.value == "licensed_sandbox"
    assert VerificationSourceType.SYNTHETIC.value == "synthetic"


def test_parse_currency_threshold():

    result = parse_threshold(
        "Bidder must have a minimum annual turnover of ₹50 lakh."
    )

    assert result.operator == ">="
    assert result.value == 5_000_000
    assert result.unit == "INR"
    assert result.parse_confidence == "high"


def test_parse_crore_threshold():
    result = parse_threshold(
        "The bidder must have a turnover of at least 2 crore."
    )

    assert result.operator == ">="
    assert result.value == 20_000_000
    assert result.unit == "INR"


def test_parse_year_threshold():

    result = parse_threshold(
        "The bidder must have at least 5 years of experience."
    )

    assert result.operator == ">="
    assert result.value == 5
    assert result.unit == "years"


def test_parse_percentage_threshold():

    result = parse_threshold(
        "The bidder must have at least 20% local content."
    )

    assert result.operator == ">="
    assert result.value == 20
    assert result.unit == "percent"


def test_parse_unrecognized_threshold():
    result = parse_threshold(
        "The bidder must be registered with the appropriate authority."
    )

    assert result.value is None
    assert result.unit is None
    assert result.parse_confidence == "unparsed"


def test_parse_threshold_batch():
    texts = [
        "Minimum turnover of ₹50 lakh",
        "At least 3 years experience",
        "Minimum 15% local content",
    ]

    results = parse_thresholds_batch(texts)

    assert len(results) == 3

    assert results[0].unit == "INR"
    assert results[1].unit == "years"
    assert results[2].unit == "percent"


def test_parse_raw_clauses():
    raw_clauses = [
        {
            "type": "udyam_msme",
            "mandatory": True,
            "threshold_value": None,
            "source_clause_text": (
                "The bidder must possess a valid Udyam registration certificate."
            ),
            "source_page": 3,
        },
        {
            "type": "gst_registration",
            "mandatory": True,
            "threshold_value": None,
            "source_clause_text": (
                "The bidder must have a valid GST registration."
            ),
            "source_page": 4,
        },
    ]

    requirements = parse_raw_clauses(
        raw_clauses,
        tender_id="TEST-TENDER-001",
    )

    assert len(requirements) == 2

    assert requirements[0].type == RequirementType.UDYAM_MSME
    assert requirements[0].mandatory is True
    assert requirements[0].source_page == 3

    assert requirements[1].type == RequirementType.GST_REGISTRATION


def test_requirement_id_generation():
    raw_clauses = [
        {
            "type": "gst_registration",
            "mandatory": True,
            "source_clause_text": "Valid GST registration is mandatory.",
            "source_page": 2,
        }
    ]

    requirements = parse_raw_clauses(
        raw_clauses,
        tender_id="TEST-001",
    )

    assert len(requirements) == 1
    assert requirements[0].requirement_id.startswith("REQ-TEST-001-001-")


def test_invalid_requirement_type_defaults_to_other():
    raw_clauses = [
        {
            "type": "some_unknown_requirement",
            "mandatory": False,
            "source_clause_text": "Some unknown tender requirement.",
            "source_page": 1,
        }
    ]

    requirements = parse_raw_clauses(
        raw_clauses,
        tender_id="TEST-002",
    )

    assert len(requirements) == 1
    assert requirements[0].type == RequirementType.OTHER


def test_missing_clause_text_is_skipped():
    raw_clauses = [
        {
            "type": "gst_registration",
            "mandatory": True,
            "source_clause_text": "",
            "source_page": 1,
        },
        {
            "type": "pan_income_tax",
            "mandatory": True,
            "source_clause_text": "PAN is mandatory.",
            "source_page": 2,
        },
    ]

    requirements = parse_raw_clauses(
        raw_clauses,
        tender_id="TEST-003",
    )

    assert len(requirements) == 1
    assert requirements[0].type == RequirementType.PAN_INCOME_TAX


def test_deduplicate_requirements():
    raw_clauses = [
        {
            "type": "gst_registration",
            "mandatory": True,
            "source_clause_text": "Valid GST registration is mandatory.",
            "source_page": 2,
        },
        {
            "type": "gst_registration",
            "mandatory": True,
            "source_clause_text": "Valid GST registration is mandatory.",
            "source_page": 2,
        },
    ]

    requirements = parse_raw_clauses(
        raw_clauses,
        tender_id="TEST-004",
    )

    assert len(requirements) == 2

    deduped = deduplicate_requirements(requirements)

    assert len(deduped) == 1


def test_evidence_mapping():
    from document_ai.ocr.pdf_text_extractor import PageText

    raw_clauses = [
        {
            "type": "gst_registration",
            "mandatory": True,
            "threshold_value": None,
            "source_clause_text": "Valid GST registration is mandatory.",
            "source_page": 2,
        }
    ]

    requirements = parse_raw_clauses(
        raw_clauses,
        tender_id="TEST-TENDER-005",
    )

    tender_pages = [
        PageText(
            page_number=1,
            text="General tender information.",
        ),
        PageText(
            page_number=2,
            text=(
                "Eligibility Criteria:\n"
                "Valid GST registration is mandatory."
            ),
        ),
    ]

    verified = verify_and_map_evidence(
        requirements=requirements,
        tender_pages=tender_pages,
        tender_id="TEST-TENDER-005",
    )

    assert len(verified) == 1
    assert verified[0].citation_verified is True
    assert verified[0].evidence.document_id == "TEST-TENDER-005"


def test_unverified_evidence():
    from document_ai.ocr.pdf_text_extractor import PageText

    raw_clauses = [
        {
            "type": "gst_registration",
            "mandatory": True,
            "source_clause_text": "This clause does not exist.",
            "source_page": 1,
        }
    ]

    requirements = parse_raw_clauses(
        raw_clauses,
        tender_id="TEST-TENDER-006",
    )

    tender_pages = [
        PageText(
            page_number=1,
            text="Only unrelated tender content exists here.",
        )
    ]

    verified = verify_and_map_evidence(
        requirements=requirements,
        tender_pages=tender_pages,
        tender_id="TEST-TENDER-006",
    )

    assert len(verified) == 1
    assert verified[0].citation_verified is False

    verified_only = filter_verified_only(verified)

    assert len(verified_only) == 0


def test_valid_id_formats():
    report = validate_id_formats(
        bidder_id="BIDDER-001",
        gstin="29ABCDE1234F1Z5",
        pan="ABCDE1234F",
        udyam="UDYAM-TN-12-1234567",
    )

    assert report.is_clean is True
    assert len(report.issues) == 0


def test_invalid_id_format():
    report = validate_id_formats(
        bidder_id="BIDDER-002",
        gstin="INVALID-GSTIN",
        pan="INVALID-PAN",
        udyam="INVALID-UDYAM",
    )

    assert report.is_clean is False
    assert len(report.issues) > 0


def test_name_consistency():
    names = {
        "gst_certificate": "ABC Technologies Private Limited",
        "pan_card": "ABC Technologies Pvt Ltd",
    }

    report = validate_name_consistency(
        bidder_id="BIDDER-003",
        document_names=names,
    )

    assert report.is_clean is True


def test_name_mismatch():
    names = {
        "gst_certificate": "ABC Technologies Private Limited",
        "pan_card": "XYZ Engineering Corporation",
    }

    report = validate_name_consistency(
        bidder_id="BIDDER-004",
        document_names=names,
    )

    assert report.is_clean is False
    assert len(report.issues) > 0


def test_full_consistency_check():
    report = full_consistency_check(
        bidder_id="BIDDER-005",
        gstin="29ABCDE1234F1Z5",
        pan="ABCDE1234F",
        udyam="UDYAM-TN-12-1234567",
        document_names={
            "gst_certificate": "ABC Technologies Private Limited",
            "pan_card": "ABC Technologies Pvt Ltd",
        },
    )

    assert report.is_clean is True


def test_extraction_accuracy_perfect():
    """Perfect predictions should achieve 100% accuracy."""

    ground_truth = {
        "DOC-001": {
            "legal_name": "ABC Technologies Pvt Ltd",
            "gstin": "29ABCDE1234F1Z5",
            "pan": "ABCDE1234F",
        }
    }

    predictions = {
        "DOC-001": {
            "legal_name": "ABC Technologies Pvt Ltd",
            "gstin": "29ABCDE1234F1Z5",
            "pan": "ABCDE1234F",
        }
    }

    report = evaluate_extraction(
        predictions=predictions,
        ground_truth=ground_truth,
    )

    assert report.overall_accuracy == 1.0
    assert report.meets_target is True
    assert len(report.mismatches) == 0


def test_extraction_accuracy_with_mismatch():
    ground_truth = {
        "DOC-002": {
            "legal_name": "ABC Technologies Pvt Ltd",
            "gstin": "29ABCDE1234F1Z5",
        }
    }

    predictions = {
        "DOC-002": {
            "legal_name": "ABC Technologies Pvt Ltd",
            "gstin": "29ABCDE9999F1Z5",
        }
    }

    report = evaluate_extraction(
        predictions=predictions,
        ground_truth=ground_truth,
    )

    assert report.overall_accuracy == 0.5
    assert len(report.mismatches) == 1

    mismatch = report.mismatches[0]

    assert mismatch["field_name"] == "gstin"
    assert mismatch["expected"] == "29ABCDE1234F1Z5"
    assert mismatch["predicted"] == "29ABCDE9999F1Z5"


def test_extraction_missing_prediction():
    """Missing predicted fields should count as incorrect."""

    ground_truth = {
        "DOC-003": {
            "legal_name": "ABC Technologies Pvt Ltd",
            "gstin": "29ABCDE1234F1Z5",
        }
    }

    predictions = {
        "DOC-003": {
            "legal_name": "ABC Technologies Pvt Ltd",
        }
    }

    report = evaluate_extraction(
        predictions=predictions,
        ground_truth=ground_truth,
    )

    assert report.overall_accuracy == 0.5
    assert len(report.mismatches) == 1


def test_strip_markdown_fences():
    """Check removal of ```json fences from LLM output."""

    raw = """```json
[
    {
        "type": "gst_registration",
        "mandatory": true
    }
]
```"""

    cleaned = _strip_markdown_fences(raw)

    assert cleaned.startswith("[")
    assert cleaned.endswith("]")
    assert "```" not in cleaned


def test_document_extraction_prompt():
    prompt = build_extraction_prompt(
        DocumentType.GST_CERTIFICATE,
        "GSTIN: 29ABCDE1234F1Z5\nLegal Name: ABC Technologies Pvt Ltd",
    )

    assert isinstance(prompt, str)
    assert len(prompt) > 0
    assert "gstin" in prompt.lower()
    assert "legal_name" in prompt.lower()


def test_clause_extraction_prompt():
    requirement_types = [
        RequirementType.GST_REGISTRATION.value,
        RequirementType.UDYAM_MSME.value,
        RequirementType.PAN_INCOME_TAX.value,
    ]

    prompt = build_clause_extraction_prompt(
        tender_text=(
            "The bidder must possess a valid GST registration "
            "and Udyam certificate."
        ),
        requirement_types=requirement_types,
    )

    assert isinstance(prompt, str)
    assert len(prompt) > 0
    assert "gst_registration" in prompt
    assert "udyam_msme" in prompt

def test_expected_document_fields():

    assert DocumentType.GST_CERTIFICATE in EXPECTED_FIELDS
    assert DocumentType.PAN_CARD in EXPECTED_FIELDS
    assert DocumentType.UDYAM_CERTIFICATE in EXPECTED_FIELDS

    assert "gstin" in EXPECTED_FIELDS[DocumentType.GST_CERTIFICATE]
    assert "pan" in EXPECTED_FIELDS[DocumentType.PAN_CARD]
    assert "udyam_number" in EXPECTED_FIELDS[DocumentType.UDYAM_CERTIFICATE]


def test_custom_exceptions():

    assert issubclass(ExtractionError, Exception)
    assert issubclass(LowConfidenceOCRError, Exception)
    assert issubclass(InvalidIDFormatError, Exception)
    assert issubclass(ClauseExtractionError, Exception)
    assert issubclass(InsufficientDataError, Exception)
    assert issubclass(ModelNotTrainedError, Exception)
    assert issubclass(GraphConstructionError, Exception)
    assert issubclass(AggregationError, Exception)


def test_low_confidence_ocr_error():
    """Check OCR confidence exception."""

    error = LowConfidenceOCRError(
        confidence=40.0,
        document_id="DOC-001",
    )

    assert error.confidence == 40.0
    assert error.document_id == "DOC-001"
    assert "40.0" in str(error)


def test_insufficient_data_error():

    error = InsufficientDataError(
        required=5,
        actual=2,
        context="bid analysis",
    )

    assert error.required == 5
    assert error.actual == 2
    assert "bid analysis" in str(error)


def test_tender_pipeline_without_llm():

    raw_clauses = [
        {
            "type": "gst_registration",
            "mandatory": True,
            "threshold_value": None,
            "source_clause_text": (
                "The bidder must possess a valid GST registration."
            ),
            "source_page": 2,
        },
        {
            "type": "udyam_msme",
            "mandatory": True,
            "threshold_value": "minimum ₹50 lakh turnover",
            "source_clause_text": (
                "The bidder must have a minimum annual turnover of ₹50 lakh."
            ),
            "source_page": 3,
        },
    ]

    requirements = parse_raw_clauses(
        raw_clauses,
        tender_id="PIPELINE-001",
    )

    assert len(requirements) == 2

    threshold = parse_threshold(
        requirements[1].threshold_value
    )

    assert threshold.value == 5_000_000
    assert threshold.unit == "INR"

    from document_ai.ocr.pdf_text_extractor import PageText

    tender_pages = [
        PageText(
            page_number=2,
            text="The bidder must possess a valid GST registration.",
        ),
        PageText(
            page_number=3,
            text="The bidder must have a minimum annual turnover of ₹50 lakh.",
        ),
    ]

    verified = verify_and_map_evidence(
        requirements=requirements,
        tender_pages=tender_pages,
        tender_id="PIPELINE-001",
    )

    assert len(verified) == 2
    assert all(item.citation_verified for item in verified)

    verified_only = filter_verified_only(verified)

    assert len(verified_only) == 2


def test_pod4_basic_health_check():

    assert CLASSIFIER_PROBABILITY_THRESHOLD > 0
    assert CV_SUSPICIOUS_THRESHOLD > 0
    assert SKEWNESS_SUSPICIOUS_THRESHOLD > 0

    # Basic tender processing
    threshold = parse_threshold("minimum ₹10 lakh")

    assert threshold.value == 1_000_000
    assert threshold.unit == "INR"

    # Basic extraction evaluation
    report = evaluate_extraction(
        predictions={
            "DOC-HEALTH": {
                "gstin": "29ABCDE1234F1Z5",
            }
        },
        ground_truth={
            "DOC-HEALTH": {
                "gstin": "29ABCDE1234F1Z5",
            }
        },
    )

    assert report.overall_accuracy == 1.0

    print("\n✓ Pod 4 basic health check passed")