from app.connectors.base import (
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
        source_type=SourceType.LICENSED_SANDBOX
    )

    identity = BidderIdentity(
        bidder_id=1,
        legal_name="Apex Safety Corp",
        gstin="33ABCDE1234F1Z5"
    )

    claim = VerificationClaim(
        requirement_code="REQ-GST-01",
        claim_type="GST_FILING"
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
        gstin=None
    )

    claim = VerificationClaim(
        requirement_code="REQ-GST-01",
        claim_type="GST_FILING"
    )

    res = connector.verify(identity, claim)

    assert res.verified is False
    assert res.data["status"] == "MISSING"
    assert "missing" in res.error_message.lower()


def test_mock_connector_oem_missing():
    connector = MockVerificationConnector()

    identity = BidderIdentity(
        bidder_id=3,
        legal_name="VENDHAR INDUSTRIES"
    )

    claim = VerificationClaim(
        requirement_code="REQ-OEM-AUTH-01",
        claim_type="OEM_AUTHORIZATION"
    )

    res = connector.verify(identity, claim)

    assert res.verified is False
    assert res.data["status"] == "MISSING"
    assert "OEM" in res.error_message.upper()


def test_mock_connector_bis_expired():
    connector = MockVerificationConnector()

    identity = BidderIdentity(
        bidder_id=4,
        legal_name="ANBU INDUSTRIES"
    )

    claim = VerificationClaim(
        requirement_code="REQ-BIS-CERT-01",
        claim_type="BIS_CERTIFICATION"
    )

    res = connector.verify(identity, claim)

    assert res.verified is False
    assert res.data["status"] == "EXPIRED"
    assert "expired" in res.error_message.lower()


def test_mock_connector_gst_mismatch():
    connector = MockVerificationConnector()

    identity = BidderIdentity(
        bidder_id=5,
        legal_name="KAVERI INDUSTRIES",
        gstin="INVALID-GSTIN"
    )

    claim = VerificationClaim(
        requirement_code="REQ-GST-01",
        claim_type="GST_FILING"
    )

    res = connector.verify(identity, claim)

    assert res.verified is False
    assert res.data["status"] == "MISMATCH"
    assert "mismatch" in res.error_message.lower()