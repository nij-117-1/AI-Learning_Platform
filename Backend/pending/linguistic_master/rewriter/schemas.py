from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class RewriteRequest(BaseModel):
    original_text: str = Field(..., description="The text to rewrite.")
    target_tone: str = Field(..., description="Tone like 'professional' or 'witty'.")
    audience: str = Field(..., description="The target demographic.")
    transformation_goal: Literal["paraphrase", "shorten", "expand", "simplify"]
    custom_instructions: Optional[str] = None

class RewriteResponse(BaseModel):
    rationale: str
    rewritten_text: str
    improvements_made: List[str]