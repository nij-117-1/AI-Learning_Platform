from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class MemoryRequest(BaseModel):
    """Data required to generate memory hooks."""
    topic: str = Field(..., description="The facts or data to memorize", min_length=5)
    technique: Optional[str] = Field(default="Best Fit", description="Preferred mnemonic technique")

class MemoryHook(BaseModel):
    """Individual concept-to-hook mapping."""
    concept: str = Field(..., description="The specific piece of info")
    hook: str = Field(..., description="The mnemonic or mental image")

class MemoryResponse(BaseModel):
    """Structured output for the client."""
    explanation: str
    memory_hooks: List[MemoryHook]
    retention_plan: str