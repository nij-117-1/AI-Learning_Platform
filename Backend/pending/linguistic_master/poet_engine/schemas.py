from pydantic import BaseModel, Field
from typing import Literal, Optional

class ConceptRequest(BaseModel):
    target_language: str = Field(..., example="Urdu")
    native_language: str = Field(..., example="English")
    concept_word: str = Field(..., example="Ishq")
    poetic_style: Literal["Shayari/Couplet", "Haiku", "Metaphorical Prose", "Ghazal-style"]
    user_mood: Optional[str] = "mystical"
    user_custom_instruction: Optional[str] = None

class ConceptResponse(BaseModel):
    etymological_soul: str
    original_poetry: str
    soulful_translation: str
    philosophical_reflection: str
    visual_metaphor: str