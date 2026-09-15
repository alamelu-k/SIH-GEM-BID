"""
Migration script to encrypt existing Bidder PAN and GSTIN columns in place.
Steps:
1. Ensure DB column length is widened to VARCHAR(255) for Fernet tokens.
2. Read all existing bidder rows and their current plaintext values.
3. Encrypt 'pan' and 'gstin' in place using app.encryption.encrypt_field().
4. Commit changes to the database.
5. Re-fetch all rows from the database and verify that decrypt_field() returns
   the exact original plaintext values.
6. Print row-by-row PASS/FAIL results.
"""
import os
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from sqlalchemy import text
from app.database import engine, SessionLocal
from app import models
from app.encryption import encrypt_field, decrypt_field


def ensure_column_widths():
    """Ensure Postgres columns are VARCHAR(255) to hold Fernet ciphertexts."""
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE bidders ALTER COLUMN pan TYPE VARCHAR(255);"))
        conn.execute(text("ALTER TABLE bidders ALTER COLUMN gstin TYPE VARCHAR(255);"))


def main():
    print("=" * 90)
    print("STEP 1: Checking and widening database column widths to VARCHAR(255)...")
    ensure_column_widths()
    print("Column widths verified/updated.")

    db = SessionLocal()
    try:
        print("\nSTEP 2: Reading existing bidder rows...")
        bidders = db.query(models.Bidder).order_by(models.Bidder.id).all()
        total = len(bidders)
        print(f"Total rows found: {total}")

        # Record original values for verification
        original_data = {}
        for b in bidders:
            original_data[b.id] = {
                "legal_name": b.legal_name,
                "pan": b.pan,
                "gstin": b.gstin,
            }

        print("\nSTEP 3: Encrypting PAN and GSTIN in place using encrypt_field()...")
        for b in bidders:
            if b.pan:
                b.pan = encrypt_field(b.pan)
            if b.gstin:
                b.gstin = encrypt_field(b.gstin)

        db.commit()
        print("Commit successful. All rows updated.")

        print("\nSTEP 4: Running verification pass (row-by-row)...")
        print("=" * 90)
        print(f"{'ID':<4} | {'Legal Name':<28} | {'PAN Check':<10} | {'GSTIN Check':<10} | {'Status'}")
        print("-" * 90)

        # Fresh query to verify persisted data
        db.expire_all()
        updated_bidders = db.query(models.Bidder).order_by(models.Bidder.id).all()

        all_passed = True
        for b in updated_bidders:
            orig = original_data[b.id]
            decrypted_pan = decrypt_field(b.pan) if b.pan else None
            decrypted_gstin = decrypt_field(b.gstin) if b.gstin else None

            pan_match = (decrypted_pan == orig["pan"])
            gstin_match = (decrypted_gstin == orig["gstin"])
            row_pass = pan_match and gstin_match

            if not row_pass:
                all_passed = False

            name_trunc = (b.legal_name[:26] + "..") if len(b.legal_name) > 28 else b.legal_name
            status_str = "PASS" if row_pass else "FAIL"
            pan_status = "MATCH" if pan_match else "MISMATCH"
            gst_status = "MATCH" if gstin_match else "MISMATCH"

            print(f"{b.id:<4} | {name_trunc:<28} | {pan_status:<10} | {gst_status:<10} | {status_str}")

        print("=" * 90)
        if all_passed:
            print(f"OVERALL RESULT: ALL {total}/{total} ROWS VERIFIED SUCCESSFULLY (PASS)")
        else:
            print("OVERALL RESULT: VERIFICATION FAILED ON ONE OR MORE ROWS")
            sys.exit(1)

    finally:
        db.close()


if __name__ == "__main__":
    main()
