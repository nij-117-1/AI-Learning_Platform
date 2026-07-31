from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal

class LanguageSessionRequest(BaseModel):
    user_input: str = Field(..., example="How do I order a coffee politely?")
    text_to_translate: Optional[str] = Field(None, example="Give me a coffee.")
    target_lang: str = Field("Spanish", example="Japanese")
    user_level: Literal["Beginner", "Intermediate", "Advanced"] = "Beginner"
    chat_history: List[Dict[str, str]] = Field(default_factory=list)
    seed_context: str = Field("Standard Learning", description="The core teaching persona.")

class LanguageSessionResponse(BaseModel):
    answer_message: str
    original_text: Optional[str]
    translated_text: str
    points_to_keep_in_mind: List[str]
    what_to_learn_today_suggestion: Optional[str]
    rationale: Optional[str] = Field(None, description="Internal reasoning for the response.")

class RegisterSpectrum(BaseModel):
    intimate: str
    casual: str
    professional: str
    formal: str

class IdiomDecodeRequest(BaseModel):
    target_expression: str = Field(..., example="To cut corners")
    user_input: str = Field(..., example="Can I use this for my homework?")
    chat_history: List[Dict[str, str]] = Field(default_factory=list)
    user_l1_equivalent: Optional[str] = Field(None, example="Escatimar")
    seed_context: str = Field("General Pragmatics", example="British English")

class IdiomDecodeResponse(BaseModel):
    rationale: str
    literal_breakdown: str
    cultural_logic: str
    register_spectrum: Dict[str, str]  # Map of social contexts
    emotional_valence: str
    false_friend_warning: bool
    usage_correction: str