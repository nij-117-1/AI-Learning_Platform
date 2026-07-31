import dspy
import logging
from typing import Dict, Any
from core.config import settings
from .schemas import TranslationRequest
from dspy.signatures.signature import Signature
from typing import Optional, Literal

logger = logging.getLogger(__name__)

class ContextualTranslator(dspy.Signature):
    """
    You are a Professional Linguist and Translator.
    Your goal is to translate text accurately while preserving the nuances of tone, 
    cultural context, and specific user instructions.
    """
    # Inputs
    text_to_translate: str = dspy.InputField(desc="The source text that needs translation.")
    source_language: str = dspy.InputField(desc="The language of the input text.")
    target_language: str = dspy.InputField(desc="The language the text should be translated into.")
    tone: Literal["formal", "casual", "business", "poetic", "technical"] = dspy.InputField(desc="The desired style of the translation.")
    reference_material: Optional[str] = dspy.InputField(default=None, desc="Glossary or context snippets to maintain consistency.")
    custom_instructions: Optional[str] = dspy.InputField(default=None, desc="Specific rules (e.g., 'avoid gendered pronouns').")
    
    # Outputs
    rationale: str = dspy.OutputField(desc="Brief explanation of linguistic choices made for this translation.")
    translated_text: str = dspy.OutputField(desc="The final translated content.")
    cultural_notes: Optional[str] = dspy.OutputField(desc="Notes on idioms or cultural adjustments made during translation.")

class TranslatorService:
    def __init__(self):
        self.lm = dspy.LM(
            model=f"openai/{settings.MODEL_NAME}",
            api_key=settings.OPENAI_API_KEY,
            api_base=settings.API_BASE,
            temperature=settings.TEMPERATURE,
            cache=False
        )

    def translate(self, data: TranslationRequest) -> Dict[str, Any]:
        """
        Executes the DSPy ChainOfThought translation.
        
        Args:
            data: The validated translation request schema.
            
        Returns:
            Dict containing the rationale, text, and cultural notes.
        """
        try:
            with dspy.context(lm=self.lm):
                translator = dspy.ChainOfThought(ContextualTranslator)
                response = translator(**data.model_dump())
                return response
        except Exception as e:
            logger.error(f"DSPy Translation Error: {str(e)}")
            raise e