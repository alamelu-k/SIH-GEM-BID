import os
import secrets
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate bcrypt hash from plain password."""
    return pwd_context.hash(password)


# JWT helpers
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    Reads SECRET_KEY and ALGORITHM from environment variables.
    Always includes an exp claim (defaults to ACCESS_TOKEN_EXPIRE_MINUTES or 30 minutes).
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire_minutes = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES") or 30)
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    secret_key = os.environ.get("SECRET_KEY", "")
    algorithm = os.environ.get("ALGORITHM", "HS256")
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and validate a JWT access token.
    Reads SECRET_KEY and ALGORITHM from environment variables.
    """
    secret_key = os.environ.get("SECRET_KEY", "")
    algorithm = os.environ.get("ALGORITHM", "HS256")
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError:
        return None


# 6-digit OTP generator (secrets module)
def generate_otp() -> str:
    """Generate a cryptographically secure 6-digit OTP."""
    return f"{secrets.randbelow(1_000_000):06d}"


# OTP email sender
def send_otp_email(to_email: str, otp_code: str) -> bool:
    """
    Send OTP code via SMTP using configuration from environment variables.
    Defaults to Gmail SMTP: smtp.gmail.com, port 587, TLS.
    """
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_password = os.environ.get("SMTP_APP_PASSWORD", "")

    if not smtp_user or not smtp_password:
        return False

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = "CodeVeil - Your One-Time Password (OTP)"

    body = (
        f"Your CodeVeil verification code is: {otp_code}\n\n"
        f"This code will expire in 5 minutes.\n"
        f"If you did not request this code, please ignore this email."
    )
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

    return True


# --- RBAC Dependencies ---
http_bearer = HTTPBearer(auto_error=False)


def get_current_officer(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
    db: Session = Depends(get_db),
) -> models.Officer:
    """
    Extract and validate JWT token from Authorization: Bearer <token> header.
    Returns the active authenticated Officer database model.
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email: Optional[str] = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload is missing subject identifier",
            headers={"WWW-Authenticate": "Bearer"},
        )

    officer = db.query(models.Officer).filter(models.Officer.email == email).first()
    if not officer or not officer.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Officer account not found or deactivated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return officer


def require_admin(
    current_officer: models.Officer = Depends(get_current_officer),
) -> models.Officer:
    """
    Enforce admin-only access control.
    Requires caller to be an authenticated active officer with role == 'admin'.
    """
    if current_officer.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation requires administrator privileges",
        )
    return current_officer

