from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, ConfigDict

# --- Requirement Schemas ---
class RequirementBase(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    mandatory: bool = True
    source_clause: Optional[str] = None
    source_page: Optional[int] = None
    threshold_value: Optional[str] = None

class RequirementCreate(RequirementBase):
    pass

class RequirementResponse(RequirementBase):
    id: int
    tender_id: int
    model_config = ConfigDict(from_attributes=True)


# --- Tender Schemas ---
class TenderBase(BaseModel):
    tender_number: str
    title: str
    issuing_authority: str
    category: Optional[str] = None

class TenderCreate(TenderBase):
    requirements: Optional[List[RequirementCreate]] = []

class TenderResponse(TenderBase):
    id: int
    created_at: datetime
    requirements: List[RequirementResponse] = []
    model_config = ConfigDict(from_attributes=True)


# --- Document Schemas ---
class DocumentBase(BaseModel):
    document_type: str
    file_name: str
    file_path: str
    extracted_fields: Optional[Dict[str, Any]] = None

class DocumentCreate(DocumentBase):
    bidder_id: int

class DocumentResponse(DocumentBase):
    id: int
    bidder_id: int
    upload_timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


# --- Bidder Schemas ---
class BidderBase(BaseModel):
    legal_name: str
    pan: Optional[str] = None
    gstin: Optional[str] = None
    udyam_number: Optional[str] = None

class BidderCreate(BidderBase):
    tender_id: int

class BidderResponse(BidderBase):
    id: int
    tender_id: int
    submission_date: datetime
    documents: List[DocumentResponse] = []
    model_config = ConfigDict(from_attributes=True)


# --- Verification Result Schemas ---
class VerificationResultCreate(BaseModel):
    bidder_id: int
    requirement_id: int
    source_name: str
    source_type: str  # official, licensed_sandbox, synthetic
    raw_response: Dict[str, Any]

class VerificationResultResponse(VerificationResultCreate):
    id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


# --- Compliance Schemas ---
class RequirementRuleItem(BaseModel):
    requirement_id: int
    rule_code: str
    requirement_title: str
    mandatory: bool
    status: str  # PASS, FAIL, MISSING, MISMATCH, MANUAL_REVIEW
    severity: str  # CRITICAL, WARNING, INFO
    reason: str
    evidence_reference: Optional[str] = None
    source_name: Optional[str] = None
    source_type: Optional[str] = None
    code: Optional[str] = None
    title: Optional[str] = None


class ComplianceScoreResponse(BaseModel):
    id: int
    bidder_id: int
    tender_id: int
    overall_status: str
    passed_count: int
    failed_count: int
    missing_count: int
    mismatch_count: int
    manual_review_count: int
    matrix_results: List[RequirementRuleItem] = []
    calculated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- Audit Log Schemas ---
class AuditLogCreate(BaseModel):
    entity_type: str
    entity_id: int
    action: str
    actor: str = "SYSTEM"
    details: Optional[Dict[str, Any]] = None

class AuditLogResponse(AuditLogCreate):
    id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
