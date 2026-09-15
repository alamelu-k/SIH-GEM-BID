import os
from typing import Optional
from cryptography.fernet import Fernet, InvalidToken
from app.config import settings  # Ensures .env is loaded before accessing env vars

# Read encryption key from environment variable
_KEY = os.environ.get("FIELD_ENCRYPTION_KEY")
if not _KEY:
    raise RuntimeError(
        "FIELD_ENCRYPTION_KEY environment variable is missing. "
        "Server startup aborted to prevent unencrypted plaintext storage of sensitive fields."
    )

try:
    _cipher_suite = Fernet(_KEY.encode("utf-8") if isinstance(_KEY, str) else _KEY)
except Exception as exc:
    raise RuntimeError(
        f"Invalid FIELD_ENCRYPTION_KEY: {exc}. Must be a valid 32-byte URL-safe base64-encoded key."
    ) from exc


def encrypt_field(plaintext: Optional[str]) -> Optional[str]:
    """
    Encrypt a plaintext string field (e.g. PAN, GSTIN) using Fernet.
    Returns URL-safe base64-encoded ciphertext string.
    """
    if plaintext is None:
        return None
    token = _cipher_suite.encrypt(plaintext.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_field(ciphertext: Optional[str]) -> Optional[str]:
    """
    Decrypt a Fernet ciphertext token back to plaintext string.
    Raises InvalidToken / ValueError if ciphertext cannot be decrypted.
    """
    if ciphertext is None:
        return None
    return _cipher_suite.decrypt(ciphertext.encode("utf-8")).decode("utf-8")
