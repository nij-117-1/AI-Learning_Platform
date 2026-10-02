import logging
from typing import NoReturn

from fastapi import APIRouter, Depends, HTTPException, status

from core.security import verify_api_key
from practice.interview.dependencies import get_interview_service
from practice.interview.schemas import (
    InterviewAnswerRequest,
    InterviewAnswerResponse,
    InterviewStartRequest,
    InterviewStartResponse,
)
from practice.interview.services import GenerationError, InterviewError, InterviewService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/interview", tags=["Interview Practice"])


class InterviewHTTPError(HTTPException):
    """Base HTTP exception for the interview module."""


class InterviewProcessingError(InterviewHTTPError):
    """Raised when an interview DSPy pipeline cannot complete."""


def _raise_processing_error(action: str, exc: InterviewError) -> NoReturn:
    """Log a domain error and raise the module's HTTP processing exception.

    Args:
        action: Human-readable operation that failed.
        exc: Underlying interview domain error.

    Raises:
        InterviewProcessingError: Always.
    """
    logger.error("Interview module failed to %s: %s", action, exc)
    raise InterviewProcessingError(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to {action}.",
    ) from exc


@router.post("/start", response_model=InterviewStartResponse)
async def start_interview(
    payload: InterviewStartRequest,
    service: InterviewService = Depends(get_interview_service),
    _: str = Depends(verify_api_key),
) -> InterviewStartResponse:
    """Start an interview and generate its opening question.

    Args:
        payload: Candidate, role, and interview configuration.
        service: Injected interview service.
        _: API key dependency.

    Returns:
        InterviewStartResponse: Initial question and state for client persistence.

    Raises:
        InterviewProcessingError: If the interview pipeline fails.
    """
    try:
        return await service.start_interview(payload)
    except GenerationError as exc:
        _raise_processing_error("start the interview", exc)


@router.post("/answer", response_model=InterviewAnswerResponse)
async def submit_answer(
    payload: InterviewAnswerRequest,
    service: InterviewService = Depends(get_interview_service),
    _: str = Depends(verify_api_key),
) -> InterviewAnswerResponse:
    """Review a candidate response and return updated progress and the next step.

    Args:
        payload: Answer and the session context persisted by the client.
        service: Injected interview service.
        _: API key dependency.

    Returns:
        InterviewAnswerResponse: Answer review and optional next question.

    Raises:
        InterviewProcessingError: If the interview pipeline fails.
    """
    try:
        return await service.submit_answer(payload)
    except GenerationError as exc:
        _raise_processing_error("process the interview answer", exc)
