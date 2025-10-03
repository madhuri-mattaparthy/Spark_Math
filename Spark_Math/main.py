from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import pages, api
import os

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="NumBot - AI Math Companion",
    description="An interactive math learning game for children with AI companion",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pages.router, tags=["Pages"])
app.include_router(api.router, prefix="/api", tags=["API"])
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {
        "message": "NumBot - AI Math Companion",
        "endpoints": {
            "play": "/play",
            "dashboard": "/dashboard",
            "api_docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}