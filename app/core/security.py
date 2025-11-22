import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from typing import Optional
from app.core.config import settings


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plaintext password against a bcrypt hash produced by get_password_hash."""
    if not isinstance(plain, str):
        plain = str(plain)
    plain_b = plain.encode("utf-8")
    try:
        return bcrypt.checkpw(plain_b, hashed.encode("utf-8"))
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt (returns utf-8 decoded string)."""
    if not isinstance(password, str):
        password = str(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise
