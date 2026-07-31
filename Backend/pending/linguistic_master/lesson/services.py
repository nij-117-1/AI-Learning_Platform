import dspy
import logging
from core.config import settings
from .dspy_modules import LanguageLessonGenerator
from .schemas import LessonRequest

logger = logging.getLogger(__name__)

class LessonService:
    def __init__(self):
        self.lm = dspy.LM(
            model=f"openai/{settings.MODEL_NAME}",
            api_key=settings.API_KEY,
            api_base=settings.API_BASE,
            temperature=settings.TEMPERATURE,
            cache=False
        )

    def generate_lesson(self, data: LessonRequest):
        """Generates a pedagogical lesson using DSPy ChainOfThought."""
        try:
            with dspy.context(lm=self.lm):
                tutor = dspy.ChainOfThought(LanguageLessonGenerator)
                prediction = tutor(
                    native_language=data.native_language,
                    target_language=data.target_language,
                    current_level=data.current_level,
                    last_lesson_summary=data.last_lesson_summary,
                    learning_focus=data.learning_focus,
                    complexity_weight=data.complexity_weight,
                    seed=data.seed,
                    user_custom_instruction=data.user_custom_instruction
                )
                return prediction
        except Exception as e:
            logger.error(f"Error generating lesson with DSPy: {str(e)}")
            raise e