from fastapi import APIRouter, HTTPException, status
from .schemas import RewriteRequest, RewriteResponse
from .services import RewriterService

router = APIRouter(
    prefix="/rewriter",
    tags=["Content Tools"]
)

@router.post("/process", response_model=RewriteResponse)
async def rewrite_text(payload: RewriteRequest):
    """
    Endpoint to rewrite text using the DSPy logic.
    """
    service = RewriterService()
    try:
        prediction = service.process_rewrite(payload)
        return {
            "rationale": prediction.rationale,
            "rewritten_text": prediction.rewritten_text,
            "improvements_made": prediction.improvements_made
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Rewrite engine failed: {str(e)}"
        )