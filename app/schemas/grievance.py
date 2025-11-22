from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GrievanceCreate(BaseModel):
    title: str = Field(..., max_length=255)
    category: Optional[str]
    dept_id: Optional[int]
    description: str


class GrievanceRead(BaseModel):
    id: int
    title: str
    category: Optional[str]
    dept_id: Optional[int]
    description: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
