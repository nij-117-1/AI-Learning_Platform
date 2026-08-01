from fastapi import APIRouter
from practice.debate.router import router as debate_router
from practice.testing_portal.router import router as testing_portal_router

practice_router = APIRouter(prefix="/practice")
practice_router.include_router(debate_router)
practice_router.include_router(testing_portal_router)

__all__ = ["practice_router"]
