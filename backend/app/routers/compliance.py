from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.services.compliance_service import evaluate_bidder_compliance

router = APIRouter(
prefix="/compliance",
tags=["Compliance Verification & Matrix"]
)

@router.post(
    "/evaluate/{bidder_id}",
    response_model=schemas.ComplianceScoreResponse,
)
def evaluate_compliance(
    bidder_id: int,
    db: Session = Depends(get_db),
):
    try:
        return evaluate_bidder_compliance(
            bidder_id=bidder_id,
            db=db,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/bidder/{bidder_id}",
    response_model=schemas.ComplianceScoreResponse,
)
def get_bidder_compliance(
    bidder_id: int,
    db: Session = Depends(get_db),
):
    score = (
        db.query(models.ComplianceScore)
        .filter(models.ComplianceScore.bidder_id == bidder_id)
        .first()
    )

    if not score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Compliance score not found for Bidder ID {bidder_id}. "
                f"Run /evaluate/{bidder_id} first."
            ),
        )

    return score
