"""
Health check endpoints for Mouse AI API.
"""
from fastapi import APIRouter

from app.core.config import settings
from app.models.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint to verify service status.
    
    Returns:
        HealthResponse: Service status and version information
    """
    return HealthResponse(
        status="ok",
        version=settings.VERSION
    )