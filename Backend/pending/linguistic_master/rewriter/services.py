import dspy
import logging
from typing import Dict, Any, Literal
from typing import Optional, Literal, List
from core.config import settings
from .schemas import RewriteRequest

logger = logging.getLogger(__name__)

class TextRewriterSignature(dspy.Signature):
    """
    You are an Expert Content Editor and Copywriter.
    Your task is to rewrite the provided text to improve its quality,
    adjust its tone, or change its structure while preserving the original intent.
    """
    # Inputs
    original_text: str = dspy.InputField(desc="The text that needs to be rewritten.")
    target_tone: str = dspy.InputField(desc="Desired tone (e.g., professional, witty, empathetic, concise).")
    audience: str = dspy.InputField(desc="Who the text is being written for.")
    transformation_goal: Literal["paraphrase", "shorten", "expand", "simplify"] = dspy.InputField(desc="The primary objective of the rewrite.")
    custom_instructions: Optional[str] = dspy.InputField(default=None, desc="Specific constraints or rules.")

    # Outputs
    rationale: str = dspy.OutputField(desc="Explanation of the stylistic changes made.")
    rewritten_text: str = dspy.OutputField(desc="The final polished version of the text.")
    improvements_made: List[str] = dspy.OutputField(desc="A list of specific changes (e.g., 'Removed passive voice').")

class RewriterService:
    def __init__(self):
        self.lm = dspy.LM(
            model=f"openai/{settings.MODEL_NAME}",
            api_key=settings.OPENAI_API_KEY,
            api_base=settings.API_BASE,
            temperature=settings.TEMPERATURE,
            cache=False
        )

    def process_rewrite(self, data: RewriteRequest) -> Dict[str, Any]:
        """
        Executes the DSPy ChainOfThought pipeline.
        
        Args:
            data: The validated rewrite parameters.
        Returns:
            Dictionary containing rewritten content and metadata.
        """
        try:
            with dspy.context(lm=self.lm):
                rewriter = dspy.ChainOfThought(TextRewriterSignature)
                result = rewriter(
                    original_text=data.original_text,
                    target_tone=data.target_tone,
                    audience=data.audience,
                    transformation_goal=data.transformation_goal,
                    custom_instructions=data.custom_instructions or "None"
                )
                logger.info("Successfully processed text rewrite.")
                return result
        except Exception as e:
            logger.error(f"DSPy Execution Error: {str(e)}")
            raise e