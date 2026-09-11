"""
Verification Connectors Package
Pluggable connector interface to integrate GST, Udyam, DigiLocker, and Debarment verification sources.
"""
from app.connectors.base import VerificationConnector, VerificationResponse, SourceType, BidderIdentity, VerificationClaim

__all__ = [
    "VerificationConnector",
    "VerificationResponse",
    "SourceType",
    "BidderIdentity",
    "VerificationClaim"
]
