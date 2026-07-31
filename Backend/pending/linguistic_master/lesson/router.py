from fastapi import APIRouter, HTTPException, Depends
from .schemas import LessonRequest, LessonResponse
from .services import LessonService

router = APIRouter(prefix="/lessons", tags=["Lessons"])

@router.post("/generate", response_model=LessonResponse)
async def create_lesson(payload: LessonRequest):
    """
    Generates a scaffolded AI language lesson based on user profile and theme.
    """
    service = LessonService()
    try:
        lesson = service.generate_lesson(payload)
        return LessonResponse(
            header=lesson.lesson_header,
            comparative_analysis=lesson.comparative_analysis,
            deep_dive=lesson.concept_deep_dive,
            vocabulary=lesson.thematic_vocabulary,
            practice=lesson.practice_suite,
            nuance=lesson.cultural_nuance,
            homework=lesson.homework_mission
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate pedagogical content.")