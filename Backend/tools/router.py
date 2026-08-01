from fastapi import APIRouter

from tools.charts.router import router as charts_router
from tools.creative_assets.router import router as creative_assets_router
from tools.ingredients.router import router as ingredients_router
from tools.prompt_generator.router import router as prompt_generator_router
from tools.social_posts.router import router as social_posts_router

tools_router = APIRouter(prefix="/tools")
tools_router.include_router(charts_router)
tools_router.include_router(creative_assets_router)
tools_router.include_router(ingredients_router)
tools_router.include_router(prompt_generator_router)
tools_router.include_router(social_posts_router)

__all__ = ["tools_router"]
