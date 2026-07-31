from fastapi import APIRouter, HTTPException, Depends, status
from .schemas import IdiomRequest, IdiomResponse
from .services import IdiomService

router = APIRouter(prefix="/idioms", tags=["Idioms"])

@router.post("/generate", response_model=IdiomResponse)
async def create_idiom_lesson(payload: IdiomRequest):
    """
    Generate an idiomatic expression lesson based on linguistic parameters.
    """
    service = IdiomService()
    try:
        lesson = service.generate_idiom_lesson(payload)
        return lesson
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Philology Engine Error: {str(e)}"
        )