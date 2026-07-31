from fastapi import APIRouter
from practice.debate.router import router as debate_router

practice_router = APIRouter(prefix="/practice", tags=["Practice Module"])
practice_router.include_router(debate_router)

__all__ = ["practice_router"]
