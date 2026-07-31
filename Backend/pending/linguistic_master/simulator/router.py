from fastapi import APIRouter, HTTPException, status
from .schemas import SimulationRequest, SimulationResponse
from .services import SimulationService
from typing import List
from fastapi import APIRouter, HTTPException, status
from .schemas import (
    SimulationRequest, SimulationResponse, 
    PromptCreate, PromptDetail, PromptUpdate
)
from .services import SimulationService, PromptManager
from fastapi import APIRouter, HTTPException, status
from .schemas import SimulationRequest, SimulationResponse, ChatRequest, ChatResponse
from .services import SimulationService, ChatService


router = APIRouter(
    prefix="/sims",
    tags=["Behavioral Simulation"]
)

@router.post("/run", response_model=SimulationResponse, status_code=status.HTTP_200_OK)
async def create_simulation(payload: SimulationRequest):
    """
    Triggers a new behavioral simulation based on persona and scenario.
    """
    try:
        result = SimulationService.run_behavioral_sim(payload)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Simulation Engine Error: {str(e)}"
        )

@router.post("/chat", response_model=ChatResponse)
async def continue_chat(payload: ChatRequest):
    """
    Maintains a situational conversation turn. 
    The client is responsible for sending back the 'updated_history'.
    """
    try:
        return ChatService.execute_chat(payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Chat Service Error: {str(e)}"
        )

@router.get("/prompts", response_model=List[str])
async def list_prompts():
    """List all available prompt names."""
    return PromptManager.list_names()

@router.post("/prompts", status_code=status.HTTP_201_CREATED)
async def create_prompt(payload: PromptCreate):
    """Create a new system prompt."""
    PromptManager.save_prompt(payload.name, payload.content)
    return {"message": f"Prompt '{payload.name}' created."}

@router.get("/prompts/{name}", response_model=PromptDetail)
async def view_prompt(name: str):
    """View a specific prompt's content."""
    content = PromptManager.get_prompt(name)
    return {"name": name, "content": content}

@router.put("/prompts/{name}")
async def update_prompt(name: str, payload: PromptUpdate):
    """Update existing prompt content."""
    # Ensure it exists first
    PromptManager.get_prompt(name) 
    PromptManager.save_prompt(name, payload.content)
    return {"message": f"Prompt '{name}' updated."}