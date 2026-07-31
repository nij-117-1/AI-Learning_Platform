from datetime import datetime
from pydantic import BaseModel, Field


class PromptFile(BaseModel):
    name: str = Field(description="Unique identifier for the prompt")
    content: str = Field(description="The system prompt text")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
