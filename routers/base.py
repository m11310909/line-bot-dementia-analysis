# routers/base.py
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "XAI Flex Message API", "docs": "/docs"}

@router.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0",
        "services": {"api": "running"}
    }

