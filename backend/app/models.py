import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Tender(Base):
    """
    Represents a GeM Procurement Tender PDF ingested into the platform.
    """
    __tablename__ = "tenders"

    id = Column(Integer, primary_key=True, index=True)
    tender_number = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    issuing_authority = Column(String(255), nullable=False) # e.g. CPCL / MoPNG
    category = Column(String(100), nullable=True) # e.g. Safety Equipment, Maintenance, MSME Purchase
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    requirements = relationship("Requirement", back_populates="tender", cascade="all, delete-orphan")
    bidders = relationship("Bidder", back_populates="tender", cascade="all, delete-orphan")


class Requirement(Base):
    """
    Represents an extracted requirement clause from a Tender PDF ("bidder must prove X").
    """
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)
    tender_id = Column(Integer, ForeignKey("tenders.id"), nullable=False)
    code = Column(String(50), index=True, nullable=False) # e.g. REQ-MSME-01, REQ-GST-01
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    mandatory = Column(Boolean, default=True)
    source_clause = Column(String(100), nullable=True) # Clause ref, e.g. "Clause 4.2"
    source_page = Column(Integer, nullable=True)
    threshold_value = Column(String(100), nullable=True) # e.g. "50 Lakhs Turnover", "3 Years Experience"

    # Relationships
    tender = relationship("Tender", back_populates="requirements")
    verification_results = relationship("VerificationResult", back_populates="requirement")


class Bidder(Base):
    """
    Represents a vendor/supplier submitting a bid for a specific tender.
    """
    __tablename__ = "bidders"

    id = Column(Integer, primary_key=True, index=True)
    tender_id = Column(Integer, ForeignKey("tenders.id"), nullable=False)
    legal_name = Column(String(255), nullable=False)
    pan = Column(String(255), nullable=True, index=True)
    gstin = Column(String(255), nullable=True, index=True)
    udyam_number = Column(String(50), nullable=True, index=True)
    submission_date = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    tender = relationship("Tender", back_populates="bidders")
    documents = relationship("Document", back_populates="bidder", cascade="all, delete-orphan")
    verification_results = relationship("VerificationResult", back_populates="bidder", cascade="all, delete-orphan")
    compliance_score = relationship("ComplianceScore", back_populates="bidder", uselist=False, cascade="all, delete-orphan")


class Document(Base):
    """
    Represents an uploaded document submitted by a bidder (e.g. GST Cert, Udyam Cert, Turnover PnL).
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    bidder_id = Column(Integer, ForeignKey("bidders.id"), nullable=False)
    document_type = Column(String(50), nullable=False) # e.g. GST_CERTIFICATE, UDYAM_CERTIFICATE, FINANCIAL_STATEMENT
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    upload_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    extracted_fields = Column(JSON, nullable=True) # OCR/LLM Extracted structured JSON data

    # Relationships
    bidder = relationship("Bidder", back_populates="documents")


class VerificationResult(Base):
    """
    Represents the output from a Verification Connector (GST API, Udyam Portal, DigiLocker, Debarment list).
    """
    __tablename__ = "verification_results"

    id = Column(Integer, primary_key=True, index=True)
    bidder_id = Column(Integer, ForeignKey("bidders.id"), nullable=False)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    source_name = Column(String(100), nullable=False) # e.g. "GSTN Portal API", "Udyam Registry Sandbox", "CPCL Debarment DB"
    source_type = Column(String(50), nullable=False) # "official", "licensed_sandbox", "synthetic"
    raw_response = Column(JSON, nullable=True) # Full response JSON payload
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    bidder = relationship("Bidder", back_populates="verification_results")
    requirement = relationship("Requirement", back_populates="verification_results")


class ComplianceScore(Base):
    """
    Represents the overall evaluated compliance verdict and breakdown for a bidder on a tender.
    """
    __tablename__ = "compliance_scores"

    id = Column(Integer, primary_key=True, index=True)
    bidder_id = Column(Integer, ForeignKey("bidders.id"), nullable=False, unique=True)
    tender_id = Column(Integer, ForeignKey("tenders.id"), nullable=False)
    overall_status = Column(String(50), nullable=False) # PASS, FAIL, REQUIRES_MANUAL_REVIEW
    passed_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    missing_count = Column(Integer, default=0)
    mismatch_count = Column(Integer, default=0)
    manual_review_count = Column(Integer, default=0)
    matrix_results = Column(JSON, nullable=True) # Full detailed requirements matrix results
    calculated_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    bidder = relationship("Bidder", back_populates="compliance_score")


class AuditLog(Base):
    """
    Append-only audit trail logging every action and evaluation for transparency.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False) # TENDER, BIDDER, DOCUMENT, VERIFICATION, COMPLIANCE
    entity_id = Column(Integer, nullable=False)
    action = Column(String(100), nullable=False) # e.g. TENDER_INGESTED, RULE_EVALUATED, OFFICER_OVERRIDE
    actor = Column(String(100), default="SYSTEM") # Procurement Officer or SYSTEM
    details = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


class Officer(Base):
    """
    Represents a procurement officer / platform user with 2FA OTP authentication.
    """
    __tablename__ = "officers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="officer")
    otp_code = Column(String(10), nullable=True)
    otp_expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
