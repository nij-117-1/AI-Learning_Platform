from pydantic import BaseModel, Field
from typing import List, Optional

class MotivationRequest(BaseModel):
    seed_topic: str = Field(..., example="Resilience", description="Keyword to anchor the quote.")
    # Literal replaced with a standard string
    quote_type: str = Field(..., example="stoic", description="Style of quote (e.g., stoic, modern, poetic).")
    user_feeling: str = Field(..., example="I feel overwhelmed.", description="User's emotional state.")

class MotivationResponse(BaseModel):
    quote: str
    author_persona: str
    actionable_insight: str
    current_date: str

class ReflectionRequest(BaseModel):
    current_mood: str = Field(..., example="Anxious about work.", description="User's current emotional state.")
    goal_alignment: str = Field(..., example="Creative independence.", description="The goal or value to focus on.")
    recent_patterns: Optional[str] = Field(None, example="High energy in mornings, crash by 3 PM.")

class ReflectionResponse(BaseModel):
    prompts: List[str] = Field(..., min_items=3, max_items=3)
    perspective_shift: str