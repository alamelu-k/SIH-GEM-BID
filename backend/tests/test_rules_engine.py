from app.rules_engine.types import RuleResultState, RuleSeverity
from app.rules_engine.rules import RuleEvaluator
from app.rules_engine.engine import RulesEngine

class DummyObject:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_mandatory_document_rule_pass():
    res = RuleEvaluator.evaluate_mandatory_document(
        requirement_id=1,
        rule_code="REQ-DOC-01",
        title="Upload GST Certificate",
        mandatory=True,
        has_document=True,
        doc_name="gst_certificate.pdf"
    )
    assert res.status == RuleResultState.PASS
    assert res.severity == RuleSeverity.INFO
    assert "uploaded successfully" in res.reason

def test_mandatory_document_rule_missing():
    res = RuleEvaluator.evaluate_mandatory_document(
        requirement_id=2,
        rule_code="REQ-DOC-02",
        title="Upload Financial Statement",
        mandatory=True,
        has_document=False
    )
    assert res.status == RuleResultState.MISSING
    assert res.severity == RuleSeverity.CRITICAL

def test_identity_mismatch_rule():
    res = RuleEvaluator.evaluate_identity_mismatch(
        requirement_id=3,
        rule_code="REQ-NAME-01",
        title="Legal Name Verification",
        mandatory=True,
        claimed_name="Alpha Safety Equipment Pvt Ltd",
        verified_name="Beta Trading Private Limited",
        source_name="GSTN Portal"
    )
    assert res.status == RuleResultState.MISMATCH
    assert res.severity == RuleSeverity.WARNING
    assert "Name Mismatch Detected" in res.reason

def test_debarment_rule_critical_fail():
    res = RuleEvaluator.evaluate_debarment(
        requirement_id=4,
        rule_code="REQ-DEBAR-01",
        title="Central Debarment Registry Check",
        mandatory=True,
        is_debarred=True,
        source_name="CPPP Central Blacklist"
    )
    assert res.status == RuleResultState.FAIL
    assert res.severity == RuleSeverity.CRITICAL
    assert "CRITICAL DISQUALIFICATION" in res.reason

def test_full_rules_engine_orchestration():
    engine = RulesEngine()
    
    requirements = [
        DummyObject(id=1, code="REQ-GST-01", title="Active GST", mandatory=True, source_clause="4.1", source_page=2),
        DummyObject(id=2, code="REQ-DEBAR-01", title="Debarment Check", mandatory=True, source_clause="4.5", source_page=3)
    ]
    
    bidder = DummyObject(id=10, legal_name="Apex Safety Corp", gstin="33AAAAA0000A1Z5")
    documents = [DummyObject(id=100, document_type="GST_CERTIFICATE", file_name="gst.pdf")]
    
    v_results = [
        DummyObject(
            requirement_id=1, 
            source_name="GSTN Portal API", 
            source_type="licensed_sandbox", 
            raw_response={"status": "ACTIVE", "gstin": "33AAAAA0000A1Z5", "verified": True}
        ),
        DummyObject(
            requirement_id=2, 
            source_name="Central Debarment Registry", 
            source_type="synthetic", 
            raw_response={"debarred": False}
        )
    ]
    
    status_verdict, counts, matrix = engine.evaluate_bidder_compliance(
        requirements=requirements,
        bidder=bidder,
        documents=documents,
        verification_results=v_results
    )
    
    assert status_verdict == "PASS"
    assert counts["passed_count"] == 2
    assert counts["failed_count"] == 0
    assert len(matrix) == 2
