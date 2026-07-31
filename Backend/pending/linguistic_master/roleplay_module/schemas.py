from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ChatMessage(BaseModel):
    role: str
    content: str

class RoleplayRequest(BaseModel):
    system_prompt: str = Field(..., description="The core persona traits.")
    history: List[ChatMessage]
    message: str
    language: str = "English"
    seed: str
    additional_instructions: Optional[str] = "Be creative."

class RoleplayResponse(BaseModel):
    response_message: str
    status: str = "success"

class RoleplayRecord(BaseModel):
    name: str = Field(..., description="Unique ID/Name of the persona")
    prompt: str = Field(..., description="The system prompt/personality")

class RoleplayUpdate(BaseModel):
    prompt: str