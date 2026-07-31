import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# --- MCQ Models ---
class MCQOption(BaseModel):
    A: str
    B: str
    C: str
    D: str

class MCQQuestion(BaseModel):
    id: str
    text: str
    options: MCQOption
    correct: str  # Changed from Literal
    explanation: str

class AssessmentRequest(BaseModel):
    target_language: str = Field(..., example="Spanish")
    native_language: str = Field("English", example="English")
    level: str  # Changed from Literal
    num_questions: int = Field(ge=1, le=10, default=5)
    scenario: str = Field(..., example="Booking a hotel room")
    user_details: str = Field(..., example="A business traveler")
    seed: str = Field(default="random_seed_123")
    custom_instructions: Optional[str] = None

class AssessmentResponse(BaseModel):
    assessment_title: str
    level_rationale: str
    questions: List[MCQQuestion]

# --- Fill in the Blank Models ---
class FIBQuestion(BaseModel):
    sentence: str
    correct_word: str
    hint: str
    context_clue: str

class FIBRequest(BaseModel):
    target_language: str
    level: str  # Changed from Literal
    num_questions: int = Field(default=3, ge=1, le=10)
    scenario: str
    user_details: str
    seed: str = "default_seed"

class FIBResponse(BaseModel):
    questions: List[FIBQuestion]

# --- Evaluation Models ---
class EvaluationRequest(BaseModel):
    sentence_context: str
    correct_word: str
    user_answer: str

class EvaluationResponse(BaseModel):
    is_correct: bool
    status: str  # Changed from Literal
    feedback: str
    improvement_tip: Optional[str] = None

# --- Translation Models ---
class TranslationChallengeRequest(BaseModel):
    target_language: str = Field(..., example="Japanese")
    native_language: str = Field("English")
    level: str  # Changed from Literal
    scenario: str = Field(..., example="Discussing skyscraper blueprints")
    user_persona: str = Field(..., example="An International Architect")
    seed: str = Field(default="arch_v105")
    custom_instructions: Optional[str] = None

class TranslationChallengeResponse(BaseModel):
    test_type: str
    challenge_instruction: str
    source_text: str
    correct_reference: str
    vocabulary_highlights: List[str]
    cultural_tip: Optional[str] = None

# --- Roleplay Models ---
class ChatMessage(BaseModel):
    role: str  # Changed from Literal
    content: str

class RoleplayRequest(BaseModel):
    target_language: str
    level: str  # Changed from Literal
    scenario: str = Field(..., example="Ordering food at a busy Parisian café")
    user_persona: str = Field(..., example="A hungry tourist in a hurry")
    chat_history: List[ChatMessage] = Field(default_factory=list)
    user_latest_response: str
    seed: str = Field(default="grumpy_waiter_v1")

class RoleplayResponse(BaseModel):
    linguistic_critique: str
    fluency_score: int = Field(ge=1, le=10)
    ai_character_response: str
    suggested_strategies: List[str]
    is_goal_achieved: bool