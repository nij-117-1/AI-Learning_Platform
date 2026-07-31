from fastapi import APIRouter, HTTPException
from learning.language_helper.schemas import (
    IdiomRequest, IdiomResponse,
    PoeticRequest, PoeticResponse,
    WordOfDayRequest, WordOfDayResponse,
    LessonRequest, LessonResponse,
    TranslationRequest, TranslationResponse,
RewriteRequest, RewriteResponse
)
from learning.language_helper.services import LanguageHelperService

router = APIRouter(
    prefix="/language-helper",
    tags=["Language Learning"]
)

service = LanguageHelperService()

@router.post("/generate-idiom", response_model=IdiomResponse)
async def get_idiom(request_data: IdiomRequest):
    try:
        result = service.generate_idiom(request_data)
        return result.toDict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/poetic-reflection", response_model=PoeticResponse)
async def get_poetic_reflection(request_data: PoeticRequest):
    """
    Deep-dive into the 'Soul' of a word through poetry and philosophy.
    """
    try:
        result = service.generate_poetic_reflection(request_data)
        return result.toDict()
    except Exception as e:
        logger.error(f"Router Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate poetic reflection")

@router.post("/word-of-the-day", response_model=WordOfDayResponse)
async def get_word_of_the_day(request_data: WordOfDayRequest):
    """
    Get a deeply researched Word of the Day with etymology and vibes.
    """
    try:
        result = service.generate_daily_word(request_data)
        # result.toDict() handles the conversion of DSPy outputs to our Schema
        return result.toDict()
    except Exception as e:
        logger.error(f"WordOfDay Router Error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="The Linguist is currently unavailable to find today's word."
        )

@router.post("/generate-lesson", response_model=LessonResponse)
async def get_custom_lesson(request_data: LessonRequest):
    """
    Generate a personalized language lesson with a custom creative theme.
    """
    try:
        result = service.generate_custom_lesson(request_data)
        return result.toDict()
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Tutor Service Unavailable: {str(e)}"
        )

@router.post("/translate", response_model=TranslationResponse)
async def translate_content(request_data: TranslationRequest):
    """
    Context-aware translation preserving tone and technical constraints.
    """
    try:
        result = service.translate_text(request_data)
        # .toDict() ensures DSPy output maps to Pydantic TranslationResponse
        return result.toDict()
    except Exception as e:
        logger.error(f"Router Error in Translation: {e}")
        raise HTTPException(
            status_code=500, 
            detail="The Translator is currently unable to process your request."
        )

@router.post("/rewrite", response_model=RewriteResponse)
async def rewrite_text(request_data: RewriteRequest):
    """
    Rewrite text for different audiences, tones, or length requirements.
    """
    try:
        result = service.rewrite_content(request_data)
        return result.toDict()
    except Exception as e:
        logger.error(f"Rewriter Router Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="The Editor is currently unavailable to rewrite your text."
        )