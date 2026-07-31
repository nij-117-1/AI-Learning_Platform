import logging
from pathlib import Path
from typing import List

import dspy
import yaml

from fastapi import HTTPException, status

from config import master_llm_config as config
from learning.tutor.models import PromptFile
from learning.tutor.schemas import TutorRequest, TutorResponse, PromptCreateUpdate

logger = logging.getLogger(__name__)


class AdaptiveTutorSignature(dspy.Signature):
    system_prompt: str = dspy.InputField(desc="The persona and pedagogical rules (e.g., Socratic method).")
    user_query: str = dspy.InputField(desc="The student's specific question or struggle.")
    student_level: str = dspy.InputField(desc="Level: (e.g., Toddler, High School, Expert, Non-native Speaker).")
    learning_style: str = dspy.InputField(
        desc="The preferred framing (e.g., use metaphors vs. core logic vs. hands-on examples)."
    )
    current_scenario: str = dspy.InputField(desc="The context of learning (e.g., 'preparing for an exam').")
    chat_history: List[dict] = dspy.InputField(desc="Previous interaction context.")
    last_topic_taught: str = dspy.InputField(desc="The context of the previous lesson.")

    adapted_explanation: str = dspy.OutputField(desc="The teaching content, tailored specifically to the user level.")
    concept_analogy: str = dspy.OutputField(desc="A specific metaphor or 'mental hook' to help the student remember.")
    tutor_feedback: str = dspy.OutputField(desc="The conversational response and a nudge/question for the student.")


class TutorService:
    def __init__(self, model_config: dict):
        self.lm = dspy.LM(
            model=f"openai/{model_config['model_name']}",
            api_key=model_config['api_key'],
            api_base=model_config.get('api_base'),
            temperature=model_config.get('temperature', 0.1),
        )
        self.tutor_engine = dspy.ChainOfThought(AdaptiveTutorSignature)

    async def get_adaptive_response(self, data: TutorRequest) -> TutorResponse:
        try:
            history_dicts = [{"role": m.role, "content": m.content} for m in data.chat_history[-10:]]
            logger.info("Processing tutor request for level: %s", data.student_level)

            with dspy.context(lm=self.lm):
                prediction = self.tutor_engine(
                    user_query=data.user_query,
                    system_prompt=data.system_prompt,
                    student_level=data.student_level,
                    learning_style=data.learning_style,
                    current_scenario=data.current_scenario,
                    last_topic_taught=data.last_topic_taught,
                    chat_history=history_dicts,
                )

                return TutorResponse(
                    adapted_explanation=prediction.adapted_explanation,
                    concept_analogy=prediction.concept_analogy,
                    tutor_feedback=prediction.tutor_feedback,
                )
        except Exception as e:
            logger.error("DSPy execution error: %s", str(e), exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Tutor engine failed to process the request.",
            )


class PromptService:
    def __init__(self):
        self.storage_dir = Path(__file__).parent / "prompts"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_path(self, name: str) -> Path:
        safe_name = "".join(c for c in name if c.isalnum() or c in (" ", "_")).rstrip()
        return self.storage_dir / f"{safe_name}.yaml"

    def create_or_update_prompt(self, data: PromptCreateUpdate) -> str:
        file_path = self._get_path(data.name)
        prompt_file = PromptFile(name=data.name, content=data.content)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                yaml.dump(prompt_file.model_dump(mode="json"), f, default_flow_style=False)
            return data.name
        except Exception as e:
            logger.error("Failed to save prompt %s: %s", data.name, str(e))
            raise HTTPException(status_code=500, detail="Error saving prompt file")

    def list_prompts(self) -> List[str]:
        return sorted(f.stem for f in self.storage_dir.glob("*.yaml"))

    def read_prompt(self, name: str) -> str:
        file_path = self._get_path(name)
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Prompt not found")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            return data["content"]
        except Exception as e:
            logger.error("Failed to read prompt %s: %s", name, str(e))
            raise HTTPException(status_code=500, detail="Error reading prompt file")

    def read_prompt_full(self, name: str) -> PromptFile:
        file_path = self._get_path(name)
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Prompt not found")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            return PromptFile(**data)
        except Exception as e:
            logger.error("Failed to read prompt %s: %s", name, str(e))
            raise HTTPException(status_code=500, detail="Error reading prompt file")

    def delete_prompt(self, name: str) -> None:
        file_path = self._get_path(name)
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Prompt not found")
        file_path.unlink()
