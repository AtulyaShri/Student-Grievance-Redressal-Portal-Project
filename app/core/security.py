import os
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import jwt

# Load from env when available; keep defaults for development.
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# import bcrypt
# from datetime import datetime, timedelta, timezone
# from jose import jwt, JWTError
# from typing import Optional
# from app.core.config import settings


# def get_password_hash(password: str) -> str:
#     """Hash a password using bcrypt (returns utf-8 decoded string)."""
#     if not isinstance(password, str):
#         password = str(password)
#     salt = bcrypt.gensalt()
#     hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
#     return hashed.decode("utf-8")


# def verify_password(plain: str, hashed: str) -> bool:
#     if not isinstance(plain, str):
#         plain = str(plain)
#     try:
#         return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
#     except Exception:
#         return False


# # def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
# #     to_encode = data.copy()
# #     expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
# #     to_encode.update({"exp": expire})
# #     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
# #     return encoded_jwt


# def decode_token(token: str) -> dict:
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         return payload
#     except JWTError:
#         raise
