from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

QuestionType = Literal[
    "technical",
    "behavioral",
    "system_design",
    "coding",
    "hr",
    "leadership",
    "domain",
]
Difficulty = Literal["easy", "medium", "hard", "expert"]
InterviewAction = Literal["new_question", "follow_up", "switch_topic", "end_session"]
ReviewRecommendation = Literal["move_on", "follow_up", "switch_topic"]
PerformanceTrend = Literal["improving", "stable", "declining"]


class InterviewQuestion(BaseModel):
    """Interview question and grading context generated for a candidate."""

    question: str = Field(..., min_length=1, description="Question presented to the candidate.")
    question_type: QuestionType = Field(..., description="Interview question category.")
    topic: str = Field(..., description="Specific skill or topic being tested.")
    difficulty: Difficulty = Field(..., description="Question difficulty.")
    expected_keywords: List[str] = Field(default_factory=list, description="Concepts expected in a strong answer.")
    evaluation_criteria: str = Field(..., description="Criteria used to evaluate the answer.")
    red_flags: List[str] = Field(default_factory=list, description="Concerning answer patterns.")
    sample_strong_answer: str = Field(..., description="Calibration example for a strong answer.")
    sample_weak_answer: str = Field(..., description="Calibration example for a weak answer.")


class InterviewStartRequest(BaseModel):
    """Inputs required to start an interview practice session."""

    candidate_profile: Dict[str, Any] = Field(..., description="Candidate background, skills, and experience.")
    position_details: Dict[str, Any] = Field(..., description="Target role, company, and required qualifications.")
    interview_context: Dict[str, Any] = Field(..., description="Interviewer role, interview format, and round.")
    max_questions: int = Field(default=8, ge=1, le=50, description="Maximum questions planned for this session.")
    time_remaining_minutes: int = Field(default=45, ge=1, description="Available interview time in minutes.")


class InterviewAnswerRequest(BaseModel):
    """Candidate answer and client-persisted context for the active session."""

    session_id: str = Field(..., min_length=1, description="Identifier returned when the session was started.")
    candidate_profile: Dict[str, Any] = Field(..., description="Candidate background and experience.")
    position_details: Dict[str, Any] = Field(..., description="Target position and role requirements.")
    interview_context: Dict[str, Any] = Field(..., description="Interview format and interviewer context.")
    current_question: InterviewQuestion = Field(..., description="Question the candidate is answering.")
    candidate_answer: str = Field(..., min_length=1, description="Candidate's complete answer.")
    session_history: List[Dict[str, Any]] = Field(default_factory=list, description="Previous questions, answers, and reviews.")
    progress_state: Dict[str, Any] = Field(default_factory=dict, description="Candidate progress accumulated so far.")
    questions_asked: int = Field(..., ge=1, description="Number of questions asked, including the current question.")
    max_questions: int = Field(..., ge=1, le=50, description="Maximum questions planned for this session.")
    time_remaining_minutes: int = Field(..., ge=0, description="Estimated interview time remaining.")


class AnswerReview(BaseModel):
    """Structured assessment of a candidate answer."""

    overall_score: float = Field(..., ge=0, le=10)
    technical_accuracy: float = Field(..., ge=0, le=10)
    completeness: float = Field(..., ge=0, le=10)
    clarity_score: float = Field(..., ge=0, le=10)
    depth_score: float = Field(..., ge=0, le=10)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    missed_keywords: List[str] = Field(default_factory=list)
    red_flags_detected: List[str] = Field(default_factory=list)
    improved_answer: str
    weak_topics_identified: List[str] = Field(default_factory=list)
    recommendation: ReviewRecommendation
    follow_up_suggestion: str


class InterviewStartResponse(BaseModel):
    """Initial interview question and state to persist on the client."""

    session_id: str
    next_action: InterviewAction
    action_reasoning: str
    directive: Dict[str, Any] = Field(default_factory=dict)
    question: Optional[InterviewQuestion] = None
    progress_state: Dict[str, Any]
    questions_asked: int = 0
    max_questions: int
    time_remaining_minutes: int
    status: str = "success"


class InterviewAnswerResponse(BaseModel):
    """Answer review, updated progress, and the next interview step."""

    session_id: str
    review: AnswerReview
    progress_state: Dict[str, Any]
    performance_trend: PerformanceTrend
    session_history: List[Dict[str, Any]]
    next_action: InterviewAction
    action_reasoning: str
    directive: Dict[str, Any] = Field(default_factory=dict)
    next_question: Optional[InterviewQuestion] = None
    questions_asked: int
    max_questions: int
    time_remaining_minutes: int
    is_complete: bool
    status: str = "success"
