from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel


class SourceType(str, Enum):
    """
    Honest transparency label for verification sources:
    - OFFICIAL: Direct government portal / API key connection
    - LICENSED_SANDBOX: Authorized 3rd party sandbox API (e.g. Surepass/Setu)
    - SYNTHETIC: Local mock/demonstration provider
    """
    OFFICIAL = "official"
    LICENSED_SANDBOX = "licensed_sandbox"
    SYNTHETIC = "synthetic"


class BidderIdentity(BaseModel):
    bidder_id: int
    legal_name: str
    pan: Optional[str] = None
    gstin: Optional[str] = None
    udyam_number: Optional[str] = None


class VerificationClaim(BaseModel):
    requirement_code: str
    claim_type: str  # GST_FILING, MSME_REGISTRATION, OEM_AUTHORIZATION, FINANCIAL_TURNOVER, DEBARMENT_CHECK
    claimed_value: Optional[Any] = None
    supporting_document_path: Optional[str] = None


class VerificationResponse(BaseModel):
    source_name: str
    source_type: SourceType
    verified: bool
    data: Dict[str, Any]
    error_message: Optional[str] = None
    confidence_score: float = 1.0  # 0.0 to 1.0


class VerificationConnector(ABC):
    """
    Abstract Base Class for all Verification Source Connectors.
    Sadhana & Gayatri will implement this interface for GST, Udyam, DigiLocker, and Debarment checks.
    """

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Name of the verification source (e.g. 'GSTN Portal API')."""
        pass

    @property
    @abstractmethod
    def source_type(self) -> SourceType:
        """Source transparency type (OFFICIAL, LICENSED_SANDBOX, SYNTHETIC)."""
        pass

    @abstractmethod
    def verify(self, identity: BidderIdentity, claim: VerificationClaim) -> VerificationResponse:
        """
        Main verification method. Must return a consistent VerificationResponse shape.
        """
        pass
