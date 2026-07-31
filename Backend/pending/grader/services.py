import dspy
import base64
import logging
from typing import Dict, Any, Optional
from learning.grader.utils import resize_image
from learning.grader.schemas import HybridUserResponseGrader, GradingResponse
from config import master_llm_config as config

logger = logging.getLogger(__name__)

class GraderService:
    @staticmethod
    def resize_image_from_path(image_path: str) -> bytes:
        """Read image from disk, resize, and return JPEG bytes."""
        try:
            with open(image_path, "rb") as f:
                return resize_image(f.read())
        except Exception as e:
            logger.error(f"Resize error: {str(e)}")
            with open(image_path, "rb") as f:
                return f.read()

    @staticmethod
    async def process_grading_logic(
        processed_bytes: Optional[bytes],
        payload: Dict[str, Any],
        config: Dict[str, Any]
    ) -> GradingResponse:
        """Executes DSPy ChainOfThought logic with optional Image injection."""
        
        img_obj = None
        if processed_bytes:
            base64_str = base64.b64encode(processed_bytes).decode("utf-8")
            image_uri = f"data:image/jpeg;base64,{base64_str}"
            img_obj = dspy.Image(url=image_uri)

        lm = dspy.LM(
            model=f"openai/{config['model_name']}",
            api_key=config['api_key'],
            api_base=config.get('api_base'),
            temperature=config.get('temperature', 0.2)
        )

        with dspy.context(lm=lm):
            grader = dspy.ChainOfThought(HybridUserResponseGrader)
            res = grader(
                scenario=payload['scenario'],
                question_asked=payload['question_asked'],
                target_objective=payload['target_objective'],
                expected_level=payload['expected_level'],
                user_answer_text=payload.get('user_answer_text'),
                user_answer_image=img_obj
            )
            
            return GradingResponse(
                combined_analysis=res.combined_analysis,
                score=float(res.score),
                strengths=res.strengths,
                weaknesses=res.weaknesses,
                detailed_feedback=res.detailed_feedback,
                is_target_met=bool(res.is_target_met)
            )