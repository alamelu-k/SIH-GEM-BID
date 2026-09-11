from app.connectors.base import VerificationConnector, VerificationResponse, SourceType, BidderIdentity, VerificationClaim

class MockVerificationConnector(VerificationConnector):
    """
    Demonstration Mock Connector providing deterministic test responses for 
    GST, Udyam, Debarment, and OEM verification.
    """

    def __init__(self, source_name: str = "CodeVeil Synthetic Verification Hub", source_type: SourceType = SourceType.SYNTHETIC):
        self._source_name = source_name
        self._source_type = source_type

    @property
    def source_name(self) -> str:
        return self._source_name

    @property
    def source_type(self) -> SourceType:
        return self._source_type

    def verify(self, identity: BidderIdentity, claim: VerificationClaim) -> VerificationResponse:
        claim_type = claim.claim_type.upper()

        if claim_type == "GST_FILING":
            # Simulate GST verification logic
            if not identity.gstin:
                return VerificationResponse(
                    source_name=self.source_name,
                    source_type=self.source_type,
                    verified=False,
                    data={"status": "MISSING", "details": "No GSTIN provided by bidder"},
                    error_message="GSTIN is missing"
                )
            
            # Synthetic check for mismatch keyword
            if "INVALID" in identity.gstin.upper() or "EXPIRED" in identity.gstin.upper():
                return VerificationResponse(
                    source_name=self.source_name,
                    source_type=self.source_type,
                    verified=False,
                    data={"gstin": identity.gstin, "status": "INACTIVE", "filing_status": "PENDING_6_MONTHS"},
                    error_message="GSTIN registration is inactive or default in filing"
                )

            return VerificationResponse(
                source_name=self.source_name,
                source_type=self.source_type,
                verified=True,
                data={
                    "gstin": identity.gstin,
                    "legal_name": identity.legal_name,
                    "status": "ACTIVE",
                    "filing_status": "REGULAR"
                }
            )

        elif claim_type == "MSME_REGISTRATION":
            if not identity.udyam_number:
                return VerificationResponse(
                    source_name=self.source_name,
                    source_type=self.source_type,
                    verified=False,
                    data={"status": "MISSING", "details": "No Udyam Registration Number provided"},
                    error_message="Udyam Number is missing"
                )

            return VerificationResponse(
                source_name=self.source_name,
                source_type=self.source_type,
                verified=True,
                data={
                    "udyam_number": identity.udyam_number,
                    "enterprise_type": "MICRO",
                    "major_activity": "MANUFACTURING",
                    "valid_until": "PERPETUAL"
                }
            )

        elif claim_type == "DEBARMENT_CHECK":
            # Synthetic blacklist check
            is_blacklisted = "DEBARRED" in identity.legal_name.upper() or "BLACKLIST" in identity.legal_name.upper()
            return VerificationResponse(
                source_name=self.source_name,
                source_type=self.source_type,
                verified=not is_blacklisted,
                data={
                    "debarred": is_blacklisted,
                    "matched_entity": identity.legal_name if is_blacklisted else None,
                    "source_portal": "CPCL / CPPP Central Debarment Database"
                },
                error_message="Entity is debarred/blacklisted from government procurement" if is_blacklisted else None
            )

        # Default fallback response for other claims
        return VerificationResponse(
            source_name=self.source_name,
            source_type=self.source_type,
            verified=True,
            data={"claim": claim.dict(), "status": "VERIFIED_DEFAULT"}
        )
