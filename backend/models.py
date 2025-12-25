from sqlalchemy import Column, String, DateTime
from .database import Base
import datetime
import uuid

class VideoJob(Base):
    __tablename__ = "video_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String)
    status = Column(String, default="Processing")  # Processing, Completed, Failed
    output_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
