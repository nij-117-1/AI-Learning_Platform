import dspy
import os
import yaml
import logging
from pathlib import Path
import logging
from core.config import settings
from typing import List, Dict, Optional
from .schemas import RoleplayRequest
from .schemas import RoleplayRecord

logger = logging.getLogger(__name__)
DATA_DIR = Path("data/roleplays")
DATA_DIR.mkdir(parents=True, exist_ok=True)

class RoleplayChatbot(dspy.Signature):
    """
    You are an immersive roleplay assistant. You must strictly adhere to the 
    provided Persona System Prompt and maintain the persona throughout the conversation.
    Use the chat history to maintain continuity and respond in the specified language.
    """
    
    roleplay_system_prompt: str = dspy.InputField(desc="The core persona, personality traits, and rules for the roleplay.")
    chat_history: List[Dict[str, str]] = dspy.InputField(desc="List of previous messages between the user and assistant.")
    current_user_message: str = dspy.InputField(desc="The latest message from the user.")
    language: str = dspy.InputField(desc="The language the chatbot must communicate in (e.g., English, Spanish, Hindi).")
    seed_uuid: str = dspy.InputField(desc="A unique identifier for the session to maintain consistency.")
    additional_instructions: Optional[str] = dspy.InputField(desc="Specific constraints or nudges for this specific turn.")

    response_message: str = dspy.OutputField(desc="The roleplay response for the user, following all persona and language rules.")


class RoleplayService:
    def __init__(self):
        self.lm = dspy.LM(
            model=f"openai/{settings.MODEL_NAME}",
            api_key=settings.OPENAI_API_KEY,
            api_base=settings.API_BASE,
            temperature=settings.TEMPERATURE,
            cache=False
        )

    def generate_response(self, data: RoleplayRequest) -> str:
        """
        Executes the DSPy ChainOfThought for roleplay.
        
        Args:
            data (RoleplayRequest): The validated request payload.
            
        Returns:
            str: The AI's generated response.
        """
        try:
            with dspy.context(lm=self.lm):
                predictor = dspy.ChainOfThought(RoleplayChatbot)
                # Convert list of ChatMessage to list of dicts for DSPy
                history_dicts = [m.model_dump() for m in data.history]
                
                prediction = predictor(
                    roleplay_system_prompt=data.system_prompt,
                    chat_history=history_dicts,
                    current_user_message=data.message,
                    language=data.language,
                    seed_uuid=data.seed,
                    additional_instructions=data.additional_instructions
                )
                return prediction.response_message
        except Exception as e:
            logger.error(f"DSPy Execution Error: {str(e)}")
            raise e


class RoleplayStorageService:
    @staticmethod
    def _get_path(name: str) -> Path:
        return DATA_DIR / f"{name.lower().replace(' ', '_')}.yaml"

    def create_role(self, role: RoleplayRecord):
        path = self._get_path(role.name)
        if path.exists():
            raise HTTPException(status_code=400, detail="Role already exists")
        
        with open(path, 'w') as f:
            yaml.dump(role.model_dump(), f)
        return role

    def list_roles(self) -> List[str]:
        return [f.stem for f in DATA_DIR.glob("*.yaml")]

    def get_role(self, name: str) -> RoleplayRecord:
        path = self._get_path(name)
        if not path.exists():
            raise HTTPException(status_code=404, detail="Role not found")
        
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
            return RoleplayRecord(**data)

    def update_role(self, name: str, prompt: str):
        role = self.get_role(name)
        role.prompt = prompt
        with open(self._get_path(name), 'w') as f:
            yaml.dump(role.model_dump(), f)
        return role

    def delete_role(self, name: str):
        path = self._get_path(name)
        if not path.exists():
            raise HTTPException(status_code=404, detail="Role not found")
        path.unlink()
        return {"message": f"Role {name} deleted"}