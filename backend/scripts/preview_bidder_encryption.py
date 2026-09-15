"""
Read-only migration preview script for existing bidder rows.
Detects whether PAN and GSTIN values are already Fernet-encrypted or still stored as plaintext.
Performs zero database modifications.
"""
import os
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from cryptography.fernet import Fernet, InvalidToken
from app.database import SessionLocal
from app import models
from app.config import settings

# Load encryption suite
key = os.environ.get("FIELD_ENCRYPTION_KEY")
if not key:
    print("ERROR: FIELD_ENCRYPTION_KEY is not set in environment.")
    sys.exit(1)

cipher = Fernet(key.encode("utf-8") if isinstance(key, str) else key)


def check_status(val: str | None) -> tuple[str, str]:
    if val is None:
        return "NULL", "-"
    val_str = str(val).strip()
    if not val_str:
        return "EMPTY", "-"
    try:
        decrypted = cipher.decrypt(val_str.encode("utf-8")).decode("utf-8")
        return "ENCRYPTED", f"{val_str[:15]}... (decrypts to {decrypted[:3]}***)"
    except (InvalidToken, Exception):
        return "PLAINTEXT", val_str


def main():
    db = SessionLocal()
    try:
        bidders = db.query(models.Bidder).order_by(models.Bidder.id).all()
        total = len(bidders)

        print("=" * 80)
        print("BIDDER FIELD-LEVEL ENCRYPTION MIGRATION PREVIEW (READ-ONLY)")
        print(f"Total Bidder Rows Found: {total}")
        print("=" * 80)
        print(f"{'ID':<4} | {'Legal Name':<30} | {'PAN Status':<12} | {'GSTIN Status':<12} | {'Details'}")
        print("-" * 80)

        pan_counts = {"PLAINTEXT": 0, "ENCRYPTED": 0, "NULL": 0, "EMPTY": 0}
        gst_counts = {"PLAINTEXT": 0, "ENCRYPTED": 0, "NULL": 0, "EMPTY": 0}

        for b in bidders:
            pan_status, pan_preview = check_status(b.pan)
            gst_status, gst_preview = check_status(b.gstin)

            pan_counts[pan_status] = pan_counts.get(pan_status, 0) + 1
            gst_counts[gst_status] = gst_counts.get(gst_status, 0) + 1

            name_trunc = (b.legal_name[:28] + "..") if len(b.legal_name) > 30 else b.legal_name
            print(f"{b.id:<4} | {name_trunc:<30} | {pan_status:<12} | {gst_status:<12} | PAN: {pan_preview} | GSTIN: {gst_preview}")

        print("=" * 80)
        print("SUMMARY:")
        print(f"  PAN:   {pan_counts.get('PLAINTEXT', 0)} Plaintext, {pan_counts.get('ENCRYPTED', 0)} Encrypted, {pan_counts.get('NULL', 0)} Null/Empty")
        print(f"  GSTIN: {gst_counts.get('PLAINTEXT', 0)} Plaintext, {gst_counts.get('ENCRYPTED', 0)} Encrypted, {gst_counts.get('NULL', 0)} Null/Empty")
        print("  Database modifications: 0 (Strictly read-only inspection)")
        print("=" * 80)
    finally:
        db.close()


if __name__ == "__main__":
    main()
