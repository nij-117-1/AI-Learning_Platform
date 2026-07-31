from config import master_llm_config as config
from learning.tutor.services import TutorService, PromptService


def get_tutor_service() -> TutorService:
    return TutorService(model_config=config)


def get_prompt_service() -> PromptService:
    return PromptService()
