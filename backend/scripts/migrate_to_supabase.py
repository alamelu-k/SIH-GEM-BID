#!/usr/bin/env python3
"""
Standalone Migration Script: SQLite (codeveil.db) -> Supabase (PostgreSQL)

This script:
1. Connects to SQLite (SOURCE) and Supabase PostgreSQL (DEST) as separate engines.
2. Creates all tables on Supabase using SQLAlchemy Base.metadata.create_all().
3. Copies table rows in strict foreign-key dependency order, preserving primary keys.
4. Updates PostgreSQL auto-increment sequence counters (setval) to max(id).
5. Compares row counts between SOURCE and DEST, reporting MATCH / MISMATCH.
6. Safe to re-run: skips row insertion if a destination table already contains records.
"""

import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Ensure backend root is on sys.path to import app models
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.models import (
    Base,
    Tender,
    Requirement,
    Bidder,
    Document,
    VerificationResult,
    ComplianceScore,
    AuditLog,
)

# Ordered list respecting foreign-key hierarchy
TABLES_IN_ORDER = [
    ("tenders", Tender),
    ("requirements", Requirement),
    ("bidders", Bidder),
    ("documents", Document),
    ("verification_results", VerificationResult),
    ("compliance_scores", ComplianceScore),
    ("audit_logs", AuditLog),
]


def load_dest_url_from_env() -> str:
    """Read DATABASE_URL from backend/.env or parent .env without altering app config."""
    env_paths = [
        backend_dir / ".env",
        backend_dir.parent / ".env",
        backend_dir.parent.parent / "sadhana-ml" / ".env",
    ]
    for env_path in env_paths:
        if env_path.exists():
            content = env_path.read_text(encoding="utf-8")
            match = re.search(r"^\s*DATABASE_URL\s*=\s*(.+)$", content, re.MULTILINE)
            if match:
                raw_url = match.group(1).strip().strip('"\'')
                # SQLAlchemy 2.0 requires postgresql:// rather than postgres://
                if raw_url.startswith("postgres://"):
                    raw_url = "postgresql://" + raw_url[len("postgres://"):]
                return raw_url

    raise ValueError(f"Could not find DATABASE_URL in any of: {env_paths}")


def get_source_sqlite_url() -> str:
    """Resolve absolute path to local SQLite codeveil.db."""
    sqlite_path = backend_dir / "codeveil.db"
    if not sqlite_path.exists():
        raise FileNotFoundError(f"Source SQLite database not found at: {sqlite_path}")
    return f"sqlite:///{sqlite_path.as_posix()}"


def main():
    print("=" * 75)
    print("CODEVEIL DATABASE MIGRATION: SQLite -> Supabase (PostgreSQL)")
    print("=" * 75)

    source_url = get_source_sqlite_url()
    dest_url = load_dest_url_from_env()

    dest_parsed = urlparse(dest_url)
    print(f"Source Database     : SQLite ({backend_dir / 'codeveil.db'})")
    print(f"Destination Host    : {dest_parsed.hostname}:{dest_parsed.port or 5432}")
    print(f"Destination DB      : {dest_parsed.path.lstrip('/')}")
    print("-" * 75)

    # 1. Initialize engines and sessions
    source_engine = create_engine(source_url, connect_args={"check_same_thread": False})
    dest_engine = create_engine(dest_url)

    SourceSession = sessionmaker(bind=source_engine)
    DestSession = sessionmaker(bind=dest_engine)

    source_session = SourceSession()
    dest_session = DestSession()

    # 2. Create tables on destination
    print("\n[Step 1] Ensuring schema and tables exist on Supabase destination...")
    Base.metadata.create_all(bind=dest_engine)
    print("  -> Schema check/creation complete.")

    # 3. Migrate data table by table
    print("\n[Step 2] Migrating rows in foreign-key dependency order...")
    migration_summary = []

    try:
        for table_name, model_cls in TABLES_IN_ORDER:
            source_count = source_session.query(model_cls).count()
            dest_count = dest_session.query(model_cls).count()

            print(f"\nProcessing '{table_name}':")
            print(f"  Source count: {source_count} | Existing destination count: {dest_count}")

            if dest_count > 0:
                print(f"  [SKIPPED] Table already contains {dest_count} records. Skipping insert to prevent duplicates.")
            elif source_count == 0:
                print(f"  [EMPTY] Source table has 0 records. Nothing to copy.")
            else:
                # Fetch all rows ordered by PK
                source_rows = source_session.query(model_cls).order_by(model_cls.id).all()
                columns = [c.name for c in model_cls.__table__.columns]

                row_dicts = []
                for row in source_rows:
                    row_data = {col: getattr(row, col) for col in columns}
                    row_dicts.append(row_data)

                # Bulk insert preserving original IDs
                dest_session.execute(model_cls.__table__.insert(), row_dicts)
                dest_session.commit()
                print(f"  [COPIED] Successfully inserted {len(row_dicts)} rows with original IDs.")

            # 4. Re-sync Postgres primary key auto-increment sequence (setval)
            try:
                dest_session.execute(text(f"""
                    SELECT setval(
                        pg_get_serial_sequence('{table_name}', 'id'),
                        COALESCE((SELECT MAX(id) FROM {table_name}), 1),
                        (SELECT MAX(id) FROM {table_name}) IS NOT NULL
                    );
                """))
                dest_session.commit()
                print(f"  [SEQUENCE] Updated Postgres sequence for '{table_name}'.")
            except Exception as seq_err:
                dest_session.rollback()
                print(f"  [SEQUENCE NOTICE] Could not set sequence for '{table_name}': {seq_err}")

            # Re-read counts for final report
            final_src = source_session.query(model_cls).count()
            final_dst = dest_session.query(model_cls).count()
            status = "MATCH" if final_src == final_dst else "MISMATCH"
            migration_summary.append((table_name, final_src, final_dst, status))

    finally:
        source_session.close()
        dest_session.close()

    # 5. Final Report
    print("\n" + "=" * 75)
    print("MIGRATION VERIFICATION REPORT")
    print("=" * 75)
    header = f"{'Table Name':<25} | {'Source (SQLite)':<15} | {'Dest (Supabase)':<15} | {'Status'}"
    print(header)
    print("-" * 75)
    all_match = True
    for t_name, src_c, dst_c, st in migration_summary:
        if st != "MATCH":
            all_match = False
        print(f"{t_name:<25} | {src_c:<15} | {dst_c:<15} | {st}")
    print("=" * 75)

    if all_match:
        print("RESULT: ALL TABLES SYNCHRONIZED SUCCESSFULLY (100% MATCH)\n")
    else:
        print("RESULT: ONE OR MORE TABLES REPORT A ROW COUNT MISMATCH\n")


if __name__ == "__main__":
    main()
