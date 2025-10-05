import sys
import os
from pathlib import Path


# Add the parent directory to Python path for imports
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.routers import auth, ml_pipeline 
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="DataSage API",
    description="Advanced Data Analytics Platform - FastAPI Backend",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(ml_pipeline.router, prefix="/api")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("🚀 DataSage API v2.0 started successfully!")

# Health check endpoints
@app.get("/")
async def root():
    return {
        "message": "DataSage API v2.0 - Ready!",
        "status": "healthy",
        "version": "2.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "DataSage API",
        "version": "2.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", 
        host=settings.api_host, 
        port=settings.api_port, 
        reload=settings.debug,
        log_level="info"
    )
