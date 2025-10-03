from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Child(Base):
    __tablename__ = "children"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, default="Student")
    age = Column(Integer, default=7)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    activities = relationship("Activity", back_populates="child")

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), default=1)
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(Integer)
    problem = Column(String)
    child_answer = Column(String)
    correct_answer = Column(String)
    is_correct = Column(Boolean)
    ai_response = Column(Text)
    time_taken_seconds = Column(Integer)
    
    child = relationship("Child", back_populates="activities")