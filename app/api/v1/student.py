from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from datetime import datetime

from app.schemas.grievance import GrievanceCreate, GrievanceRead
from app.api.dependencies import get_current_user

router = APIRouter()

# In-memory store (replace with DB)
_db: Dict[int, Dict] = {}
_counter = 1


@router.post("/", response_model=GrievanceRead)
def create_grievance(payload: GrievanceCreate, user=Depends(get_current_user)):
    global _counter
    gid = _counter
    _counter += 1
    record = {
        "id": gid,
        "title": payload.title,
        "category": payload.category,
        "dept_id": payload.dept_id,
        "description": payload.description,
        "status": "open",
        "created_at": datetime.utcnow(),
    }
    _db[gid] = record
    return record


@router.get("/{grievance_id}", response_model=GrievanceRead)
def read_grievance(grievance_id: int, user=Depends(get_current_user)):
    g = _db.get(grievance_id)
    if not g:
        raise HTTPException(status_code=404, detail="Not found")
    return g
