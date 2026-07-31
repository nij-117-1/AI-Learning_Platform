from fastapi import APIRouter
from learning.explainer.router import router as explainer_router
from learning.roadmap.router import router as roadmap_router

learning_router = APIRouter(prefix="/learning")
learning_router.include_router(explainer_router)
learning_router.include_router(roadmap_router)

__all__ = ["learning_router"]
