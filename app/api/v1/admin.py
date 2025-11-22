from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.schemas.grievance import GrievanceRead
from app.api.dependencies import get_current_user

router = APIRouter()

# For demo we rely on student module's in-memory store
from app.api.v1 import student as student_module


@router.get("/grievances", response_model=List[GrievanceRead])
def list_grievances(user=Depends(get_current_user)):
    # TODO: enforce admin role
    return list(student_module._db.values())


@router.get("/grievances/{grievance_id}", response_model=GrievanceRead)
def get_grievance(grievance_id: int, user=Depends(get_current_user)):
    g = student_module._db.get(grievance_id)
    if not g:
        raise HTTPException(status_code=404, detail="Not found")
    return g
