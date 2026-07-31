from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class WOTDRequest(BaseModel):
    target_language: str = Field(..., example="Japanese")
    native_language: str = Field(default="English")
    proficiency: Literal["basic", "academic", "poetic", "slang"] = Field(default="academic")
    theme: Optional[str] = Field(default="General")
    custom_instructions: Optional[str] = Field(None)

class WOTDResponse(BaseModel):
    word: str
    native_translation: str
    phonetic_and_audio_guide: str
    morphology_breakdown: str
    primary_definition: str
    the_vibe_check: str
    modern_usage_sentence: str
    synonym_web: List[str]