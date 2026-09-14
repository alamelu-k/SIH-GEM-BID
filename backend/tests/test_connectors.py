from app.connectors.base import (
    VerificationConnector,
    VerificationResponse,
    SourceType,
    BidderIdentity,
    VerificationClaim,
)
from app.connectors.mock_connector import MockVerificationConnector


def test_connector_source_type_enum():
    assert SourceType.OFFICIAL.value == "official"
    assert SourceType.LICENSED_SANDBOX.value == "licensed_sandbox"
    assert SourceType.SYNTHETIC.value == "synthetic"


def test_mock_connector_gst_verification():
    connector = MockVerificationConnector(
        source_name="Test GST API",
        source_type=SourceType.LICENSED_SANDBOX,
    )

    identity = BidderIdentity(
        bidder_id=1,
        legal_name="Apex Safety Corp",
        gstin="33ABCDE1234F1Z5",
    )

    claim = VerificationClaim(
        requirement_code="REQ-GST-01",
        claim_type="GST_FILING",
    )

    res = connector.verify(identity, claim)

    assert isinstance(res, VerificationResponse)
    assert res.source_name == "Test GST API"
    assert res.source_type == SourceType.LICENSED_SANDBOX
    assert res.verified is True
    assert res.data["status"] == "ACTIVE"


def test_mock_connector_missing_gstin():
    connector = MockVerificationConnector()

    identity = BidderIdentity(
        bidder_id=2,
        legal_name="Missing GST Ltd",
        gstin=None,
    )

    claim = VerificationClaim(
        requirement_code="REQ-GST-01",
        claim_type="GST_FILING",
    )

    res = connector.verify(identity, claim)

    assert res.verified is False
    assert res.data["status"] == "MISSING"
    assert "missing" in res.error_message.lower()


# =========================================================
# Bug 2: Identity mismatch verification tests
# =========================================================

def test_mock_connector_gst_identity_mismatch():
    connector = MockVerificationConnector()

    identity = BidderIdentity(
        bidder_id=3,
        legal_name="Kaveri PPE Traders",
        gstin="33KAVERI1234F1Z5",
    )

    claim = VerificationClaim(
        requirement_code="REQ-GST-01",
        claim_type="GST_FILING",
    )

    res = connector.verify(identity, claim)

    assert res.verified is False
    assert res.data["status"] == "MISMATCH"
    assert res.data["legal_name_match"] is False


def test_mock_connector_pan_identity_mismatch():
    connector = MockVerificationConnector()

    identity = BidderIdentity(
        bidder_id=4,
        legal_name="Muruga Technical Services",
        pan="ABCDE1234F",
    )

    claim = VerificationClaim(
        requirement_code="REQ-PAN-01",
        claim_type="PAN_VERIFICATION",
    )

    res = connector.verify(identity, claim)

    assert res.verified is False
    assert res.data["status"] == "MISMATCH"
    assert res.data["legal_name_match"] is False


def test_mock_connector_udyam_identity_mismatch():
    connector = MockVerificationConnector()

    identity = BidderIdentity(
        bidder_id=5,
        legal_name="Lakshmi Office Interiors",
        udyam_number="UDYAM-TN-00-1234567",
    )

    claim = VerificationClaim(
        requirement_code="REQ-UDYAM-01",
        claim_type="MSME_REGISTRATION",
    )

    res = connector.verify(identity, claim)

    assert res.verified is False
    assert res.data["status"] == "MISMATCH"
    assert res.data["legal_name_match"] is False