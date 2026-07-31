import logging
from fastapi import Depends
from core.security import verify_api_key

logger = logging.getLogger(__name__)

__all__ = ["get_debate_service", "verify_api_key"]


def get_debate_service():
    """
    Dependency provider for DebateService.

    Yields:
        DebateService: An initialized service instance.
    """
    from practice.debate.services import DebateService

    service = DebateService()
    try:
        yield service
    finally:
        pass
