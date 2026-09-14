import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

# Import identify_and_extract from tender_extraction
_router_path = Path(__file__).resolve()
_candidates = [
    _router_path.parents[3] / "tender_extraction",
    _router_path.parents[2] / "tender_extraction",
]
for _candidate in _candidates:
    if _candidate.exists() and str(_candidate) not in sys.path:
        sys.path.insert(0, str(_candidate))
        break

from identify_tender import identify_and_extract

router = APIRouter(prefix="/tenders", tags=["Tenders & Requirements"])


@router.post("/identify", status_code=status.HTTP_200_OK)
def identify_tender(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Identify a tender document from an uploaded PDF and extract its requirements.
    Read-only operation: no database writes or persistent side effects.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be a PDF."
        )

    temp_dir = tempfile.mkdtemp()
    temp_path = Path(temp_dir) / file.filename
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = identify_and_extract(str(temp_path))
        if not result.get("identified") and "PDF extraction failed" in result.get("reason", ""):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("reason")
            )
        return result
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing tender PDF: {str(exc)}"
        ) from exc
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


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
