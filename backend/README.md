# CodeVeil — Pod 2: Backend & Rules Engine Guide

> **Author / Lead**: Alamelu  
> **Project**: CodeVeil — SIH26100 (CPCL / Ministry of Petroleum & Natural Gas)  
> **Tech Stack**: Python, FastAPI, SQLAlchemy 2.0, Pydantic v2, Pytest, SQLite / PostgreSQL  

---

## 📚 Overview for Alamelu

Welcome to your complete, production-grade backend! As the Pod 2 lead, you own:
1. **Database Schema & ORM Models** (`app/models.py`)
2. **Pluggable Verification Connector Interface** (`app/connectors/base.py`)
3. **Deterministic Rules Engine** (`app/rules_engine/`)
4. **FastAPI REST API Routes** (`app/routers/`)

This guide explains **what each file does**, **why it is built this way**, and **how to explain it during jury evaluation**.

---

## 🏗️ Architecture & Component Breakdown

```
backend/
├── app/
│   ├── main.py                  # FastAPI Application Entrypoint & CORS configuration
│   ├── config.py                # App settings & SQLite / PostgreSQL connection string
│   ├── database.py              # SQLAlchemy DB Engine & Session Provider (get_db)
│   ├── models.py                # Database tables: Tender, Requirement, Bidder, Document, etc.
│   ├── schemas.py               # Pydantic data validation schemas for Requests & Responses
│   ├── connectors/
│   │   ├── base.py              # VerificationConnector abstract interface & SourceType enum
│   │   └── mock_connector.py    # Demonstration connector implementation
│   ├── rules_engine/
│   │   ├── types.py             # Rule states: PASS, FAIL, MISSING, MISMATCH, MANUAL_REVIEW
│   │   ├── rules.py             # Deterministic rule evaluators
│   │   └── engine.py            # RulesEngine orchestrator
│   └── routers/
│       ├── tenders.py           # /api/v1/tenders (Ingest tender PDFs & list requirements)
│       ├── bidders.py           # /api/v1/bidders (Bidder registration & document upload)
│       ├── compliance.py        # /api/v1/compliance (Run rules engine & get matrix)
│       └── audit.py             # /api/v1/audit (Append-only audit trail logging)
├── tests/
│   ├── test_rules_engine.py     # Unit tests for rule evaluations
│   ├── test_connectors.py       # Unit tests for connector contracts
│   └── test_api.py              # Integration tests for FastAPI endpoints
└── requirements.txt             # Python dependencies
```

---

## 🔑 Key Concepts to Understand

### 1. Database Schema (`app/models.py`)
- **`Tender`**: Stores tender details and extracted requirement clauses.
- **`Requirement`**: Specific requirements extracted from the tender PDF (e.g. `REQ-GST-01`, mandatory flag, clause ref, page number).
- **`Bidder`**: Vendor submitting a bid (Legal Name, PAN, GSTIN, Udyam Number).
- **`Document`**: Submitted documents (GST cert, financial statement, Udyam cert).
- **`VerificationResult`**: Raw verification data returned from connectors (GST, Udyam, Debarment list).
- **`ComplianceScore`**: The evaluated outcome matrix (Passed count, Failed count, Missing count, Overall Status).
- **`AuditLog`**: Append-only log tracking every action for transparency.

### 2. Honest Verification Connectors (`app/connectors/base.py`)
To prevent "fake demo" criticisms from judges, we explicitly tag every verification source with `source_type`:
- `OFFICIAL`: Direct government portal API (e.g. GSTN)
- `LICENSED_SANDBOX`: Authorized third-party sandbox (e.g. Surepass/Setu)
- `SYNTHETIC`: Local mock data provider

All connectors implement:
```python
def verify(self, identity: BidderIdentity, claim: VerificationClaim) -> VerificationResponse:
```

### 3. Deterministic Rules Engine (`app/rules_engine/`)
> 💡 **Pitch Point for Jury**: *"LLMs extract tender clauses, but an LLM NEVER makes compliance decisions. Our deterministic rules engine evaluates compliance using strict, auditable data rules."*

It evaluates 5 possible result states:
- **`PASS`**: Requirement verified and satisfied.
- **`FAIL`**: Disqualification factor (e.g. Debarred, expired GST).
- **`MISSING`**: Document or source response not provided.
- **`MISMATCH`**: Extracted document field contradicts official registry (e.g. legal name mismatch).
- **`MANUAL_REVIEW`**: Needs procurement officer human judgment.

---

## 🚀 How to Run the Backend Locally

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the FastAPI Development Server
```bash
uvicorn app.main:app --reload --port 8000
```

Open your browser to **`http://localhost:8000/docs`** to see the interactive OpenAPI documentation!

### 3. Run Automated Tests
```bash
pytest tests/
```

---

## 🤝 How Teammates Integrate with Your Code

- **Akhshaya (Pod 1 Lead)**: Uses `/api/v1/tenders` and `/api/v1/bidders` to seed tender scenarios and 15 bidder cases.
- **Agnes & Anupriya (Pod 3 Frontend)**: Call `/api/v1/compliance/bidder/{bidder_id}` to display the Requirement Matrix and Officer Decision views in React. CORS is already configured!
- **Sadhana & Gayatri (Pod 4 AI/ML)**: Implement custom classes inheriting from `VerificationConnector` in `app/connectors/` to connect their real sandbox or mock APIs seamlessly.
