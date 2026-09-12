"""
common/schemas.py

Base Pydantic models shared across two or more Pod 4 modules — the
building blocks other modules' own schemas compose from. Request/
response models for the FastAPI layer stay in api/schemas/, not here.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .enums import DocumentType, VerificationSourceType, RequirementType


class EvidenceReference(BaseModel):
    """
    Points to the exact source that produced a result — document page,
    tender clause, or verification-source response. Core to the
    "evidence-linked, not a black box" pitch principle: every
    downstream result (extraction, verification, risk signal) should
    be traceable back to one of these.
    """
    document_id: Optional[str] = None
    page_number: Optional[int] = None
    clause_text: Optional[str] = None
    source_type: VerificationSourceType
    source_name: Optional[str] = Field(
        default=None, description="e.g. 'Sandbox.co.in GST API', 'Synthetic dataset v2'"
    )
    retrieved_at: datetime = Field(default_factory=datetime.utcnow)


class ExtractedField(BaseModel):
    """One structured field pulled from a bidder document by the
    document_ai extraction module."""
    field_name: str  # e.g. "legal_name", "gstin", "turnover"
    value: str
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    evidence: Optional[EvidenceReference] = None


class BidderIdentity(BaseModel):
    """Minimal identity envelope used wherever a bidder needs to be
    referenced across document_ai, graph_intelligence, and
    risk_classifier without pulling in each module's full schema."""
    bidder_id: str
    legal_name: str
    pan: Optional[str] = None
    gstin: Optional[str] = None
    udyam_number: Optional[str] = None


class TenderRequirement(BaseModel):
    """Structured requirement produced by tender_intelligence's
    clause_extraction, consumed by the rules engine (Pod 2) and
    referenced by explainability."""
    requirement_id: str
    type: RequirementType
    mandatory: bool
    threshold_value: Optional[str] = None
    source_clause_text: str
    source_page: Optional[int] = None


class DocumentClassificationResult(BaseModel):
    document_type: DocumentType
    confidence: float = Field(ge=0.0, le=1.0)


class RiskSignal(BaseModel):
    """One contributing signal into the risk aggregator — e.g. the
    CV/skewness screen's output, the graph module's cluster signal,
    or the classifier's predicted probability. Kept explicit and
    named so the aggregator's explanation can list each signal's
    contribution separately rather than collapsing into one number."""
    signal_name: str  # e.g. "cv_skewness_signal", "graph_signal", "classifier_signal"
    value: float = Field(ge=0.0, le=1.0)
    evidence: Optional[EvidenceReference] = None
