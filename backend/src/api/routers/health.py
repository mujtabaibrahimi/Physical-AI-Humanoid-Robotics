"""
Health Check Router
Service health status endpoint
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint

    Returns:
        Service status and timestamp
    """
    return {
        "status": "healthy",
        "service": "Physical AI Textbook API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "api": "operational",
            "database": "pending",  # Will check Qdrant/Neon when implemented
            "cache": "pending",      # Will check Redis when implemented
        }
    }
