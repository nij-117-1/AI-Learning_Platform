from fastapi import APIRouter, HTTPException, status
from .schemas import (
    FIBRequest, FIBResponse, 
    EvaluationRequest, EvaluationResponse, AssessmentResponse, AssessmentRequest, RoleplayRequest, RoleplayResponse
)
from .services import LanguageTesterService
from .schemas import (
    FIBRequest, FIBResponse,
    EvaluationRequest, EvaluationResponse,
    TranslationChallengeRequest, TranslationChallengeResponse # New
)
import random
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/language-tester",
    tags=["Language Assessment"]
)

@router.post("/generate", response_model=AssessmentResponse, status_code=status.HTTP_200_OK)
async def create_assessment(request_data: AssessmentRequest):
    """
    Generate a personalized MCQ assessment based on CEFR levels and specific scenarios.
    """
    try:
        result = LanguageTesterService.generate_assessment(request_data)
        return result
    except Exception as e:
        logger.error(f"Error generating assessment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate language assessment."
        )

@router.post("/fib/generate", response_model=FIBResponse)
async def generate_fib(request: FIBRequest):
    """
    Endpoint 1: Create 'Fill in the Blank' questions based on CEFR level and scenario.
    """
    try:
        return LanguageTesterService.generate_fib_questions(request)
    except Exception as e:
        logger.error(f"FIB Generation Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating questions.")

@router.post("/fib/evaluate", response_model=EvaluationResponse)
async def evaluate_fib(request: EvaluationRequest):
    """
    Endpoint 2: Evaluate a user's answer for typos, correctness, and grammar.
    """
    try:
        return LanguageTesterService.evaluate_answer(request)
    except Exception as e:
        logger.error(f"FIB Evaluation Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error evaluating answer.")

@router.post("/translation/challenge", response_model=TranslationChallengeResponse)
async def create_translation_challenge(request: TranslationChallengeRequest):
    """
    Endpoint 3: Generate an Active or Passive translation challenge.
    Determines challenge type (To Native, To Target, or Explain Nuance) automatically.
    """
    try:
        return LanguageTesterService.generate_translation_task(request)
    except Exception as e:
        logger.error(f"Translation Generation Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate translation challenge."
        )

@router.post("/roleplay/continue", response_model=RoleplayResponse)
async def chat_roleplay(request: RoleplayRequest):
    """
    Endpoint 4: Conversational Roleplay.
    Processes the latest user message, provides grammatical feedback, 
    and returns the AI's next line in character.
    """
    try:
        return LanguageTesterService.continue_roleplay(request)
    except Exception as e:
        logger.error(f"Roleplay Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The language coach is currently unavailable."
        )