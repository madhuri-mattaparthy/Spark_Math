from pydantic import BaseModel
from datetime import datetime
from typing import List

class AnswerSubmission(BaseModel):
    child_id: int = 1
    level: int
    problem: str
    answer: str
    correct_answer: str
    time_taken: int

class ActivityResponse(BaseModel):
    id: int
    timestamp: datetime
    level: int
    problem: str
    child_answer: str
    correct_answer: str
    is_correct: bool
    ai_response: str
    time_taken_seconds: int
    
    class Config:
        from_attributes = True

class PerformanceStats(BaseModel):
    total_problems: int
    correct_answers: int
    accuracy: float
    average_time: float
    current_streak: int
    recent_activities: List[ActivityResponse]
