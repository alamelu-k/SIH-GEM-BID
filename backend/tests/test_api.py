import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_health_check():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "Alamelu" in data["lead"]

def test_tender_creation_and_listing():
    unique_num = f"CPCL-SAFETY-2026-{uuid.uuid4().hex[:6]}"
    tender_payload = {
        "tender_number": unique_num,
        "title": "Procurement of Industrial Safety Equipment",
        "issuing_authority": "CPCL / MoPNG",
        "category": "Industrial Safety Equipment",
        "requirements": [
            {
                "code": "REQ-GST-01",
                "title": "GST Registration & Regular Filing",
                "mandatory": True,
                "source_clause": "Clause 3.1",
                "source_page": 2
            },
            {
                "code": "REQ-DEBAR-01",
                "title": "Central Debarment & Blacklist Check",
                "mandatory": True,
                "source_clause": "Clause 7.4",
                "source_page": 5
            }
        ]
    }

    
    # Create Tender
    res = client.post("/api/v1/tenders", json=tender_payload)
    assert res.status_code == 201
    created_tender = res.json()
    assert created_tender["tender_number"] == unique_num
    assert len(created_tender["requirements"]) == 2
    tender_id = created_tender["id"]
    
    # List Tenders
    list_res = client.get("/api/v1/tenders")
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # Create Bidder
    bidder_payload = {
        "tender_id": tender_id,
        "legal_name": "Apex Safety Solutions Pvt Ltd",
        "pan": "AAACA1234A",
        "gstin": "33AAACA1234A1Z5",
        "udyam_number": "UDYAM-TN-01-0001234"
    }
    bidder_res = client.post("/api/v1/bidders", json=bidder_payload)
    assert bidder_res.status_code == 201
    bidder = bidder_res.json()
    bidder_id = bidder["id"]

    # Upload Document
    doc_payload = {
        "document_type": "GST_CERTIFICATE",
        "file_name": "apex_gst_cert.pdf",
        "file_path": "/uploads/apex_gst_cert.pdf"
    }
    doc_res = client.post(f"/api/v1/bidders/{bidder_id}/documents", json=doc_payload)
    assert doc_res.status_code == 201

    # Evaluate Compliance
    eval_res = client.post(f"/api/v1/compliance/evaluate/{bidder_id}")
    assert eval_res.status_code == 200
    compliance_score = eval_res.json()
    assert compliance_score["overall_status"] == "PASS"
    assert compliance_score["passed_count"] == 2

    # Verify Audit Trail
    audit_res = client.get(f"/api/v1/audit?entity_id={tender_id}")
    assert audit_res.status_code == 200
    assert len(audit_res.json()) >= 1
