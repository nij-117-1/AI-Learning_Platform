from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class SimulationRequest(BaseModel):
    persona: str = Field(..., example="A pragmatic retired starship captain.")
    scenario: str = Field(..., example="Oxygen levels at 15%. Distress signal detected.")
    user_input: str = Field(..., example="Captain, we must help them!")
    additional_context: Optional[str] = None
    temperature: Optional[float] = 0.4

class SimulationResponse(BaseModel):
    simulation_id: str
    thought_process: str
    chosen_action: str
    response_dialogue: str
    emotional_state: str

class PromptCreate(BaseModel):
    name: str = Field(..., example="captain_crush")
    content: str = Field(..., example="You are a strict, no-nonsense starship captain.")

class PromptUpdate(BaseModel):
    content: str

class PromptDetail(BaseModel):
    name: str
    content: str

class PromptList(BaseModel):
    prompts: List[str]


class ChatMessage(BaseModel):
    role: str  # "User" or "Assistant"
    content: str

class ChatRequest(BaseModel):
    persona: str
    scenario: str
    user_input: str
    chat_history: List[ChatMessage] = Field(default_factory=list)
    model_name: Optional[str] = None

class ChatResponse(BaseModel):
    thought: str
    dialogue: str
    updated_history: List[ChatMessage]