import dspy
import logging
from datetime import datetime
from typing import List, Literal, Optional
from core.config import settings

logger = logging.getLogger(__name__)

class WordOfTheDayExplorer(dspy.Signature):
    """
    You are a Master Etymologist and Linguist. Your goal is to provide a 'Deep Dive' Word of the Day.
    You bridge the gap between ancient linguistic roots and modern-day usage, providing 
    translations and context in the user's native language to deepen understanding.
    """
    # Inputs
    date: str = dspy.InputField(desc="The current date (YYYY-MM-DD).")
    target_language: str = dspy.InputField(desc="The language of the 'Word of the Day'.")
    native_language: str = dspy.InputField(desc="The user's primary language for explanations and translations.")
    user_proficiency: Literal["basic", "academic", "poetic", "slang"] = dspy.InputField()
    thematic_focus: Optional[str] = dspy.InputField(default="General", desc="Theme like 'Nature' or 'Technology'.")
    seed: str = dspy.InputField(desc="Entropy string for unique daily selection.")
    user_custom_instructions: Optional[str] = dspy.InputField(default=None, desc="e.g., 'Untranslatable words only'.")

    # Outputs
    word: str = dspy.OutputField(desc="The chosen word.")
    native_translation: str = dspy.OutputField(desc="The closest equivalent in the user's native language.")
    phonetic_and_audio_guide: str = dspy.OutputField(desc="Pronunciation guide.")
    morphology_breakdown: str = dspy.OutputField(desc="Etymological roots (Latin, Greek, etc.).")
    primary_definition: str = dspy.OutputField(desc="Dictionary-style meaning in the native language.")
    the_vibe_check: str = dspy.OutputField(desc="The 'feeling' and social context of the word.")
    modern_usage_sentence: str = dspy.OutputField(desc="Example sentence in target language with native translation.")
    synonym_web: List[str] = dspy.OutputField(desc="3-5 related words or concepts.")

class LinguisticService:
    def __init__(self):
        self.lm = dspy.LM(
            model=f"openai/{settings.MODEL_NAME}",
            api_key=settings.OPENAI_API_KEY,
            api_base=settings.API_BASE,
            cache=False
        )

    async def generate_daily_word(self, data: 'WOTDRequest') -> dspy.Prediction:
        """
        Generates a linguistic deep-dive using DSPy ChainOfThought.
        
        Args:
            data: The request schema containing user preferences.
            
        Returns:
            dspy.Prediction: The generated word object.
        """
        try:
            with dspy.context(lm=self.lm):
                explorer = dspy.ChainOfThought(WordOfTheDayExplorer)
                prediction = explorer(
                    date=datetime.now().strftime("%Y-%m-%d"),
                    target_language=data.target_language,
                    native_language=data.native_language,
                    user_proficiency=data.proficiency,
                    thematic_focus=data.theme,
                    seed=f"fixed_seed_{datetime.now().day}",
                    user_custom_instructions=data.custom_instructions
                )
                return prediction
        except Exception as e:
            logger.error(f"DSPy generation failed: {str(e)}")
            raise e