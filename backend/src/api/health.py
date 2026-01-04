from fastapi import APIRouter
from typing import Dict

router = APIRouter(prefix="/api", tags=["health"])

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint to verify the API is running
    """
    return {"status": "healthy", "message": "Todo API is running"}

@router.get("/ready")
async def readiness_check() -> Dict[str, str]:
    """
    Readiness check endpoint
    """
    # In a real implementation, this would check database connections,
    # external service availability, etc.
    return {"status": "ready", "message": "Todo API is ready to serve requests"}