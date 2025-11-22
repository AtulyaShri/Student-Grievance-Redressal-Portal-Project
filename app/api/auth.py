from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Temporary in-memory 'DB' for demo; replace with real DB session logic.
_users = {}
_next_id = 1

# Simple login attempt tracker: per-email timestamps (seconds)
_login_attempts: dict[str, list[float]] = {}
LOGIN_ATTEMPTS_WINDOW = 15 * 60  # 15 minutes
LOGIN_ATTEMPTS_LIMIT = 5


@router.post("/register", status_code=201)
def register(req: RegisterRequest):
    global _next_id
    if req.email in _users:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = get_password_hash(req.password)
    user = {"id": _next_id, "email": req.email, "hashed_password": hashed, "is_active": True, "is_admin": False}
    _users[req.email] = user
    _next_id += 1
    return {"id": user["id"], "email": user["email"]}


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    # rate limiting per email
    import time

    now = time.time()
    attempts = _login_attempts.setdefault(req.email, [])
    # remove stale
    attempts[:] = [t for t in attempts if now - t <= LOGIN_ATTEMPTS_WINDOW]
    if len(attempts) >= LOGIN_ATTEMPTS_LIMIT:
        raise HTTPException(status_code=429, detail="Too many login attempts. Try again later.")

    user = _users.get(req.email)
    if not user or not verify_password(req.password, user["hashed_password"]):
        # record failed attempt
        attempts.append(now)
        _login_attempts[req.email] = attempts
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # on success clear attempts
    _login_attempts.pop(req.email, None)
    token = create_access_token({"sub": str(user["id"]), "email": user["email"]})
    return {"access_token": token, "token_type": "bearer"}
