from fastapi import APIRouter
from practice.clarity_trainer.router import router as clarity_trainer_router
from practice.debate.router import router as debate_router
from practice.guess_game.router import router as guess_game_router
from practice.negotiation.router import router as negotiation_router
from practice.observation_trainer.router import router as observation_trainer_router
from practice.testing_portal.router import router as testing_portal_router

practice_router = APIRouter(prefix="/practice", tags=["Practice Module"])
practice_router.include_router(clarity_trainer_router)
practice_router.include_router(debate_router)
practice_router.include_router(guess_game_router)
practice_router.include_router(negotiation_router)
practice_router.include_router(observation_trainer_router)
practice_router.include_router(testing_portal_router)

__all__ = ["practice_router"]
