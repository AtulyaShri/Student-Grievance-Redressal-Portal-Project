from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
