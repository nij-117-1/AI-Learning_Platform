from fastapi import APIRouter
from learning.explainer.router import router as explainer_router

learning_router = APIRouter(prefix="/learning")
learning_router.include_router(explainer_router)

__all__ = ["learning_router"]
