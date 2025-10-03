from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime

def get_or_create_child(db: Session, child_id: int = 1):
    child = db.query(models.Child).filter(models.Child.id == child_id).first()
    if not child:
        child = models.Child(id=child_id, name="Student", age=7)
        db.add(child)
        db.commit()
        db.refresh(child)
    return child

def create_activity(db: Session, submission: schemas.AnswerSubmission, ai_response: str):
    activity = models.Activity(
        child_id=submission.child_id,
        timestamp=datetime.utcnow(),
        level=submission.level,
        problem=submission.problem,
        child_answer=submission.answer,
        correct_answer=submission.correct_answer,
        is_correct=(submission.answer.strip() == submission.correct_answer.strip()),
        ai_response=ai_response,
        time_taken_seconds=submission.time_taken
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity

def get_child_activities(db: Session, child_id: int = 1, limit: int = 50):
    return db.query(models.Activity).filter(
        models.Activity.child_id == child_id
    ).order_by(models.Activity.timestamp.desc()).limit(limit).all()

def get_performance_stats(db: Session, child_id: int = 1):
    activities = get_child_activities(db, child_id, limit=100)
    
    if not activities:
        return schemas.PerformanceStats(
            total_problems=0,
            correct_answers=0,
            accuracy=0,
            average_time=0,
            current_streak=0,
            recent_activities=[]
        )
    
    total = len(activities)
    correct = sum(1 for a in activities if a.is_correct)
    avg_time = sum(a.time_taken_seconds for a in activities) / total
    
    # Calculate current streak
    streak = 0
    for activity in activities:
        if activity.is_correct:
            streak += 1
        else:
            break
    
    return schemas.PerformanceStats(
        total_problems=total,
        correct_answers=correct,
        accuracy=round((correct / total) * 100, 1) if total > 0 else 0,
        average_time=round(avg_time, 1),
        current_streak=streak,
        recent_activities=[schemas.ActivityResponse.from_orm(a) for a in activities[:10]]
    )