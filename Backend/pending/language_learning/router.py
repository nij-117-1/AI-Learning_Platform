from fastapi import APIRouter, HTTPException, Depends
from learning.language_learning.models import LanguageSessionRequest, LanguageSessionResponse
from learning.language_learning.services import LanguageLearningService

router = APIRouter(
    prefix="/language-learning",
    tags=["Language Learning"]
)

@router.post("/chat", response_model=LanguageSessionResponse)
async def language_bot_interaction(payload: LanguageSessionRequest):
    """
    Handles translation and proactive language learning suggestions.
    """
    service = LanguageLearningService()
    try:
        response = service.process_session(payload)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fulfillment error: {str(e)}")