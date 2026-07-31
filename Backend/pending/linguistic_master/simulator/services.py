import dspy
import uuid
import logging
from core.config import settings
from .schemas import SimulationRequest
import os
import yaml
import logging
from pathlib import Path
from fastapi import HTTPException
import dspy
import logging
from typing import List, Optional
from core.config import settings
from .schemas import ChatRequest, ChatMessage


logger = logging.getLogger(__name__)

# Constants for storage
STORAGE_PATH = Path("Data/language/wahtwillyoudo/prompts.yaml")

class SituationSimulator(dspy.Signature):
    """
    You are an advanced behavioral simulation engine. Given a specific persona (system prompt), 
     a scenario, and user input, you calculate the most logical and character-consistent 
     course of action.
    """
    system_prompt: str = dspy.InputField(desc="The persona and personality traits you must embody.")
    scenario: str = dspy.InputField(desc="The setting or situation currently unfolding.")
    user_input: str = dspy.InputField(desc="The specific question or dialogue directed at the persona.")
    additional_context: Optional[str] = dspy.InputField(default=None, desc="Extra background info, history, or environmental factors.")
    seed_uuid: str = dspy.InputField(desc="A unique identifier to ensure variety or tracking for this specific run.")

    thought_process: str = dspy.OutputField(desc="A detailed 'Chain of Thought' explaining WHY the persona chooses this action.")
    chosen_action: str = dspy.OutputField(desc="A description of the physical or verbal action taken.")
    response_dialogue: str = dspy.OutputField(desc="The actual words spoken by the persona in character.")
    emotional_state: str = dspy.OutputField(desc="The internal feeling/mood of the character after this interaction.")


class SituationalChat(dspy.Signature):
    """
    You are an AI character in a specific scenario. 
    Analyze the chat history and the current situation to decide what to do next.
    Stay strictly in character based on the System Prompt.
    """
    system_prompt: str = dspy.InputField(desc="Your persona, personality, and rules.")
    scenario: str = dspy.InputField(desc="The initial setting or ongoing situation.")
    chat_history: str = dspy.InputField(desc="The formatted history of past interactions.")
    user_input: str = dspy.InputField(desc="The latest message or action from the user.")
    
    thought: str = dspy.OutputField(desc="Your internal reasoning: Why are you saying this? What are you feeling?")
    dialogue: str = dspy.OutputField(desc="Your response to the user, written in character.")

    
class BehavioralEngine(dspy.Module):
    def __init__(self):
        super().__init__()
        self.simulator = dspy.ChainOfThought(SituationSignature)

    def forward(self, **kwargs):
        return self.simulator(**kwargs)

class SimulationService:
    @staticmethod
    def run_behavioral_sim(data: SimulationRequest) -> dict:
        """
        Executes the behavioral simulation using DSPy.
        
        Args:
            data: The validated simulation request.
            
        Returns:
            dict: The results of the simulation.
        """
        run_id = str(uuid.uuid4())
        lm = dspy.LM(
            model=f"openai/{settings.MODEL_NAME}",
            api_key=settings.OPENAI_API_KEY,
            api_base=settings.API_BASE,
            temperature=settings.TEMPERATURE,
            cache=False
        )

        with dspy.context(lm=lm):
            engine = BehavioralEngine()
            try:
                prediction = engine(
                    system_prompt=data.persona,
                    scenario=data.scenario,
                    user_input=data.user_input,
                    additional_context=data.additional_context or "N/A",
                    seed_uuid=run_id
                )
                
                logger.info(f"Simulation successful: {run_id}")
                return {
                    "simulation_id": run_id,
                    "thought_process": prediction.thought_process,
                    "chosen_action": prediction.chosen_action,
                    "response_dialogue": prediction.response_dialogue,
                    "emotional_state": prediction.emotional_state
                }
            except Exception as e:
                logger.error(f"Simulation failed: {str(e)}")
                raise e

class SituationalBot(dspy.Module):
    def __init__(self):
        super().__init__()
        self.chat_engine = dspy.ChainOfThought(SituationalChat)

    def forward(self, system_prompt, scenario, history_list: List[ChatMessage], user_input):
        # Format list to string: "User: msg\nAssistant: msg"
        formatted_history = "\n".join([f"{msg.role}: {msg.content}" for msg in history_list])
        
        return self.chat_engine(
            system_prompt=system_prompt,
            scenario=scenario,
            chat_history=formatted_history,
            user_input=user_input
        )

class ChatService:
    @staticmethod
    def execute_chat(data: ChatRequest) -> dict:
        """
        Runs a single turn in a situational chat.
        
        Returns:
            dict: The thought, dialogue, and updated history list.
        """
        lm = dspy.LM(
            model=f"openai/{settings.MODEL_NAME}",
            api_key=settings.OPENAI_API_KEY,
            api_base=settings.API_BASE,
            temperature=settings.TEMPERATURE,
            cache=False
        )

        with dspy.context(lm=lm):
            bot = SituationalBot()
            try:
                result = bot(
                    system_prompt=data.persona,
                    scenario=data.scenario,
                    history_list=data.chat_history,
                    user_input=data.user_input
                )
                
                # Construct updated history
                new_history = data.chat_history + [
                    ChatMessage(role="User", content=data.user_input),
                    ChatMessage(role="Assistant", content=result.dialogue)
                ]

                return {
                    "thought": result.thought,
                    "dialogue": result.dialogue,
                    "updated_history": new_history
                }
            except Exception as e:
                logger.error(f"Chat Engine Error: {str(e)}")
                raise e
                
class PromptManager:
    @staticmethod
    def _ensure_storage():
        """Ensures the directory and file exist."""
        STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not STORAGE_PATH.exists():
            with open(STORAGE_PATH, 'w') as f:
                yaml.dump({}, f)

    @staticmethod
    def load_all() -> dict:
        """Loads all prompts from the YAML file."""
        PromptManager._ensure_storage()
        with open(STORAGE_PATH, 'r') as f:
            return yaml.safe_load(f) or {}

    @staticmethod
    def save_prompt(name: str, content: str):
        """Saves or updates a prompt by name."""
        prompts = PromptManager.load_all()
        prompts[name] = content
        with open(STORAGE_PATH, 'w') as f:
            yaml.dump(prompts, f)
        logger.info(f"Prompt '{name}' saved successfully.")

    @staticmethod
    def get_prompt(name: str) -> str:
        """Retrieves a specific prompt."""
        prompts = PromptManager.load_all()
        if name not in prompts:
            raise HTTPException(status_code=404, detail=f"Prompt '{name}' not found.")
        return prompts[name]

    @staticmethod
    def list_names() -> list:
        """Returns a list of all prompt names."""
        return list(PromptManager.load_all().keys())