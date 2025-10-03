from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app import crud, schemas
from app.database import get_db
from app.services.ai_service import ai_service
import httpx
import os

router = APIRouter()

# New: Request model for text-to-speech
class TextToSpeechRequest(BaseModel):
    text: str

# New: AI Voice endpoint
@router.post("/text-to-speech")
async def text_to_speech(request: TextToSpeechRequest):
    """Convert text to AI voice using OpenAI TTS"""
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key == "your-openai-api-key-here":
        return {"error": "No API key configured"}
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/audio/speech",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "tts-1",
                    "voice": "nova",
                    "input": request.text,
                    "speed": 0.9
                }
            )
            
            if response.status_code == 200:
                return StreamingResponse(
                    iter([response.content]),
                    media_type="audio/mpeg"
                )
            else:
                print(f"OpenAI TTS Error: {response.status_code}")
                return {"error": "TTS failed"}
                
    except Exception as e:
        print(f"TTS error: {e}")
        return {"error": str(e)}

@router.post("/submit-answer")
async def submit_answer(
    submission: schemas.AnswerSubmission,
    db: Session = Depends(get_db)
):
    child = crud.get_or_create_child(db, submission.child_id)
    is_correct = submission.answer.strip() == submission.correct_answer.strip()
    
    ai_response = await ai_service.generate_response(
        is_correct=is_correct,
        problem=submission.problem,
        child_age=child.age
    )
    
    activity = crud.create_activity(db, submission, ai_response)
    
    return {
        "is_correct": is_correct,
        "ai_response": ai_response,
        "activity_id": activity.id,
        "correct_answer": submission.correct_answer
    }

@router.get("/generate-question")
def generate_question(level: int = 1):  
    if level not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Level must be 1, 2, or 3")
    
    # Instant generation - no AI latency
    question = ai_service.generate_question(level=level)
    
    return {
        "problem": question["problem"],
        "answer": question["answer"],
        "level": level
    }

@router.get("/performance/{child_id}", response_model=schemas.PerformanceStats)
async def get_performance(child_id: int = 1, db: Session = Depends(get_db)):
    stats = crud.get_performance_stats(db, child_id)
    return stats

@router.get("/activities/{child_id}")
async def get_activities(
    child_id: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    activities = crud.get_child_activities(db, child_id, limit)
    
    return {
        "child_id": child_id,
        "total": len(activities),
        "activities": [
            {
                "id": a.id,
                "timestamp": a.timestamp.isoformat(),
                "level": a.level,
                "problem": a.problem,
                "child_answer": a.child_answer,
                "correct_answer": a.correct_answer,
                "is_correct": a.is_correct,
                "ai_response": a.ai_response,
                "time_taken_seconds": a.time_taken_seconds
            }
            for a in activities
        ]
    }