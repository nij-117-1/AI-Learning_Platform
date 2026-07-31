from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class LessonRequest(BaseModel):
    native_language: str = Field(..., example="English")
    target_language: str = Field(..., example="Japanese")
    current_level: Literal["A1", "A2", "B1", "B2", "C1", "C2"]
    last_lesson_summary: Optional[str] = None
    learning_focus: Literal["Grammar", "Vocabulary", "Conversation", "Culture", "Pronunciation"]
    complexity_weight: Literal["Low", "Medium", "High"]
    seed: str
    user_custom_instruction: Optional[str] = None

class VocabularyItem(BaseModel):
    word: str
    ipa: str
    translation: str
    example: str

class LessonResponse(BaseModel):
    header: str
    comparative_analysis: str
    deep_dive: str
    vocabulary: List[dict]
    practice: List[str]
    nuance: str
    homework: str