from fastapi import APIRouter, Depends, status
from fastapi import APIRouter, status
from practice.iq_generator.schemas import (
    RiddleRequest, RiddleResponse, 
    EvaluationRequest, EvaluationResponse,
    BridgeRequest, BridgeResponse,
    SocraticRequest, SocraticResponse,
    BiasRequest, BiasResponse, 
    PuzzleRequest, PuzzleResponse,
    PuzzleEvaluationRequest, PuzzleEvaluationResponse
)
from practice.iq_generator.services import IQService
from practice.iq_generator.services import IQService

router = APIRouter(
    prefix="/iq-generator",
    tags=["IQ Generation"]
)

@router.post("/puzzle/generate", response_model=PuzzleResponse, status_code=status.HTTP_201_CREATED)
async def create_puzzle(payload: PuzzleRequest):

    print(payload)
    """
    Trigger the generation of a personalized cognitive puzzle.
    The system generates a unique internal seed to ensure non-repetitive content.
    """
    return IQService.generate_puzzle(payload)
    
@router.post("/puzzle/evaluate", response_model=PuzzleEvaluationResponse)
async def evaluate_puzzle_attempt(payload: PuzzleEvaluationRequest):
    """
    Advanced evaluation endpoint that provides accuracy scores, 
    logical redirection, and metacognitive prompts.
    """
    return IQService.evaluate_puzzle(payload)
    
@router.post("/generate", response_model=RiddleResponse, status_code=status.HTTP_201_CREATED)
async def create_riddle(payload: RiddleRequest):
    """
    Endpoint to trigger the generation of a new cognitive puzzle.
    """
    return IQService.generate_riddle(payload)



@router.post("/evaluate", response_model=EvaluationResponse)
async def check_answer(payload: EvaluationRequest):
    """
    Endpoint to evaluate a user's answer and receive feedback.
    """
    return IQService.evaluate_answer(payload)

@router.post("/bridge", response_model=BridgeResponse, status_code=status.HTTP_201_CREATED)
async def create_conceptual_bridge(payload: BridgeRequest):
    """
    Generate a conceptual bridge between two unrelated topics to 
    train neuroplasticity and lateral thinking.
    """
    return IQService.build_bridge(payload)

@router.post("/socratic-challenge", response_model=SocraticResponse, status_code=status.HTTP_200_OK)
async def socratic_challenge(payload: SocraticRequest):
    """
    Challenge a user statement using Socratic questioning to identify 
    logical fallacies and encourage deeper critical thinking.
    """
    return IQService.get_socratic_challenge(payload)

@router.post("/bias-inoculator", response_model=BiasResponse, status_code=status.HTTP_201_CREATED)
async def bias_training(payload: BiasRequest):
    """
    Generate a 'System 1 vs System 2' training scenario. 
    The response contains both the scenario (to show the user) 
    and the rational reveal (to show after the user answers).
    """
    return IQService.inoculate_bias(payload)