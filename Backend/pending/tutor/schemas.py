from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class TutorRequest(BaseModel):
    system_prompt: str = Field(..., description="The persona and pedagogical rules.")
    user_query: str = Field(..., description="The student's specific question or struggle.")
    student_level: str = Field(..., description="Level: Toddler, High School, Expert, etc.")
    learning_style: str = Field(..., description="Preferred framing: analogical, first_principles, etc.")
    current_scenario: str = Field(..., description="Context of learning (e.g. 'preparing for an exam').")
    chat_history: List[ChatMessage] = Field(default_factory=list)
    last_topic_taught: Optional[str] = Field(None, description="Context of the previous lesson.")


class TutorResponse(BaseModel):
    adapted_explanation: str
    concept_analogy: Optional[str] = None
    tutor_feedback: str


class PromptCreateUpdate(BaseModel):
    name: str = Field(..., example="socratic_tutor", description="Unique name for the prompt file.")
    content: str = Field(..., example="You are a Socratic tutor...", description="The system prompt text.")


class PromptResponse(BaseModel):
    name: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
