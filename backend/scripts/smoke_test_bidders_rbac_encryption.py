"""
Live smoke test for Bidder endpoints, RBAC role gating, and field-level encryption.
Verifies:
1. Unauthenticated calls return 401.
2. Officer caller to list_bidders (admin-only) returns 403 Forbidden.
3. Admin caller to list_bidders returns 200 OK with all PAN/GSTIN values decrypted.
4. Officer caller to create_bidder returns 201 Created, stores ciphertext in DB, and returns decrypted plaintext.
5. Invalid ciphertext triggers InvalidToken/ValueError rather than silently passing through.
"""
import os
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from cryptography.fernet import InvalidToken
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app import models
from app.auth import create_access_token
from app.encryption import decrypt_field, encrypt_field

client = TestClient(app)


def setup_test_officers(db):
    """Ensure an admin officer and a regular officer exist in DB for authenticating."""
    admin = db.query(models.Officer).filter(models.Officer.email == "admin.smoke@cpcl.gov.in").first()
    if not admin:
        admin = models.Officer(
            email="admin.smoke@cpcl.gov.in",
            hashed_password="fake_hashed_pw",
            role="admin",
            is_active=True,
        )
        db.add(admin)

    officer = db.query(models.Officer).filter(models.Officer.email == "officer.smoke@cpcl.gov.in").first()
    if not officer:
        officer = models.Officer(
            email="officer.smoke@cpcl.gov.in",
            hashed_password="fake_hashed_pw",
            role="officer",
            is_active=True,
        )
        db.add(officer)

    db.commit()
    return admin, officer


def main():
    print("=" * 80)
    print("LIVE SMOKE TEST: BIDDERS RBAC & FIELD-LEVEL ENCRYPTION")
    print("=" * 80)

    db = SessionLocal()
    created_bidder_id = None
    try:
        # Step 1: Setup officers & JWT tokens
        admin_user, officer_user = setup_test_officers(db)
        admin_token = create_access_token({"sub": admin_user.email})
        officer_token = create_access_token({"sub": officer_user.email})

        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        officer_headers = {"Authorization": f"Bearer {officer_token}"}

        # Step 2: Unauthenticated check on list_bidders
        print("\n[TEST 1] GET /api/v1/bidders without Authorization header:")
        res = client.get("/api/v1/bidders")
        assert res.status_code == 401, f"Expected 401, got {res.status_code}"
        print(f"  -> PASS: Correctly rejected with 401 Unauthorized ({res.json().get('detail')})")

        # Step 3: Officer check on list_bidders (must be 403 Forbidden)
        print("\n[TEST 2] GET /api/v1/bidders with Officer role (Admin required):")
        res = client.get("/api/v1/bidders", headers=officer_headers)
        assert res.status_code == 403, f"Expected 403, got {res.status_code}"
        print(f"  -> PASS: Correctly rejected with 403 Forbidden ({res.json().get('detail')})")

        # Step 4: Admin check on list_bidders (must be 200 OK with decrypted fields)
        print("\n[TEST 3] GET /api/v1/bidders with Admin role:")
        res = client.get("/api/v1/bidders", headers=admin_headers)
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        bidders = res.json()
        print(f"  -> PASS: Returned 200 OK with {len(bidders)} bidders.")
        # Verify first 3 bidders decrypted
        for b in bidders[:3]:
            pan = b.get("pan")
            gstin = b.get("gstin")
            assert pan and len(pan) == 10 and not pan.startswith("gAAAAA"), f"PAN not decrypted: {pan}"
            assert gstin and len(gstin) == 15 and not gstin.startswith("gAAAAA"), f"GSTIN not decrypted: {gstin}"
            print(f"     Bidder #{b['id']} ({b['legal_name'][:20]}): PAN={pan}, GSTIN={gstin} (Successfully Decrypted)")

        # Step 5: Officer check on create_bidder
        print("\n[TEST 4] POST /api/v1/bidders as Officer:")
        # Find an existing tender
        tender = db.query(models.Tender).first()
        tender_id = tender.id if tender else 1
        new_bidder_payload = {
            "tender_id": tender_id,
            "legal_name": "Smoke Test Vendor Ltd",
            "pan": "AAACS8888S",
            "gstin": "33AAACS8888S1Z8",
            "udyam_number": "UDYAM-TN-01-0008888",
        }
        res = client.post("/api/v1/bidders", json=new_bidder_payload, headers=officer_headers)
        assert res.status_code == 201, f"Expected 201, got {res.status_code}: {res.text}"
        created = res.json()
        created_bidder_id = created["id"]
        print(f"  -> PASS: Created Bidder ID {created_bidder_id} (HTTP 201)")
        print(f"     Response PAN: {created['pan']} (Decrypted)")
        print(f"     Response GSTIN: {created['gstin']} (Decrypted)")
        assert created["pan"] == "AAACS8888S"
        assert created["gstin"] == "33AAACS8888S1Z8"

        # Verify DB directly stores ciphertext
        db.expire_all()
        db_row = db.query(models.Bidder).filter(models.Bidder.id == created_bidder_id).first()
        assert db_row.pan.startswith("gAAAAA"), f"DB PAN is not ciphertext: {db_row.pan}"
        assert db_row.gstin.startswith("gAAAAA"), f"DB GSTIN is not ciphertext: {db_row.gstin}"
        print(f"     Database Stored PAN:   {db_row.pan[:25]}... (Ciphertext Verified)")
        print(f"     Database Stored GSTIN: {db_row.gstin[:25]}... (Ciphertext Verified)")

        # Step 6: Verify bad ciphertext raises exception (fallback removed)
        print("\n[TEST 5] Corrupted ciphertext decrypt_field check:")
        corrupt_token = "gAAAAABqq_THIS_IS_CORRUPTED_CIPHERTEXT_GARBAGE="
        try:
            decrypt_field(corrupt_token)
            print("  -> FAIL: Corrupt ciphertext did NOT raise an exception!")
            sys.exit(1)
        except (InvalidToken, Exception) as exc:
            print(f"  -> PASS: Bad ciphertext correctly raised {type(exc).__name__}: {exc}")

        print("\n" + "=" * 80)
        print("ALL SMOKE TESTS PASSED SUCCESSFULLY!")
        print("=" * 80)

    finally:
        # Cleanup test bidder and officers by exact name to handle aborted runs
        test_bidders = db.query(models.Bidder).filter(
            models.Bidder.legal_name.in_(["Smoke Test Vendor Ltd", "Smoke Bidder Pvt Ltd"])
        ).all()
        for b in test_bidders:
            # Delete dependent rows to avoid ForeignKeyViolation
            db.query(models.Document).filter(models.Document.bidder_id == b.id).delete()
            db.query(models.VerificationResult).filter(models.VerificationResult.bidder_id == b.id).delete()
            db.query(models.ComplianceScore).filter(models.ComplianceScore.bidder_id == b.id).delete()
            db.query(models.AuditLog).filter(
                models.AuditLog.entity_id == b.id, models.AuditLog.entity_type == 'BIDDER'
            ).delete()
            db.query(models.Bidder).filter(models.Bidder.id == b.id).delete()

        db.query(models.Officer).filter(models.Officer.email.in_(["admin.smoke@cpcl.gov.in", "officer.smoke@cpcl.gov.in"])).delete()
        db.commit()
        db.close()


if __name__ == "__main__":
    main()
