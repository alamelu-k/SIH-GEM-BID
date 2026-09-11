from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import tenders, bidders, compliance, audit

# Create database tables automatically on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## CodeVeil - SIH26100 Backend Platform (Pod 2 - Alamelu)
    
    Integrated Bid Compliance Verification Platform for GeM Procurement.
    
    ### Key Features:
    - **PostgreSQL / SQLite Storage**: Full database model tracking Tenders, Requirements, Bidders, Documents, Verification Results, Compliance Matrix, and Audit Trail.
    - **Deterministic Rules Engine**: Pure data-driven evaluator returning `PASS`, `FAIL`, `MISSING`, `MISMATCH`, and `MANUAL_REVIEW`.
    - **Pluggable Verification Connectors**: Abstract connector interface with `source_type` (`official`, `licensed_sandbox`, `synthetic`) for GST, Udyam, DigiLocker, and Debarment APIs.
    - **Append-only Audit Trail**: Transparent logging of every check and procurement officer action.
    """,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS middleware for Pod 3 React Frontend Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local dev / demo deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers under /api/v1
app.include_router(tenders.router, prefix=settings.API_V1_STR)
app.include_router(bidders.router, prefix=settings.API_V1_STR)
app.include_router(compliance.router, prefix=settings.API_V1_STR)
app.include_router(audit.router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Health Check"])
def root():
    """
    Root endpoint verifying CodeVeil backend operation.
    """
    return {
        "status": "online",
        "system": "CodeVeil - SIH26100 Verification Platform",
        "pod": "Pod 2 - Backend & Rules Engine",
        "lead": "Alamelu",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }
