import os
from datetime import datetime, timedelta
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.auth import (
    verify_password,
    create_access_token,
    generate_otp,
    send_otp_email,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Rate limiter instance using client IP
limiter = Limiter(key_func=get_remote_address)


# --- CAPTCHA Verification Helper ---
def verify_captcha(captcha_token: str, remote_ip: Optional[str] = None) -> bool:
    """
    Verify CAPTCHA token against hCaptcha verification endpoint (https://api.hcaptcha.com/siteverify).
    
    Selected Provider: hCaptcha
    Rationale:
    1. Privacy-centric: Fully GDPR compliant and does not track or profile users across the web.
    2. Deterministic: Clear binary validation (success: true/false) rather than opaque heuristic risk
       scores (like reCAPTCHA v3) that risk falsely blocking authorized procurement officers.
    """
    # Gated bypass strictly for local automated testing / dev when explicitly enabled
    if os.environ.get("DISABLE_CAPTCHA_FOR_TESTS", "").lower() in ("true", "1", "yes"):
        return True

    secret_key = os.environ.get("HCAPTCHA_SECRET_KEY")
    if not secret_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="HCAPTCHA_SECRET_KEY is not configured on the server",
        )

    try:
        data = {
            "secret": secret_key,
            "response": captcha_token,
        }
        if remote_ip:
            data["remoteip"] = remote_ip
        with httpx.Client(timeout=5.0) as client:
            resp = client.post("https://api.hcaptcha.com/siteverify", data=data)
            result = resp.json()
            return bool(result.get("success", False))
    except HTTPException:
        raise
    except Exception:
        return False


# --- Schemas ---
class LoginRequest(BaseModel):
    email: str
    password: str
    captcha_token: Optional[str] = None


class VerifyOTPRequest(BaseModel):
    email: str
    otp: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Note: Officer account creation will be addressed with RBAC in step 3.


# --- Endpoints ---
@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, req: LoginRequest, db: Session = Depends(get_db)):
    """
    Accepts email + password + captcha_token, verifies CAPTCHA first,
    verifies password hash, generates OTP, saves otp_code + otp_expires_at (now + 5 minutes),
    sends OTP email, and returns a generic 'OTP sent' response (no JWT at this step).
    Rate limit: 5 requests per minute.
    """
    if not req.captcha_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CAPTCHA token is required",
        )

    client_ip = request.client.host if request.client else None
    if not verify_captcha(req.captcha_token, remote_ip=client_ip):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CAPTCHA verification failed",
        )

    officer = db.query(models.Officer).filter(models.Officer.email == req.email).first()
    if not officer or not officer.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(req.password, officer.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    otp = generate_otp()
    officer.otp_code = otp
    officer.otp_expires_at = datetime.utcnow() + timedelta(minutes=5)
    db.commit()

    try:
        send_otp_email(officer.email, otp)
    except Exception:
        pass

    return {"message": "OTP sent", "email": officer.email}


@router.post("/verify-otp", response_model=TokenResponse)
@limiter.limit("3/minute")
def verify_otp(request: Request, req: VerifyOTPRequest, db: Session = Depends(get_db)):
    """
    Accepts email + otp, checks otp_code matches AND otp_expires_at hasn't passed,
    clears the OTP fields on success, issues and returns a JWT access token.
    Rate limit: 3 requests per minute (stricter to prevent brute-force attacks on OTPs).
    """
    officer = db.query(models.Officer).filter(models.Officer.email == req.email).first()
    if not officer or not officer.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request",
        )

    if not officer.otp_code or officer.otp_code != req.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP code",
        )

    if not officer.otp_expires_at or datetime.utcnow() > officer.otp_expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP code has expired",
        )

    # Clear OTP fields on successful verification
    officer.otp_code = None
    officer.otp_expires_at = None
    db.commit()

    # Issue JWT access token
    access_token = create_access_token(
        data={"sub": officer.email, "role": officer.role, "officer_id": officer.id}
    )

    return TokenResponse(access_token=access_token, token_type="bearer")
