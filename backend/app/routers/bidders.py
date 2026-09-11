from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

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


@router.get("/{bidder_id}", response_model=schemas.BidderResponse)
def get_bidder(bidder_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information for a specific bidder.
    """
    bidder = db.query(models.Bidder).filter(models.Bidder.id == bidder_id).first()
    if not bidder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bidder ID {bidder_id} not found."
        )
    return bidder


@router.post("/{bidder_id}/documents", response_model=schemas.DocumentResponse, status_code=status.HTTP_201_CREATED)
def upload_bidder_document(bidder_id: int, doc_in: schemas.DocumentBase, db: Session = Depends(get_db)):
    """
    Record an uploaded document submission for a bidder.
    """
    bidder = db.query(models.Bidder).filter(models.Bidder.id == bidder_id).first()
    if not bidder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bidder ID {bidder_id} not found."
        )

    db_doc = models.Document(
        bidder_id=bidder_id,
        document_type=doc_in.document_type,
        file_name=doc_in.file_name,
        file_path=doc_in.file_path,
        extracted_fields=doc_in.extracted_fields
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    # Audit Log
    audit = models.AuditLog(
        entity_type="DOCUMENT",
        entity_id=db_doc.id,
        action="DOCUMENT_UPLOADED",
        actor="SYSTEM",
        details={"bidder_id": bidder_id, "document_type": db_doc.document_type, "file_name": db_doc.file_name}
    )
    db.add(audit)
    db.commit()

    return db_doc
