from fastapi import APIRouter, HTTPException, Depends
from .schemas import TranslationRequest, TranslationResponse
from .services import TranslatorService

router = APIRouter(
    prefix="/translator",
    tags=["Linguistic Services"]
)

@router.post("/process", response_model=TranslationResponse)
async def process_translation(
    request: TranslationRequest,
    service: TranslatorService = Depends(TranslatorService)
):
    """
    Endpoint to process contextual translations using DSPy Chain of Thought.
    """
    try:
        result = service.translate(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Translation Engine Error")