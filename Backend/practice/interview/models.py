from datetime import UTC, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from practice.interview.schemas import InterviewQuestion


class InterviewSession(BaseModel):
    """Client-persistable interview session model for future database storage."""

    id: Optional[str] = Field(default=None, description="Unique interview session identifier.")
    candidate_profile: Dict[str, Any] = Field(default_factory=dict)
    position_details: Dict[str, Any] = Field(default_factory=dict)
    interview_context: Dict[str, Any] = Field(default_factory=dict)
    session_history: List[Dict[str, Any]] = Field(default_factory=list)
    progress_state: Dict[str, Any] = Field(default_factory=dict)
    current_question: Optional[InterviewQuestion] = None
    questions_asked: int = 0
    max_questions: int = 8
    time_remaining_minutes: int = 45
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
