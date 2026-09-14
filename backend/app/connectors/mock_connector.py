from app.connectors.base import (
    VerificationConnector,
    VerificationResponse,
    SourceType,
    BidderIdentity,
    VerificationClaim,
)


class MockVerificationConnector(VerificationConnector):
    """
    Demonstration Mock Connector providing deterministic synthetic responses
    for GST, Udyam/MSME, PAN, Debarment, OEM, BIS, MII, Experience,
    Financial Turnover, Manpower, EPFO/ESIC, SLA, and Quality verification.
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
    ) -> VerificationResponse:
        return VerificationResponse(
            source_name=self.source_name,
            source_type=self.source_type,
            verified=verified,
            data=data,
            error_message=error_message,
        )

    def verify(
        self,
        identity: BidderIdentity,
        claim: VerificationClaim,
    ) -> VerificationResponse:

        claim_type = claim.claim_type.upper()
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

            # Synthetic identity mismatch case
            if legal_name.startswith("KAVERI"):
                return self._response(
                    verified=False,
                    data={
                        "gstin": identity.gstin,
                        "status": "MISMATCH",
                        "legal_name": "KAVERI REGISTERED ENTITY",
                        "legal_name_match": False,
                        "details": (
                            "GST registered legal name does not match "
                            "bidder identity"
                        ),
                    },
                    error_message="GSTIN identity mismatch",
                )

            if "INVALID" in identity.gstin.upper():
                return self._response(
                    verified=False,
                    data={
                        "gstin": identity.gstin,
                        "status": "MISMATCH",
                        "legal_name_match": False,
                        "details": (
                            "GST registration details do not match "
                            "bidder identity"
                        ),
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
                        "details": (
                            "No Udyam Registration Number provided"
                        ),
                    },
                    error_message="Udyam Number is missing",
                )

            # Synthetic identity mismatch case
            if legal_name.startswith("LAKSHMI"):
                return self._response(
                    verified=False,
                    data={
                        "udyam_number": identity.udyam_number,
                        "status": "MISMATCH",
                        "legal_name": "LAKSHMI REGISTERED ENTITY",
                        "legal_name_match": False,
                        "details": (
                            "Udyam registered legal name does not match "
                            "bidder identity"
                        ),
                    },
                    error_message="Udyam identity mismatch",
                )

            if "INVALID" in identity.udyam_number.upper():
                return self._response(
                    verified=False,
                    data={
                        "udyam_number": identity.udyam_number,
                        "status": "MISMATCH",
                        "legal_name_match": False,
                        "details": (
                            "Udyam registration identity does not "
                            "match bidder"
                        ),
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
        # PAN verification
        # ---------------------------------------------------------
        elif claim_type == "PAN_VERIFICATION":

            if not identity.pan:
                return self._response(
                    verified=False,
                    data={
                        "status": "MISSING",
                        "details": "No PAN provided by bidder",
                    },
                    error_message="PAN is missing",
                )

            # Synthetic identity mismatch case
            if legal_name.startswith("MURUGA"):
                return self._response(
                    verified=False,
                    data={
                        "pan": identity.pan,
                        "status": "MISMATCH",
                        "legal_name": "MURUGA REGISTERED ENTITY",
                        "legal_name_match": False,
                        "details": (
                            "PAN registered legal name does not match "
                            "bidder identity"
                        ),
                    },
                    error_message="PAN identity mismatch",
                )

            return self._response(
                verified=True,
                data={
                    "pan": identity.pan,
                    "legal_name": identity.legal_name,
                    "status": "VERIFIED",
                    "legal_name_match": True,
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
                    "matched_entity": (
                        identity.legal_name if is_blacklisted else None
                    ),
                    "source_portal": (
                        "CPCL / CPPP Central Debarment Database"
                    ),
                    "status": (
                        "DEBARRED" if is_blacklisted else "CLEAR"
                    ),
                },
                error_message=(
                    "Entity is debarred/blacklisted from government "
                    "procurement"
                    if is_blacklisted
                    else None
                ),
            )

        # ---------------------------------------------------------
        # OEM Authorization verification
        # ---------------------------------------------------------
        elif claim_type == "OEM_AUTHORIZATION":

            if "VENDHAR" in legal_name:
                return self._response(
                    verified=False,
                    data={
                        "status": "MISSING",
                        "details": (
                            "OEM authorization document is not available"
                        ),
                    },
                    error_message="OEM authorization is missing",
                )

            return self._response(
                verified=True,
                data={
                    "status": "VERIFIED",
                    "authorized": True,
                    "legal_name": identity.legal_name,
                },
            )

        # ---------------------------------------------------------
        # BIS Certification verification
        # ---------------------------------------------------------
        elif claim_type == "BIS_CERTIFICATION":

            if "ANBU" in legal_name:
                return self._response(
                    verified=False,
                    data={
                        "status": "INACTIVE",
                        "details": "BIS certification has expired",
                    },
                    error_message="BIS certification is expired",
                )

            return self._response(
                verified=True,
                data={
                    "status": "ACTIVE",
                    "certified": True,
                    "legal_name": identity.legal_name,
                },
            )

        # ---------------------------------------------------------
        # Make in India declaration
        # ---------------------------------------------------------
        elif claim_type == "MII_DECLARATION":

            return self._response(
                verified=True,
                data={
                    "status": "VERIFIED",
                    "document_type": "MII_DECLARATION",
                    "declaration_valid": True,
                },
            )

        # ---------------------------------------------------------
        # Experience verification
        # ---------------------------------------------------------
        elif claim_type == "EXPERIENCE_VERIFICATION":

            if "THIRUVALLUVAR" in legal_name:
                return self._response(
                    verified=False,
                    data={
                        "status": "MANUAL_REVIEW",
                        "details": (
                            "Experience records require manual verification"
                        ),
                    },
                    error_message="Experience requires manual review",
                )

            return self._response(
                verified=True,
                data={
                    "status": "VERIFIED",
                    "experience_verified": True,
                },
            )

        # ---------------------------------------------------------
        # Financial turnover verification
        # ---------------------------------------------------------
        elif claim_type == "FINANCIAL_TURNOVER":

            if (
                "THIRUVALLUVAR" in legal_name
                or "GANESH" in legal_name
            ):
                return self._response(
                    verified=False,
                    data={
                        "status": "MANUAL_REVIEW",
                        "details": (
                            "Financial turnover requires manual verification"
                        ),
                    },
                    error_message="Turnover requires manual review",
                )

            return self._response(
                verified=True,
                data={
                    "status": "VERIFIED",
                    "turnover_verified": True,
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
                        "details": (
                            "Manpower records require manual verification"
                        ),
                    },
                    error_message="Manpower requires manual review",
                )

            return self._response(
                verified=True,
                data={
                    "status": "VERIFIED",
                    "manpower_verified": True,
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
                        "details": (
                            "EPFO/ESIC verification data is unavailable"
                        ),
                    },
                    error_message="EPFO/ESIC data is missing",
                )

            if "COROMANDEL" in legal_name:
                return self._response(
                    verified=False,
                    data={
                        "status": "INACTIVE",
                        "details": (
                            "EPFO/ESIC registration is inactive"
                        ),
                    },
                    error_message="EPFO/ESIC registration is inactive",
                )

            return self._response(
                verified=True,
                data={
                    "status": "VERIFIED",
                    "epfo_esic_verified": True,
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
                    "sla_accepted": True,
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
                    "quality_certified": True,
                },
            )

        # ---------------------------------------------------------
        # Tender-specific MSME preference requirements
        # ---------------------------------------------------------
        elif "MSME" in claim_type or "UDYAM" in claim_type:

            if not identity.udyam_number:
                return self._response(
                    verified=False,
                    data={
                        "status": "MISSING",
                        "details": (
                            "MSME/Udyam registration number is missing"
                        ),
                    },
                    error_message="MSME/Udyam registration is missing",
                )

            return self._response(
                verified=True,
                data={
                    "status": "ACTIVE",
                    "udyam_number": identity.udyam_number,
                    "legal_name": identity.legal_name,
                },
            )

        # ---------------------------------------------------------
        # Safe fallback for unsupported claims
        # ---------------------------------------------------------
        return self._response(
            verified=True,
            data={
                "claim": claim.model_dump()
                if hasattr(claim, "model_dump")
                else claim.dict(),
                "status": "VERIFIED_DEFAULT",
            },
        )
