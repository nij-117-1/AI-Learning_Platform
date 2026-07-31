from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import ConceptRequest, ConceptResponse
from .services import PoetService

router = APIRouter(
    prefix="/poet",
    tags=["Poetic Philology"]
)

@router.post("/explain", response_model=ConceptResponse)
async def explain_concept(request: ConceptRequest):
    """
    Explains the 'Soul' of a word using AI-driven poetic philology.
    """
    service = PoetService()
    try:
        result = service.generate_explanation(request)
        return ConceptResponse(
            etymological_soul=result.etymological_soul,
            original_poetry=result.original_poetry,
            soulful_translation=result.soulful_translation,
            philosophical_reflection=result.philosophical_reflection,
            visual_metaphor=result.visual_metaphor
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The soul of the word remained hidden: {str(e)}"
        )