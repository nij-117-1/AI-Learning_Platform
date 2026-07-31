from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import SentenceRequest, SentenceResponse
from .services import SentenceService

router = APIRouter(
    prefix="/sentence-of-the-day",
    tags=["Linguistic Insights"]
)

@router.post("/", response_model=SentenceResponse)
async def get_daily_sentence(payload: SentenceRequest):
    """
    Fetches the daily featured sentence with linguistic and cultural nuances.
    """
    service = SentenceService()
    try:
        return service.generate_daily_sentence(
            target=payload.target_language,
            native=payload.native_language,
            context=payload.context_setting,
            level=payload.complexity_level
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate linguistic insight."
        )