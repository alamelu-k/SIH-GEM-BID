from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.ml.service import DocumentMLService

router = APIRouter(prefix="/bidders", tags=["Bidders & Document Submissions"])


@router.post("", response_model=schemas.BidderResponse, status_code=status.HTTP_201_CREATED)
def create_bidder(bidder_in: schemas.BidderCreate, db: Session = Depends(get_db)):
    """
    Register a bidder for a specific tender.
    """
    tender = db.query(models.Tender).filter(models.Tender.id == bidder_in.tender_id).first()
    if not tender:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tender ID {bidder_in.tender_id} does not exist."
        )

    db_bidder = models.Bidder(
        tender_id=bidder_in.tender_id,
        legal_name=bidder_in.legal_name,
        pan=bidder_in.pan,
        gstin=bidder_in.gstin,
        udyam_number=bidder_in.udyam_number
    )
    db.add(db_bidder)
    db.commit()
    db.refresh(db_bidder)

    # Audit Log
    audit = models.AuditLog(
        entity_type="BIDDER",
        entity_id=db_bidder.id,
        action="BIDDER_REGISTERED",
        actor="SYSTEM",
        details={"legal_name": db_bidder.legal_name, "tender_id": db_bidder.tender_id}
    )
    db.add(audit)
    db.commit()

    return db_bidder


@router.get("", response_model=List[schemas.BidderResponse])
def list_bidders(tender_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all bidders, optionally filtered by tender_id.
    """
    query = db.query(models.Bidder)
    if tender_id:
        query = query.filter(models.Bidder.tender_id == tender_id)
    return query.offset(skip).limit(limit).all()


@router.post(
    "/{bidder_id}/documents",
    response_model=schemas.DocumentResponse,
    status_code=status.HTTP_201_CREATED
)
def upload_bidder_document(
    bidder_id: int,
    doc_in: schemas.DocumentBase,
    db: Session = Depends(get_db)
):
    """
    Record an uploaded document and optionally classify its text
    using the existing ML document classifier.
    """

    bidder = (
        db.query(models.Bidder)
        .filter(models.Bidder.id == bidder_id)
        .first()
    )

    if not bidder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bidder ID {bidder_id} not found."
        )

    # Copy user-provided extracted fields.
    extracted_fields = dict(doc_in.extracted_fields or {})

    # Run ML classification only when extracted text is provided.
    if doc_in.extracted_text and doc_in.extracted_text.strip():

        try:
            ml_result = DocumentMLService.classify(
                doc_in.extracted_text
            )

            predicted_type = str(
                ml_result.document_type.value
            ).upper()

            confidence = float(
                ml_result.confidence
            )

            submitted_type = doc_in.document_type.upper()

            matches = submitted_type == predicted_type

            extracted_fields["ml_classification"] = {
                "predicted_type": predicted_type,
                "confidence": confidence,
                "matches_submitted_type": matches,
                "status": "MATCH" if matches else "MISMATCH"
            }

        except Exception as exc:
            extracted_fields["ml_classification"] = {
                "status": "ERROR",
                "message": str(exc)
            }

    else:
        extracted_fields["ml_classification"] = {
            "status": "NOT_PERFORMED",
            "message": "No extracted text was provided."
        }

    db_doc = models.Document(
        bidder_id=bidder_id,
        document_type=doc_in.document_type,
        file_name=doc_in.file_name,
        file_path=doc_in.file_path,
        extracted_fields=extracted_fields
    )

    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    audit = models.AuditLog(
        entity_type="DOCUMENT",
        entity_id=db_doc.id,
        action="DOCUMENT_UPLOADED",
        actor="SYSTEM",
        details={
            "bidder_id": bidder_id,
            "document_type": db_doc.document_type,
            "file_name": db_doc.file_name,
            "ml_status": extracted_fields.get(
                "ml_classification",
                {}
            ).get("status")
        }
    )

    db.add(audit)
    db.commit()

    return db_doc