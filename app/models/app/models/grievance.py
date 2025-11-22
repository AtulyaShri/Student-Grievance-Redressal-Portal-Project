from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, func
from app.db.base import Base
import enum

class StatusEnum(str, enum.Enum):
    submitted = "Submitted"
    under_review = "Under Review"
    in_progress = "In Progress"
    resolved = "Resolved"
    closed = "Closed"

class Grievance(Base):
    __tablename__ = "grievances"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dept_id = Column(Integer, ForeignKey("departments.id"))
    title = Column(String(255), nullable=False)
    category = Column(String(100))
    description = Column(Text, nullable=False)
    attachment_path = Column(String(255))
    status = Column(Enum(StatusEnum), default=StatusEnum.submitted)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
