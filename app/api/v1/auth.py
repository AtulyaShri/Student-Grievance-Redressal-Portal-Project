from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict

from app.core import security

router = APIRouter()


class RegisterRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Simple in-memory store for demo purposes. Replace with DB in production.
_users: Dict[str, Dict] = {}


@router.post("/register", status_code=201)
def register(req: RegisterRequest):
    if req.email in _users:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = security.get_password_hash(req.password)
    _users[req.email] = {"email": req.email, "hashed": hashed}
    return {"msg": "registered"}


@router.post("/login", response_model=TokenResponse)
def login(req: RegisterRequest):
    user = _users.get(req.email)
    if not user or not security.verify_password(req.password, user["hashed"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = security.create_access_token(subject=req.email)
    return {"access_token": token}
