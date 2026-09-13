from enum import Enum


class DocumentType(str, Enum):
    GST_CERTIFICATE = "gst_certificate"
    PAN_CARD = "pan_card"
    UDYAM_CERTIFICATE = "udyam_certificate"
    TURNOVER_STATEMENT = "turnover_statement"
    OEM_AUTHORIZATION_LETTER = "oem_authorization_letter"
    EPFO_ESIC_CERTIFICATE = "epfo_esic_certificate"
    STARTUP_INDIA_CERTIFICATE = "startup_india_certificate"
    NSIC_CERTIFICATE = "nsic_certificate"
    BIS_LICENSE = "bis_license"
    TENDER_PDF = "tender_pdf"
    UNKNOWN = "unknown"


class VerificationSourceType(str, Enum):
    OFFICIAL = "official"
    LICENSED_SANDBOX = "licensed_sandbox"
    SYNTHETIC = "synthetic"


class RequirementType(str, Enum):
    UDYAM_MSME = "udyam_msme"
    GST_REGISTRATION = "gst_registration"
    GST_FILING = "gst_filing"
    PAN_INCOME_TAX = "pan_income_tax"
    MAKE_IN_INDIA_LOCAL_CONTENT = "make_in_india_local_content"
    EPFO_ESIC = "epfo_esic"
    STARTUP_INDIA = "startup_india"
    NSIC = "nsic"
    OEM_AUTHORIZATION = "oem_authorization"
    DIGILOCKER_DOCUMENT = "digilocker_document"
    BLACKLISTING_DEBARMENT = "blacklisting_debarment"
    OTHER = "other"


class ComplianceVerdict(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    MISSING = "missing"
    MISMATCH = "mismatch"
    MANUAL_REVIEW = "manual_review"


class BidderArchetype(str, Enum):
    CLEAN = "clean"
    MISSING_DOCUMENT = "missing_document"
    MISMATCH = "mismatch"
    EXPIRED_INVALID = "expired_invalid"
    BORDERLINE = "borderline"
