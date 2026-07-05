from sqlalchemy import Column, Integer, String, Text, DateTime, Date
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base

class UserNote(Base):
    __tablename__ = "users_notes"
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(100), index=True)
    topic = Column(String(150), index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class UserRoadmap(Base):
    __tablename__ = "users_roadmap"
    id = Column(Integer, primary_key=True, index=True)
    sprint_start_date = Column(Date)
    roadmap_json = Column(JSONB)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
