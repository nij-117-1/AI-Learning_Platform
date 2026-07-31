import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class DebateSession(BaseModel):
    """
    ORM-style model representing a debate session.

    In a production system this would be a SQLAlchemy or Beanie document.
    For now it serves as a data contract for future database integration.
    """
    id: Optional[str] = Field(None, description="Unique session identifier")
    topic: str
    theme: str
    persona: str
    stance: str
    debate_style: str
    history: List[Dict[str, str]] = Field(default_factory=list)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    is_active: bool = True
