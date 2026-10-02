import logging
from typing import Any, Dict, List, Literal, Optional
from uuid import uuid4

import dspy

from core.dspy_utils import build_lm, run_predictor
from practice.interview.schemas import (
    AnswerReview,
    InterviewAnswerRequest,
    InterviewAnswerResponse,
    InterviewQuestion,
    InterviewStartRequest,
    InterviewStartResponse,
)

logger = logging.getLogger(__name__)


class InterviewError(Exception):
    """Base exception for interview module failures."""


class GenerationError(InterviewError):
    """Raised when an interview DSPy pipeline fails."""


class SessionManager(dspy.Signature):
    """Choose the next interview action using session performance and remaining time.

    Use follow-ups to probe weak or incomplete answers, increase difficulty after
    strong answers, cover under-tested topics, and end once the question limit or
    interview goals are reached.
    """

    candidate_profile: Dict[str, Any] = dspy.InputField(desc="Candidate's background, experience, and skills.")
    position_details: Dict[str, Any] = dspy.InputField(desc="Target role, company, required skills, and job description.")
    interview_context: Dict[str, Any] = dspy.InputField(desc="Interviewer role, interview type, round, format, and time.")
    session_history: List[Dict[str, Any]] = dspy.InputField(desc="All previous questions, answers, and reviews.")
    progress_state: Dict[str, Any] = dspy.InputField(desc="Current scores, strengths, weak areas, and topic coverage.")
    questions_asked: int = dspy.InputField(desc="How many questions have been asked so far.")
    max_questions: int = dspy.InputField(desc="Maximum number of questions planned.")
    time_remaining_minutes: int = dspy.InputField(desc="Estimated minutes remaining in the interview.")

    next_action: Literal["new_question", "follow_up", "switch_topic", "end_session"] = dspy.OutputField(
        desc="High-level action to take next."
    )
    action_reasoning: str = dspy.OutputField(desc="Brief explanation for the selected action.")
    directive: Dict[str, Any] = dspy.OutputField(desc="Question type, topic, difficulty, focus, tone, and constraints.")


class QuestionGenerator(dspy.Signature):
    """Craft a natural, role-appropriate question that follows the session directive."""

    directive: Dict[str, Any] = dspy.InputField(desc="Session manager directive describing what to ask.")
    candidate_profile: Dict[str, Any] = dspy.InputField(desc="Candidate background and experience.")
    position_details: Dict[str, Any] = dspy.InputField(desc="Target position information.")
    interview_context: Dict[str, Any] = dspy.InputField(desc="Interviewer role, interview type, format, and round.")
    previous_question: Optional[str] = dspy.InputField(default=None, desc="Previous question, when generating a follow-up.")
    previous_answer: Optional[str] = dspy.InputField(default=None, desc="Candidate's previous answer, when relevant.")
    previous_review: Optional[Dict[str, Any]] = dspy.InputField(default=None, desc="Previous answer review, when relevant.")
    all_questions_asked: List[str] = dspy.InputField(desc="Questions already asked; do not repeat them.")

    question: str = dspy.OutputField(desc="A polished interview question.")
    topic: str = dspy.OutputField(desc="Specific topic being tested.")
    difficulty: Literal["easy", "medium", "hard", "expert"] = dspy.OutputField(desc="Question difficulty.")
    expected_keywords: List[str] = dspy.OutputField(desc="Key concepts expected in a strong answer.")
    evaluation_criteria: str = dspy.OutputField(desc="What differentiates a great answer from a poor one.")
    red_flags: List[str] = dspy.OutputField(desc="Concerning patterns in the answer.")
    sample_strong_answer: str = dspy.OutputField(desc="Calibration example of a strong answer.")
    sample_weak_answer: str = dspy.OutputField(desc="Calibration example of a weak answer.")


class AnswerReviewer(dspy.Signature):
    """Evaluate an interview answer fairly and strictly against the question and role level."""

    question: str = dspy.InputField(desc="Question presented to the candidate.")
    candidate_answer: str = dspy.InputField(desc="Candidate's complete answer.")
    expected_keywords: List[str] = dspy.InputField(desc="Key concepts expected.")
    evaluation_criteria: str = dspy.InputField(desc="Criteria distinguishing a strong answer.")
    red_flags: List[str] = dspy.InputField(desc="Concerning answer patterns to watch for.")
    sample_strong_answer: str = dspy.InputField(desc="Calibration example of a strong answer.")
    sample_weak_answer: str = dspy.InputField(desc="Calibration example of a weak answer.")
    position_level: str = dspy.InputField(desc="Seniority level used to calibrate expectations.")
    question_type: str = dspy.InputField(desc="Interview category.")
    difficulty: str = dspy.InputField(desc="Question difficulty.")

    overall_score: float = dspy.OutputField(desc="Overall answer score from 0.0 to 10.0.")
    technical_accuracy: float = dspy.OutputField(desc="Technical accuracy score from 0.0 to 10.0.")
    completeness: float = dspy.OutputField(desc="Completeness score from 0.0 to 10.0.")
    clarity_score: float = dspy.OutputField(desc="Clarity score from 0.0 to 10.0.")
    depth_score: float = dspy.OutputField(desc="Depth score from 0.0 to 10.0.")
    strengths: List[str] = dspy.OutputField(desc="What the candidate did well.")
    weaknesses: List[str] = dspy.OutputField(desc="What the candidate should improve.")
    missed_keywords: List[str] = dspy.OutputField(desc="Expected concepts not covered.")
    red_flags_detected: List[str] = dspy.OutputField(desc="Red flags present in the answer.")
    improved_answer: str = dspy.OutputField(desc="Example of a stronger, improved answer.")
    weak_topics_identified: List[str] = dspy.OutputField(desc="Topics the candidate should study further.")
    recommendation: Literal["move_on", "follow_up", "switch_topic"] = dspy.OutputField(
        desc="Recommended next step for the session manager."
    )
    follow_up_suggestion: str = dspy.OutputField(desc="Suggested direction if a follow-up is recommended.")


class ProgressTracker(dspy.Signature):
    """Update the candidate performance profile after the latest reviewed answer."""

    current_profile: Dict[str, Any] = dspy.InputField(desc="Current candidate progress state.")
    latest_review: Dict[str, Any] = dspy.InputField(desc="Structured review of the most recent answer.")
    question_topic: str = dspy.InputField(desc="Topic of the latest question.")
    question_type: str = dspy.InputField(desc="Category of the latest question.")

    updated_profile: Dict[str, Any] = dspy.OutputField(
        desc="Updated overall score, answered count, strengths, weak areas, topic/type scores, and next topics."
    )
    performance_trend: Literal["improving", "stable", "declining"] = dspy.OutputField(
        desc="Performance trend across the interview so far."
    )


class InterviewService:
    """Business layer orchestrating the interview DSPy signatures."""

    def __init__(self) -> None:
        self.lm = build_lm(temperature=0.4, cache=False)

    @staticmethod
    def _as_dict(value: object) -> Dict[str, Any]:
        """Return a dictionary for a DSPy value, or an empty dictionary."""
        return value if isinstance(value, dict) else {}

    @staticmethod
    def _as_list(value: object) -> List[str]:
        """Normalize an arbitrary DSPy value into a list of strings."""
        if value is None:
            return []
        if isinstance(value, (list, tuple)):
            return [str(item) for item in value]
        return [str(value)]

    @staticmethod
    def _as_str(value: object, default: str = "") -> str:
        """Normalize an arbitrary DSPy value into a string."""
        return default if value is None else str(value)

    @staticmethod
    def _as_score(value: object, default: float = 0.0) -> float:
        """Coerce a value to a score in the range 0-10."""
        try:
            return max(0.0, min(10.0, float(value)))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _choose(value: object, allowed: tuple[str, ...], default: str) -> str:
        """Select a normalized value from an allowed set."""
        candidate = str(value).strip().lower()
        return candidate if candidate in allowed else default

    @classmethod
    def _progress_defaults(cls, progress: Dict[str, Any]) -> Dict[str, Any]:
        """Add expected progress fields while preserving client-provided state."""
        state = dict(progress)
        state.setdefault("overall_score", 0.0)
        state.setdefault("questions_answered", 0)
        state.setdefault("weak_areas", [])
        state.setdefault("strong_areas", [])
        state.setdefault("topics_covered", [])
        state.setdefault("topic_scores", {})
        state.setdefault("type_scores", {})
        state.setdefault("recommended_next_topics", [])
        state.setdefault("confidence_level", "not_assessed")
        return state

    @classmethod
    def _build_review(cls, result: object) -> AnswerReview:
        """Normalize raw reviewer output into a validated response model.

        Args:
            result: Raw DSPy prediction from the answer reviewer.

        Returns:
            AnswerReview: Validated and bounded assessment.
        """
        recommendation = cls._choose(
            getattr(result, "recommendation", "move_on"),
            ("move_on", "follow_up", "switch_topic"),
            "move_on",
        )
        return AnswerReview(
            overall_score=cls._as_score(getattr(result, "overall_score", 0)),
            technical_accuracy=cls._as_score(getattr(result, "technical_accuracy", 0)),
            completeness=cls._as_score(getattr(result, "completeness", 0)),
            clarity_score=cls._as_score(getattr(result, "clarity_score", 0)),
            depth_score=cls._as_score(getattr(result, "depth_score", 0)),
            strengths=cls._as_list(getattr(result, "strengths", [])),
            weaknesses=cls._as_list(getattr(result, "weaknesses", [])),
            missed_keywords=cls._as_list(getattr(result, "missed_keywords", [])),
            red_flags_detected=cls._as_list(getattr(result, "red_flags_detected", [])),
            improved_answer=cls._as_str(getattr(result, "improved_answer", "")),
            weak_topics_identified=cls._as_list(getattr(result, "weak_topics_identified", [])),
            recommendation=recommendation,  # type: ignore[arg-type]
            follow_up_suggestion=cls._as_str(getattr(result, "follow_up_suggestion", "")),
        )

    @classmethod
    def _build_question(cls, result: object, directive: Dict[str, Any]) -> InterviewQuestion:
        """Normalize raw question generator output into a validated question.

        Args:
            result: Raw DSPy prediction from the question generator.
            directive: Session manager directive for this question.

        Returns:
            InterviewQuestion: Validated question with reviewer calibration data.
        """
        question_type = cls._choose(
            directive.get("question_type", "technical"),
            ("technical", "behavioral", "system_design", "coding", "hr", "leadership", "domain"),
            "technical",
        )
        difficulty = cls._choose(
            getattr(result, "difficulty", directive.get("difficulty", "medium")),
            ("easy", "medium", "hard", "expert"),
            "medium",
        )
        return InterviewQuestion(
            question=cls._as_str(getattr(result, "question", "Describe your approach to this role.")),
            question_type=question_type,  # type: ignore[arg-type]
            topic=cls._as_str(getattr(result, "topic", directive.get("topic", "General"))),
            difficulty=difficulty,  # type: ignore[arg-type]
            expected_keywords=cls._as_list(getattr(result, "expected_keywords", [])),
            evaluation_criteria=cls._as_str(getattr(result, "evaluation_criteria", "")),
            red_flags=cls._as_list(getattr(result, "red_flags", [])),
            sample_strong_answer=cls._as_str(getattr(result, "sample_strong_answer", "")),
            sample_weak_answer=cls._as_str(getattr(result, "sample_weak_answer", "")),
        )

    def _generate_question(
        self,
        directive: Dict[str, Any],
        candidate_profile: Dict[str, Any],
        position_details: Dict[str, Any],
        interview_context: Dict[str, Any],
        history: List[Dict[str, Any]],
    ) -> InterviewQuestion:
        """Generate a question from a manager directive and session context.

        Args:
            directive: Strategic question-generation instructions.
            candidate_profile: Candidate background and experience.
            position_details: Role information used to tailor the question.
            interview_context: Interviewer and interview format details.
            history: Completed questions, answers, and reviews.

        Returns:
            InterviewQuestion: Generated question with evaluation guidance.
        """
        previous_entry = history[-1] if history else {}
        previous_question = self._as_dict(previous_entry.get("question"))
        previous_review = self._as_dict(previous_entry.get("review"))
        result = run_predictor(
            QuestionGenerator,
            self.lm,
            directive=directive,
            candidate_profile=candidate_profile,
            position_details=position_details,
            interview_context=interview_context,
            previous_question=self._as_str(previous_question.get("question")) or None,
            previous_answer=self._as_str(previous_entry.get("candidate_answer")) or None,
            previous_review=previous_review or None,
            all_questions_asked=[
                self._as_str(self._as_dict(entry.get("question")).get("question"))
                for entry in history
            ],
        )
        return self._build_question(result, directive)

    def _manage_session(
        self,
        *,
        candidate_profile: Dict[str, Any],
        position_details: Dict[str, Any],
        interview_context: Dict[str, Any],
        session_history: List[Dict[str, Any]],
        progress_state: Dict[str, Any],
        questions_asked: int,
        max_questions: int,
        time_remaining_minutes: int,
        initial: bool = False,
    ) -> tuple[str, str, Dict[str, Any]]:
        """Ask the session manager to choose the next action and question directive.

        Args:
            candidate_profile: Candidate background and experience.
            position_details: Target position information.
            interview_context: Interview format and interviewer details.
            session_history: Previous questions, answers, and reviews.
            progress_state: Current performance summary.
            questions_asked: Number of questions already asked.
            max_questions: Session question limit.
            time_remaining_minutes: Remaining interview time.
            initial: Whether this is the opening decision.

        Returns:
            tuple[str, str, Dict[str, Any]]: Selected action, reasoning, and directive.
        """
        result = run_predictor(
            SessionManager,
            self.lm,
            candidate_profile=candidate_profile,
            position_details=position_details,
            interview_context=interview_context,
            session_history=session_history,
            progress_state=progress_state,
            questions_asked=questions_asked,
            max_questions=max_questions,
            time_remaining_minutes=time_remaining_minutes,
        )
        action = self._choose(
            getattr(result, "next_action", "new_question"),
            ("new_question", "follow_up", "switch_topic", "end_session"),
            "new_question",
        )
        if initial and action == "end_session":
            action = "new_question"
        directive = self._as_dict(getattr(result, "directive", {}))
        directive.setdefault("action", "follow_up" if action == "follow_up" else "new_question")
        directive.setdefault("question_type", "technical")
        directive.setdefault("topic", "Role-specific skills")
        directive.setdefault("difficulty", "medium")
        return action, self._as_str(getattr(result, "action_reasoning", "")), directive

    async def start_interview(self, data: InterviewStartRequest) -> InterviewStartResponse:
        """Create a session identifier, choose the opening direction, and generate its question.

        Args:
            data: Validated interview start information.

        Returns:
            InterviewStartResponse: The initial question and state to persist.

        Raises:
            GenerationError: If a DSPy pipeline fails.
        """
        try:
            progress = self._progress_defaults({})
            action, reasoning, directive = self._manage_session(
                candidate_profile=data.candidate_profile,
                position_details=data.position_details,
                interview_context=data.interview_context,
                session_history=[],
                progress_state=progress,
                questions_asked=0,
                max_questions=data.max_questions,
                time_remaining_minutes=data.time_remaining_minutes,
                initial=True,
            )
            question = self._generate_question(
                directive,
                data.candidate_profile,
                data.position_details,
                data.interview_context,
                [],
            )
            logger.info("Started interview session for position '%s'", data.position_details)
            return InterviewStartResponse(
                session_id=str(uuid4()),
                next_action=action,  # type: ignore[arg-type]
                action_reasoning=reasoning,
                directive=directive,
                question=question,
                progress_state=progress,
                questions_asked=1,
                max_questions=data.max_questions,
                time_remaining_minutes=data.time_remaining_minutes,
            )
        except Exception as exc:
            logger.error("Interview start failed: %s", exc, exc_info=True)
            raise GenerationError("Unable to start the interview session.") from exc

    async def submit_answer(self, data: InterviewAnswerRequest) -> InterviewAnswerResponse:
        """Review an answer, update progress, and prepare the next question if appropriate.

        Args:
            data: Answer and client-persisted session context.

        Returns:
            InterviewAnswerResponse: Review, progress, session action, and optional next question.

        Raises:
            GenerationError: If a DSPy pipeline fails.
        """
        try:
            current = data.current_question
            reviewer_result = run_predictor(
                AnswerReviewer,
                self.lm,
                question=current.question,
                candidate_answer=data.candidate_answer,
                expected_keywords=current.expected_keywords,
                evaluation_criteria=current.evaluation_criteria,
                red_flags=current.red_flags,
                sample_strong_answer=current.sample_strong_answer,
                sample_weak_answer=current.sample_weak_answer,
                position_level=self._as_str(data.position_details.get("level", "unspecified")),
                question_type=current.question_type,
                difficulty=current.difficulty,
            )
            review = self._build_review(reviewer_result)
            tracker_result = run_predictor(
                ProgressTracker,
                self.lm,
                current_profile=self._progress_defaults(data.progress_state),
                latest_review=review.model_dump(),
                question_topic=current.topic,
                question_type=current.question_type,
            )
            progress = self._progress_defaults(self._as_dict(getattr(tracker_result, "updated_profile", {})))
            trend = self._choose(
                getattr(tracker_result, "performance_trend", "stable"),
                ("improving", "stable", "declining"),
                "stable",
            )
            history = [*data.session_history, {
                "question": current.model_dump(),
                "candidate_answer": data.candidate_answer,
                "review": review.model_dump(),
            }]
            action, reasoning, directive = self._manage_session(
                candidate_profile=data.candidate_profile,
                position_details=data.position_details,
                interview_context=data.interview_context,
                session_history=history,
                progress_state=progress,
                questions_asked=data.questions_asked,
                max_questions=data.max_questions,
                time_remaining_minutes=data.time_remaining_minutes,
            )
            if data.questions_asked >= data.max_questions or data.time_remaining_minutes <= 0:
                action = "end_session"

            next_question: Optional[InterviewQuestion] = None
            if action != "end_session":
                next_question = self._generate_question(
                    directive,
                    data.candidate_profile,
                    data.position_details,
                    data.interview_context,
                    history,
                )
            logger.info("Reviewed answer for interview session %s (score=%.1f)", data.session_id, review.overall_score)
            return InterviewAnswerResponse(
                session_id=data.session_id,
                review=review,
                progress_state=progress,
                performance_trend=trend,  # type: ignore[arg-type]
                session_history=history,
                next_action=action,  # type: ignore[arg-type]
                action_reasoning=reasoning,
                directive=directive,
                next_question=next_question,
                questions_asked=data.questions_asked + (1 if next_question is not None else 0),
                max_questions=data.max_questions,
                time_remaining_minutes=data.time_remaining_minutes,
                is_complete=action == "end_session",
            )
        except Exception as exc:
            logger.error("Interview answer processing failed: %s", exc, exc_info=True)
            raise GenerationError("Unable to review the interview answer.") from exc
