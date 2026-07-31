from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict

class PersonaRequest(BaseModel):
    topic: str = Field(..., example="Universal Basic Income")
    stance: str = Field(..., example="Strongly Opposed")
    debate_style: Literal["Socratic", "Aggressive", "Scientific", "Empathetic", "Formal"]
    user_constraints: Optional[str] = Field(None, example="Focus on inflation.")

class PersonaResponse(BaseModel):
    master_prompt: str
    status: str = "success"


class ChatEntry(BaseModel):
    role: str = Field(..., example="CEO")
    content: str = Field(..., example="AI is just a tool.")

class DebateTurnRequest(BaseModel):
    persona: str = Field(..., description="The system prompt defining the character.")
    topic: str = Field(..., example="Is AI a threat to creativity?")
    theme: str = Field(..., example="Philosopher vs Silicon Valley CEO")
    history: List[Dict[str, str]] = Field(..., description="List of previous messages.")
    context: str = Field(..., description="Focus area (e.g., impact on jobs).")
    strategy: Literal["attack", "defend", "counter"]
    instructions: Optional[str] = "Be concise and sharp."
    evidence: Optional[str] = None

class DebateTurnResponse(BaseModel):
    rebuttal_summary: str
    argument_body: str
    rhetorical_devices: List[str]
    next_question: str
    status: str = "success"