"""Dependency injections for FastAPI endpoints."""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core import security
from app.db.session import get_db
from app.models.user import User as UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Validate JWT token and return current User from database."""
    try:
        payload = security.decode_token(token)
        # Prefer explicit 'email' claim; handle 'sub' which may be either an id or an email
        email = payload.get("email")
        user = None
        if email:
            user = db.query(UserModel).filter(UserModel.email == email).first()
        else:
            sub = payload.get("sub")
            if sub:
                # if sub looks like an email, treat it as email
                if isinstance(sub, str) and "@" in sub:
                    user = db.query(UserModel).filter(UserModel.email == sub).first()
                else:
                    try:
                        user = db.query(UserModel).filter(UserModel.id == int(sub)).first()
                    except Exception:
                        user = None

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def admin_required(current_user: UserModel = Depends(get_current_user)):
    """Dependency that ensures current_user is an admin."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return current_user
