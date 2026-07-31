from pydantic import BaseModel, Field
from typing import Optional, Literal

class TranslationRequest(BaseModel):
    text_to_translate: str = Field(..., description="Source text")
    source_language: str
    target_language: str
    tone: Literal["formal", "casual", "business", "poetic", "technical"]
    reference_material: Optional[str] = None
    custom_instructions: Optional[str] = None

class TranslationResponse(BaseModel):
    rationale: str
    translated_text: str
    cultural_notes: Optional[str] = None