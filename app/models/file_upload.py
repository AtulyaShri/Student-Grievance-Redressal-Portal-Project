from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.base import Base

class FileUpload(Base):
    __tablename__ = "file_uploads"
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    content_type = Column(String(100), nullable=False)
    file_size = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)  # Foreign key to User
    created_at = Column(DateTime(timezone=True), server_default=func.now())
