from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.grievance import GrievanceCreate, GrievanceRead
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.grievance import Grievance

router = APIRouter()


@router.post("/", response_model=GrievanceRead)
def create_grievance(payload: GrievanceCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    # user is the User model returned by dependency
    grievance = Grievance(
        student_id=user.id,
        dept_id=payload.dept_id,
        title=payload.title,
        category=payload.category,
        description=payload.description,
    )
    db.add(grievance)
    db.commit()
    db.refresh(grievance)
    return grievance


@router.get("/{grievance_id}", response_model=GrievanceRead)
def read_grievance(grievance_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    g = db.query(Grievance).filter(Grievance.id == grievance_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Not found")
    return g


@router.get("/health", response_model=dict)
def health_check():
    return {"status": "healthy"}
