from fastapi import APIRouter, HTTPException, status
from learning.guides.schemas import (
    GuideRequest, GuideResponse,
    DailyPlannerRequest, DailyPlannerResponse,
    ProjectArchitectRequest, ProjectArchitectResponse,
WhatToLearnRequest, WhatToLearnResponse,
ProjectSuggestorRequest, ProjectSuggestorResponse

)
from learning.guides.services import GuideService
import logging
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/guides",
    tags=["Guides"]
)

@router.post("/task", response_model=GuideResponse, status_code=status.HTTP_200_OK)
async def create_learning_guide(payload: GuideRequest):
    """
    Generate a customized learning guide based on user skill level and goals.
    """
    try:
        result = await GuideService.generate_guide(payload)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate guide: {str(e)}"
        )

@router.post("/daily-plan", response_model=DailyPlannerResponse, status_code=status.HTTP_200_OK)
async def create_daily_plan(payload: DailyPlannerRequest):
    """
    Generate a detailed daily study plan with roadmap, gap analysis, and exercises.
    """
    try:
        return await GuideService.generate_daily_plan(payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Daily Planner Error: {str(e)}"
        )

@router.post("/project-blueprint", response_model=ProjectArchitectResponse)
async def create_project_blueprint(payload: ProjectArchitectRequest):
    """
    Generate a unique, industry-specific project blueprint to achieve mastery.
    """
    try:
        return await GuideService.generate_unique_project(payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Project Generation Error: {str(e)}"
        )

@router.post("/suggest-topics", response_model=WhatToLearnResponse, status_code=status.HTTP_200_OK)
async def get_next_learning_topics(payload: WhatToLearnRequest):
    """
    Personalized recommendation engine to suggest new topics while avoiding 
    previously suggested content and adhering to custom constraints.
    """
    try:
        print(payload)
        return await GuideService.suggest_next_topics(payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Enhanced Topic Suggestion Error: {str(e)}"
        )

@router.post("/suggest-projects", response_model=ProjectSuggestorResponse, status_code=status.HTTP_200_OK)
async def suggest_industry_projects(payload: ProjectSuggestorRequest):
    """
    Generate strategic project use cases for a specific topic and industry.
    """
    try:
        return await GuideService.suggest_projects(payload)
    except Exception as e:
        logger.error(f"Router Error in suggest_projects: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to suggest projects: {str(e)}"
        )