from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/play", response_class=HTMLResponse)
async def play_page(request: Request, child_id: int = 1):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "child_id": child_id}
    )

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(
    request: Request,
    child_id: int = 1,
    db: Session = Depends(get_db)
):
    stats = crud.get_performance_stats(db, child_id)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "child_id": child_id,
            "stats": stats
        }
    )

