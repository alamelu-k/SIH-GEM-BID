from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.rules_engine import RulesEngine
from app.connectors.mock_connector import MockVerificationConnector
from app.connectors.base import BidderIdentity, VerificationClaim

router = APIRouter(prefix="/compliance", tags=["Compliance Verification & Matrix"])


@router.post("/evaluate/{bidder_id}", response_model=schemas.ComplianceScoreResponse)
def evaluate_compliance(bidder_id: int, db: Session = Depends(get_db)):
    """
    Triggers the deterministic rules engine for a bidder against their tender requirements.
    Runs verification source checks via connectors and calculates the requirement matrix.
    """
    bidder = db.query(models.Bidder).filter(models.Bidder.id == bidder_id).first()

    if not bidder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bidder ID {bidder_id} not found."
        )

    tender = db.query(models.Tender).filter(
        models.Tender.id == bidder.tender_id
    ).first()

    if not tender:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tender ID {bidder.tender_id} not found."
        )

    requirements = db.query(models.Requirement).filter(
        models.Requirement.tender_id == tender.id
    ).all()

    documents = db.query(models.Document).filter(
        models.Document.bidder_id == bidder_id
    ).all()

    # Connector verification steps
    connector = MockVerificationConnector()

    identity = BidderIdentity(
        bidder_id=bidder.id,
        legal_name=bidder.legal_name,
        pan=bidder.pan,
        gstin=bidder.gstin,
        udyam_number=bidder.udyam_number
    )

    # Clean up previous verification results for this evaluation run
    db.query(models.VerificationResult).filter(
        models.VerificationResult.bidder_id == bidder_id
    ).delete()

    db.commit()

    verification_results = []

    for req in requirements:
        code_upper = req.code.upper()
        claim_type = "GENERAL_CLAIM"

        if "GST" in code_upper:
            claim_type = "GST_FILING"

        elif "MSME" in code_upper or "UDYAM" in code_upper:
            claim_type = "MSME_REGISTRATION"

        elif "DEBAR" in code_upper or "BLACK" in code_upper:
            claim_type = "DEBARMENT_CHECK"

        elif "OEM" in code_upper:
            claim_type = "OEM_AUTHORIZATION"

        elif "TURNOVER" in code_upper:
            claim_type = "FINANCIAL_TURNOVER"

        elif "BIS" in code_upper:
            claim_type = "BIS_CERTIFICATION"

        elif "MII" in code_upper:
            claim_type = "MII_DECLARATION"

        elif "EXP" in code_upper:
            claim_type = "EXPERIENCE_VERIFICATION"

        elif "MANPOWER" in code_upper:
            claim_type = "MANPOWER_VERIFICATION"

        elif "EPFO" in code_upper or "ESIC" in code_upper:
            claim_type = "EPFO_ESIC_VERIFICATION"

        elif "SLA" in code_upper:
            claim_type = "SLA_ACCEPTANCE"

        elif "QUALITY" in code_upper:
            claim_type = "QUALITY_CERTIFICATION"

        v_claim = VerificationClaim(
            requirement_code=req.code,
            claim_type=claim_type
        )

        v_resp = connector.verify(identity, v_claim)

        db_vr = models.VerificationResult(
            bidder_id=bidder.id,
            requirement_id=req.id,
            source_name=v_resp.source_name,
            source_type=v_resp.source_type.value,
            raw_response=v_resp.data
        )

        db.add(db_vr)
        db.commit()
        db.refresh(db_vr)

        verification_results.append(db_vr)

    # Run Rules Engine
    engine = RulesEngine()

    overall_status, counts, matrix = engine.evaluate_bidder_compliance(
        requirements=requirements,
        bidder=bidder,
        documents=documents,
        verification_results=verification_results
    )

    # Save or Update Compliance Score Record
    existing_score = db.query(models.ComplianceScore).filter(
        models.ComplianceScore.bidder_id == bidder_id
    ).first()

    matrix_json = [
        m.model_dump() if hasattr(m, "model_dump") else m.dict()
        for m in matrix
    ]

    if existing_score:
        existing_score.overall_status = overall_status
        existing_score.passed_count = counts["passed_count"]
        existing_score.failed_count = counts["failed_count"]
        existing_score.missing_count = counts["missing_count"]
        existing_score.mismatch_count = counts["mismatch_count"]
        existing_score.manual_review_count = counts["manual_review_count"]
        existing_score.matrix_results = matrix_json

        db_score = existing_score

    else:
        db_score = models.ComplianceScore(
            bidder_id=bidder_id,
            tender_id=tender.id,
            overall_status=overall_status,
            passed_count=counts["passed_count"],
            failed_count=counts["failed_count"],
            missing_count=counts["missing_count"],
            mismatch_count=counts["mismatch_count"],
            manual_review_count=counts["manual_review_count"],
            matrix_results=matrix_json
        )

        db.add(db_score)

    db.commit()
    db.refresh(db_score)

    # Audit Log
    audit = models.AuditLog(
        entity_type="COMPLIANCE",
        entity_id=db_score.id,
        action="COMPLIANCE_EVALUATED",
        actor="SYSTEM",
        details={
            "bidder_id": bidder_id,
            "overall_status": overall_status,
            "passed": counts["passed_count"],
            "failed": counts["failed_count"]
        }
    )

    db.add(audit)
    db.commit()

    return db_score


@router.get(
    "/bidder/{bidder_id}",
    response_model=schemas.ComplianceScoreResponse
)
def get_bidder_compliance(
    bidder_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the compliance evaluation score matrix for a specific bidder.
    """
    score = db.query(models.ComplianceScore).filter(
        models.ComplianceScore.bidder_id == bidder_id
    ).first()

    if not score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Compliance score not found for Bidder ID {bidder_id}. "
                f"Run /evaluate/{bidder_id} first."
            )
        )

    return score