from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.schemas.grievance import GrievanceRead
from app.api.deps import get_current_user, admin_required
from app.db.session import get_db
from app.models.grievance import Grievance

router = APIRouter()


@router.get("/grievances", response_model=List[GrievanceRead])
def list_grievances(user=Depends(get_current_user), db: Session = Depends(get_db)):
    # TODO: enforce admin role
    return db.query(Grievance).all()


@router.get("/grievances/{grievance_id}", response_model=GrievanceRead)
def get_grievance(grievance_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    g = db.query(Grievance).filter(Grievance.id == grievance_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Not found")
    return g
