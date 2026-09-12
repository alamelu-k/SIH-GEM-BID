from app.connectors.base import (
    VerificationConnector,
    VerificationResponse,
    SourceType,
    BidderIdentity,
    VerificationClaim,
)


class MockVerificationConnector(VerificationConnector):
    """
    Synthetic verification connector for CodeVeil testing.

    This connector provides deterministic responses for the synthetic
    bidder archetypes used in the project.

    Source type is SYNTHETIC because these are mock/demo responses,
    not live government portal checks.
    """

    def __init__(
        self,
        source_name: str = "CodeVeil Synthetic Verification Hub",
        source_type: SourceType = SourceType.SYNTHETIC,
    ):
        self._source_name = source_name
        self._source_type = source_type

    @property
    def source_name(self) -> str:
        return self._source_name

    @property
    def source_type(self) -> SourceType:
        return self._source_type

    def _response(
        self,
        verified: bool,
        data: dict,
        error_message: str | None = None,
        confidence_score: float = 1.0,
    ) -> VerificationResponse:
        return VerificationResponse(
            source_name=self.source_name,
            source_type=self.source_type,
            verified=verified,
            data=data,
            error_message=error_message,
            confidence_score=confidence_score,
        )

    def verify(
        self,
        identity: BidderIdentity,
        claim: VerificationClaim,
    ) -> VerificationResponse:

        claim_type = claim.claim_type.upper()
        requirement_code = claim.requirement_code.upper()
        legal_name = identity.legal_name.upper()

        # ---------------------------------------------------------
        # GST verification
        # ---------------------------------------------------------
        if claim_type == "GST_FILING":

            if not identity.gstin:
                return self._response(
                    verified=False,
                    data={
                        "status": "MISSING",
                        "details": "No GSTIN provided by bidder",
                    },
                    error_message="GSTIN is missing",
                )

            if "INVALID" in identity.gstin.upper():
                return self._response(
                    verified=False,
                    data={
                        "gstin": identity.gstin,
                        "status": "MISMATCH",
                        "legal_name_match": False,
                        "details": "GST registration details do not match bidder identity",
                    },
                    error_message="GSTIN identity mismatch",
                )

            if "EXPIRED" in identity.gstin.upper():
                return self._response(
                    verified=False,
                    data={
                        "gstin": identity.gstin,
                        "status": "INACTIVE",
                        "filing_status": "PENDING_6_MONTHS",
                    },
                    error_message="GST registration is inactive",
                )

            return self._response(
                verified=True,
                data={
                    "gstin": identity.gstin,
                    "legal_name": identity.legal_name,
                    "status": "ACTIVE",
                    "filing_status": "REGULAR",
                },
            )

        # ---------------------------------------------------------
        # Udyam / MSME verification
        # ---------------------------------------------------------
        elif claim_type == "MSME_REGISTRATION":

            if not identity.udyam_number:
                return self._response(
                    verified=False,
                    data={
                        "status": "MISSING",
                        "details": "No Udyam Registration Number provided",
                    },
                    error_message="Udyam Number is missing",
                )

            if "INVALID" in identity.udyam_number.upper():
                return self._response(
                    verified=False,
                    data={
                        "udyam_number": identity.udyam_number,
                        "status": "MISMATCH",
                        "legal_name_match": False,
                        "details": "Udyam registration identity does not match bidder",
                    },
                    error_message="Udyam identity mismatch",
                )

            if "CANCELLED" in identity.udyam_number.upper():
                return self._response(
                    verified=False,
                    data={
                        "udyam_number": identity.udyam_number,
                        "status": "INACTIVE",
                        "registration_status": "CANCELLED",
                    },
                    error_message="Udyam registration is inactive/cancelled",
                )

            return self._response(
                verified=True,
                data={
                    "udyam_number": identity.udyam_number,
                    "legal_name": identity.legal_name,
                    "enterprise_type": "MICRO",
                    "major_activity": "MANUFACTURING",
                    "valid_until": "PERPETUAL",
                    "status": "ACTIVE",
                },
            )

        # ---------------------------------------------------------
        # Debarment verification
        # ---------------------------------------------------------
        elif claim_type == "DEBARMENT_CHECK":

            is_blacklisted = (
                "DEBARRED" in legal_name
                or "BLACKLIST" in legal_name
            )

            return self._response(
                verified=not is_blacklisted,
                data={
                    "debarred": is_blacklisted,
                    "matched_entity": identity.legal_name if is_blacklisted else None,
                    "source_portal": "CPCL / CPPP Central Debarment Database",
                    "status": "DEBARRED" if is_blacklisted else "CLEAR",
                },
                error_message=(
                    "Entity is debarred/blacklisted from government procurement"
                    if is_blacklisted
                    else None
                ),
            )

        # ---------------------------------------------------------
        # OEM authorization
        # ---------------------------------------------------------
        elif claim_type == "OEM_AUTHORIZATION":

            if "VENDHAR" in legal_name:
                return self._response(
                    verified=False,
                    data={
                        "status": "MISSING",
                        "document_type": "OEM_AUTH_LETTER",
                        "details": "OEM authorization letter not submitted",
                    },
                    error_message="OEM authorization document is missing",
                )

            return self._response(
                verified=True,
                data={
                    "status": "VERIFIED",
                    "document_type": "OEM_AUTH_LETTER",
                    "details": "OEM authorization requirement satisfied",
                },
            )

        # ---------------------------------------------------------
        # BIS certification
        # ---------------------------------------------------------
        elif claim_type == "BIS_CERTIFICATION":

            if "ANBU" in legal_name:
                return self._response(
                    verified=False,
                    data={
                        "status": "EXPIRED",
                        "document_type": "BIS_LICENSE",
                        "details": "BIS license has expired",
                    },
                    error_message="BIS certification is expired",
                )

            return self._response(
                verified=True,
                data={
                    "status": "ACTIVE",
                    "document_type": "BIS_LICENSE",
                    "details": "BIS certification is valid",
                },
            )

        # ---------------------------------------------------------
        # MII declaration
        # ---------------------------------------------------------
        elif claim_type == "MII_DECLARATION":

            return self._response(
                verified=True,
                data={
                    "status": "VERIFIED",
                    "document_type": "MII_DECLARATION",
                },
            )

        # ---------------------------------------------------------
        # Experience verification
        # ---------------------------------------------------------
        elif claim_type == "EXPERIENCE_VERIFICATION":

            return self._response(
                verified=True,
                data={
                    "status": "VERIFIED",
                    "document_type": "EXPERIENCE_CERT",
                },
            )

        # ---------------------------------------------------------
        # Financial turnover
        # ---------------------------------------------------------
        elif claim_type == "FINANCIAL_TURNOVER":

            if "THIRUVALLUVAR" in legal_name or "GANESH" in legal_name:
                return self._response(
                    verified=False,
                    data={
                        "status": "MANUAL_REVIEW",
                        "document_type": "FINANCIAL_STATEMENT",
                        "details": "Turnover is borderline against the tender threshold",
                    },
                    error_message="Turnover requires manual review",
                    confidence_score=0.75,
                )

            return self._response(
                verified=True,
                data={
                    "status": "VERIFIED",
                    "document_type": "FINANCIAL_STATEMENT",
                },
            )

        # ---------------------------------------------------------
        # Manpower verification
        # ---------------------------------------------------------
        elif claim_type == "MANPOWER_VERIFICATION":

            if "VETRI" in legal_name:
                return self._response(
                    verified=False,
                    data={
                        "status": "MANUAL_REVIEW",
                        "document_type": "MANPOWER_LIST",
                        "details": "Manpower strength is borderline",
                    },
                    error_message="Manpower requires manual review",
                    confidence_score=0.75,
                )

            return self._response(
                verified=True,
                data={
                    "status": "VERIFIED",
                    "document_type": "MANPOWER_LIST",
                },
            )

        # ---------------------------------------------------------
        # EPFO / ESIC verification
        # ---------------------------------------------------------
        elif claim_type == "EPFO_ESIC_VERIFICATION":

            if "SPK" in legal_name:
                return self._response(
                    verified=False,
                    data={
                        "status": "MISSING",
                        "document_type": "EPFO_ESI_CERT",
                        "details": "EPFO/ESIC certificate not submitted",
                    },
                    error_message="EPFO/ESIC document is missing",
                )

            if "COROMANDEL" in legal_name:
                return self._response(
                    verified=False,
                    data={
                        "status": "INACTIVE",
                        "document_type": "EPFO_ESI_CERT",
                        "details": "ESIC registration is inactive",
                    },
                    error_message="EPFO/ESIC registration is inactive",
                )

            return self._response(
                verified=True,
                data={
                    "status": "ACTIVE",
                    "document_type": "EPFO_ESI_CERT",
                },
            )

        # ---------------------------------------------------------
        # SLA acceptance
        # ---------------------------------------------------------
        elif claim_type == "SLA_ACCEPTANCE":

            return self._response(
                verified=True,
                data={
                    "status": "VERIFIED",
                    "document_type": "SLA_ACCEPTANCE",
                },
            )

        # ---------------------------------------------------------
        # Quality certification
        # ---------------------------------------------------------
        elif claim_type == "QUALITY_CERTIFICATION":

            return self._response(
                verified=True,
                data={
                    "status": "VERIFIED",
                    "document_type": "QUALITY_CERT",
                },
            )

        # ---------------------------------------------------------
        # Tender-specific MSME preference requirements
        # ---------------------------------------------------------
        elif requirement_code in {
            "REQ-MSE-CATEGORY-01",
            "REQ-EMD-EXEMPT-01",
            "REQ-L1-PREFERENCE-01",
        }:

            return self._response(
                verified=True,
                data={
                    "status": "VERIFIED",
                    "details": "Requirement derived from valid MSME/Udyam status",
                },
            )

        # ---------------------------------------------------------
        # Safe fallback
        # ---------------------------------------------------------
        return self._response(
            verified=False,
            data={
                "status": "MANUAL_REVIEW",
                "claim_type": claim_type,
                "requirement_code": claim.requirement_code,
                "details": "No synthetic verification rule is defined for this claim",
            },
            error_message="Unsupported verification claim requires manual review",
            confidence_score=0.5,
        )