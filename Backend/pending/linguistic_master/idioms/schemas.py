from pydantic import BaseModel, Field
from typing import Literal, Optional

class IdiomRequest(BaseModel):
    target_language: str = Field(..., examples=["French"])
    user_proficiency: Literal["beginner", "intermediate", "advanced", "native-aspirant"]
    theme_or_keyword: str = Field(..., examples=["Success and Hard Work"])
    native_language: str = Field(..., examples=["English"])
    seed: str = Field(..., description="Unique string for rotation logic")
    custom_user_request: Optional[str] = None

class IdiomResponse(BaseModel):
    idiom_in_target_language: str
    phonetic_pronunciation: str
    figurative_meaning: str
    cultural_context: str
    equivalent_in_native_language: str
    dialogue_scenario: str
    practice_prompt: str
    rationale: str