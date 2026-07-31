import dspy
import logging
from datetime import datetime
from typing import List, Literal
from core.config import settings
from .schemas import SentenceResponse

logger = logging.getLogger(__name__)

class SentenceOfTheDaySignature(dspy.Signature):
    """
    You are a Cultural Linguistic Guide. Your goal is to provide a 'Sentence of the Day' 
    that captures the soul of the target language. You focus on idiomatic expressions, 
    proverbs, or sophisticated conversational structures that don't always translate literally.
    """
    # Inputs
    date: str = dspy.InputField(desc="YYYY-MM-DD")
    target_language: str = dspy.InputField(desc="The language the user is learning.")
    native_language: str = dspy.InputField(desc="The user's primary language.")
    context_setting: Literal["business", "casual", "literary", "romantic", "travel"] = dspy.InputField()
    complexity_level: Literal["beginner", "intermediate", "advanced", "native-level"] = dspy.InputField()
    seed: str = dspy.InputField(desc="Entropy string for variety.")

    # Outputs
    target_sentence: str = dspy.OutputField(desc="The sentence in the target language.")
    literal_translation: str = dspy.OutputField(desc="Word-for-word translation in native language.")
    natural_translation: str = dspy.OutputField(desc="The equivalent 'meaning-based' translation in native language.")
    grammatical_highlight: str = dspy.OutputField(desc="Explanation of a specific rule or tense used in the sentence.")
    cultural_context: str = dspy.OutputField(desc="Where and why a native would say this. Any hidden social taboos or nuances.")
    substitution_options: List[str] = dspy.OutputField(desc="2-3 variations of the sentence by changing one key word.")

class SentenceService:
    def __init__(self):
        self.lm =dspy.LM(
            model=f"openai/{settings.MODEL_NAME}",
            api_key=settings.OPENAI_API_KEY,
            api_base=settings.API_BASE,
            temperature=settings.TEMPERATURE,
            cache=False
        )

    def generate_daily_sentence(
        self, 
        target: str, 
        native: str, 
        context: str, 
        level: str
    ) -> SentenceResponse:
        """
        Generates a culturally relevant sentence using DSPy.
        
        Args:
            target: The language being learned.
            native: The user's primary language.
            context: The situational setting.
            level: Proficiency level.

        Returns:
            SentenceResponse: Validated Pydantic model with linguistic data.
        """
        try:
            with dspy.context(lm=self.lm):
                generator = dspy.Predict(SentenceOfTheDaySignature)
                today = datetime.now().strftime("%Y-%m-%d")
                
                response = generator(
                    date=today,
                    target_language=target,
                    native_language=native,
                    context_setting=context,
                    complexity_level=level,
                    seed=f"{today}_{target}"
                )

                return SentenceResponse(
                    date=today,
                    target_sentence=response.target_sentence,
                    literal_translation=response.literal_translation,
                    natural_translation=response.natural_translation,
                    grammatical_highlight=response.grammatical_highlight,
                    cultural_context=response.cultural_context,
                    substitution_options=response.substitution_options
                )
        except Exception as e:
            logger.error(f"Error generating daily sentence: {str(e)}")
            raise e