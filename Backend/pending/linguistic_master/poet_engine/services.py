import dspy
import logging
from core.config import settings
from .schemas import ConceptRequest
from typing import Literal, Optional

logger = logging.getLogger(__name__)

class PoeticLanguageExplainer(dspy.Signature):
    """
    You are a Poetic Philologist and Sufi-inspired Linguist. 
    Your goal is to bridge cultural gaps by explaining the 'Soul' of a word.
    You translate not just words, but the historical and emotional weight they carry, 
    adapting the explanation to the user's native language.
    """
    
    # Inputs
    target_language: str = dspy.InputField(desc="The source language of the concept (e.g., Urdu, Persian, Japanese).")
    native_language: str = dspy.InputField(desc="The user's primary language for the explanation and translation.")
    concept_word: str = dspy.InputField(desc="The specific word or abstract concept (e.g., 'Ishq', 'Wabi-sabi').")
    poetic_style: Literal["Shayari/Couplet", "Haiku", "Metaphorical Prose", "Ghazal-style"] = dspy.InputField()
    user_mood: Optional[str] = dspy.InputField(default="mystical", desc="The emotional tone for the generation.")
    user_custom_instruction: Optional[str] = dspy.InputField(default=None, desc="Specific constraints like nature metaphors or urban settings.")

    # Outputs
    etymological_soul: str = dspy.OutputField(desc="The cultural and historical origin of the word.")
    original_poetry: str = dspy.OutputField(desc="The poetic piece in the target_language.")
    soulful_translation: str = dspy.OutputField(desc="A deep translation into the user's native_language.")
    philosophical_reflection: str = dspy.OutputField(desc="Connection of the word to the universal human experience.")
    visual_metaphor: str = dspy.OutputField(desc="A vivid description of a scene representing this concept.")
class PoetService:
    def __init__(self):
        self.lm =  dspy.LM(
            model=f"openai/{settings.MODEL_NAME}",
            api_key=settings.OPENAI_API_KEY,
            api_base=settings.API_BASE,
            temperature=settings.TEMPERATURE,
            cache=False
        )

    def generate_explanation(self, data: ConceptRequest):
        """Generates a poetic explanation using DSPy Chain of Thought."""
        logger.info(f"Generating poetic insight for: {data.concept_word}")
        
        with dspy.context(lm=self.lm):
            explainer = dspy.ChainOfThought(PoeticLanguageExplainer)
            try:
                prediction = explainer(
                    target_language=data.target_language,
                    native_language=data.native_language,
                    concept_word=data.concept_word,
                    poetic_style=data.poetic_style,
                    user_mood=data.user_mood,
                    user_custom_instruction=data.user_custom_instruction
                )
                return prediction
            except Exception as e:
                logger.error(f"DSPy Error: {str(e)}")
                raise e