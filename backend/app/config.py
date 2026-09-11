import os

class Settings:
    PROJECT_NAME: str = "CodeVeil - Integrated Bid Compliance Verification Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database setting: defaults to local SQLite file for zero-config demo/dev,
    # but seamlessly supports PostgreSQL when DATABASE_URL environment variable is set.
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./codeveil.db"
    )

settings = Settings()

