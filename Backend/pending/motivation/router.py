from fastapi import APIRouter, HTTPException, status
from learning.motivation.schemas import (
    MotivationRequest, 
    MotivationResponse,
    ReflectionRequest,
    ReflectionResponse
)
from learning.motivation.services import MotivationService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/motivation",
    tags=["Motivation & Reflection"]
)

@router.post("/generate", response_model=MotivationResponse)
async def create_motivation(payload: MotivationRequest):
    """Endpoint for daily motivational quotes."""
    try:
        return MotivationService.generate_motivation_quote(payload)
    except Exception as e:
        logger.error(f"Motivation Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating quote.")

@router.post("/reflect", response_model=ReflectionResponse)
async def create_reflection(payload: ReflectionRequest):
    """
    Endpoint to generate deep journaling prompts based on user mood and goals.
    """
    try:
        return MotivationService.generate_reflection_session(payload)
    except Exception as e:
        logger.error(f"Reflection Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating reflection prompts."
        )