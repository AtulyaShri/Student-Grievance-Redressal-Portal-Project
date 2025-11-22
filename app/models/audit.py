from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Text
from app.db.base import Base

class Audit(Base):
    __tablename__ = "audits"
    id = Column(Integer, primary_key=True)
    grievance_id = Column(Integer, ForeignKey("grievances.id"))
    action = Column(String(100))
    performed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    remarks = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
