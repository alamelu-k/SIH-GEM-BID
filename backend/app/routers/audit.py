from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import get_current_officer, require_admin

router = APIRouter(prefix="/audit", tags=["Audit Trail"])


@router.post("", response_model=schemas.AuditLogResponse, status_code=status.HTTP_201_CREATED)
def record_audit_event(
    audit_in: schemas.AuditLogCreate,
    db: Session = Depends(get_db),
    current_officer: models.Officer = Depends(get_current_officer),
):
    """
    Record an append-only audit event (Officer).
    Actor is securely bound to the authenticated officer's email.
    """
    db_audit = models.AuditLog(
        entity_type=audit_in.entity_type,
        entity_id=audit_in.entity_id,
        action=audit_in.action,
        actor=current_officer.email,
        details=audit_in.details
    )
    db.add(db_audit)
    db.commit()
    db.refresh(db_audit)
    return db_audit


@router.get("", response_model=List[schemas.AuditLogResponse])
def get_audit_trail(
    entity_type: str = None, 
    entity_id: int = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_officer: models.Officer = Depends(require_admin),
):
    """
    Query chronological audit trail logs, optionally filtered by entity (Admin-only).
    """
    query = db.query(models.AuditLog)
    if entity_type:
        query = query.filter(models.AuditLog.entity_type == entity_type.upper())
    if entity_id:
        query = query.filter(models.AuditLog.entity_id == entity_id)
    return query.order_by(models.AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
