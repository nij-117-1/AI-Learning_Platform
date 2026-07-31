from pydantic import BaseModel, Field
from typing import List, Literal

class SentenceRequest(BaseModel):
    target_language: str = Field(..., example="Spanish")
    native_language: str = Field(..., example="English")
    context_setting: Literal["business", "casual", "literary", "romantic", "travel"]
    complexity_level: Literal["beginner", "intermediate", "advanced", "native-level"]

class SentenceResponse(BaseModel):
    date: str
    target_sentence: str
    literal_translation: str
    natural_translation: str
    grammatical_highlight: str
    cultural_context: str
    substitution_options: List[str]