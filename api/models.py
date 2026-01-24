# api/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String, index=True)
    text = Column(String)
    has_image = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
