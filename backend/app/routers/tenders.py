from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/tenders", tags=["Tenders & Requirements"])


@router.post("", response_model=schemas.TenderResponse, status_code=status.HTTP_201_CREATED)
def create_tender(tender_in: schemas.TenderCreate, db: Session = Depends(get_db)):
    """
    Ingest a new GeM Tender PDF / specification with its extracted requirements.
    """
    existing = db.query(models.Tender).filter(models.Tender.tender_number == tender_in.tender_number).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tender number '{tender_in.tender_number}' already exists."
        )

    db_tender = models.Tender(
        tender_number=tender_in.tender_number,
        title=tender_in.title,
        issuing_authority=tender_in.issuing_authority,
        category=tender_in.category
    )
    db.add(db_tender)
    db.commit()
    db.refresh(db_tender)

    # Add associated requirements if provided
    if tender_in.requirements:
        for req in tender_in.requirements:
            db_req = models.Requirement(
                tender_id=db_tender.id,
                code=req.code,
                title=req.title,
                description=req.description,
                mandatory=req.mandatory,
                source_clause=req.source_clause,
                source_page=req.source_page,
                threshold_value=req.threshold_value
            )
            db.add(db_req)
        db.commit()
        db.refresh(db_tender)

    # Record Audit Log
    audit = models.AuditLog(
        entity_type="TENDER",
        entity_id=db_tender.id,
        action="TENDER_INGESTED",
        actor="SYSTEM",
        details={"tender_number": db_tender.tender_number, "requirement_count": len(db_tender.requirements)}
    )
    db.add(audit)
    db.commit()

    return db_tender


@router.get("", response_model=List[schemas.TenderResponse])
def list_tenders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all ingested tenders in the system.
    """
    tenders = db.query(models.Tender).offset(skip).limit(limit).all()
    return tenders


@router.get("/{tender_id}", response_model=schemas.TenderResponse)
def get_tender(tender_id: int, db: Session = Depends(get_db)):
    """
    Retrieve details and extracted requirements for a specific tender by ID.
    """
    tender = db.query(models.Tender).filter(models.Tender.id == tender_id).first()
    if not tender:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tender ID {tender_id} not found."
        )
    return tender
