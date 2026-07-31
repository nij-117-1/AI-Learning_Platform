import logging
import uuid
import dspy
from typing import List, Dict, Literal, Optional
from core.config import master_llm_config as config
from practice.debate.schemas import PersonaRequest, DebateTurnRequest
logger = logging.getLogger(__name__)

class DebatePersonaGenerator(dspy.Signature):
    """
    You are a Master Rhetorician and Debate Coach. 
    Your task is to craft a comprehensive 'Master System Prompt' for an AI agent 
    to adopt a specific debating persona. This prompt should define their 
    argumentation style, logical fallacies to avoid (or use), and their 
    philosophical stance.
    """
    random_seed: str = dspy.InputField(
        description="A unique UUID or seed to ensure randomness in the generation process."
    )
    
    topic: str = dspy.InputField(desc="The subject of the debate.")
    stance: str = dspy.InputField(desc="The position the persona should take (e.g., Pro, Con, Neutral, Devil's Advocate).")
    debate_style: Literal["Socratic", "Aggressive", "Scientific", "Empathetic", "Formal"] = dspy.InputField(
        desc="The rhetorical approach to be used."
    )
    user_constraints: Optional[str] = dspy.InputField(
        default=None, 
        desc="Specific traits like 'use humor', 'be brief', or 'focus on ethical arguments'."
    )
    
    master_prompt: str = dspy.OutputField(
        desc="A complete, standalone System Prompt that embodies the full persona and rules for the debate."
    )

class DebatePersona(dspy.Signature):
    """
    You are an expert debater. Analyze the chat history, topic, and theme to 
    provide a logically sound, persuasive argument. You must adhere to your 
    assigned persona and strategy (Attack, Defend, or Counter).
    """

    # --- Input Fields ---
    random_seed: str = dspy.InputField(
        description="A unique UUID or seed to ensure randomness in the generation process."
    )
    system_prompt: str = dspy.InputField(desc="The persona definition and character rules.")
    debate_topic: str = dspy.InputField(desc="The core subject being debated.")
    context: str = dspy.InputField(desc="Information about general theme.")
    chat_history: List[Dict[str, str]] = dspy.InputField(desc="Previous exchanges in the debate.")
    stance_strategy: Literal["attack", "defend", "counter"] = dspy.InputField(desc="The rhetorical goal for this turn.")
    custom_instructions: Optional[str] = dspy.InputField(desc="Specific constraints like word count or emotional tone.")
    external_evidence: Optional[str] = dspy.InputField(desc="Supporting facts or raw data to be used in the argument.")

    # --- Output Fields ---
    rebuttal_summary: str = dspy.OutputField(desc="A brief analysis of the opponent's previous point.")
    argument_body: str = dspy.OutputField(desc="The main persuasive response or statement.")
    rhetorical_devices: List[str] = dspy.OutputField(desc="List of techniques used (e.g., Ethos, Pathos, Logos).")
    citations: List[str] = dspy.OutputField(desc="References or 'according to' markers used to back the claim.")
    next_question: str = dspy.OutputField(desc="A piercing question aimed at the opponent to pivot the debate.")
    
class DebateService:
    def __init__(self):
        self.lm = dspy.LM(
            model=f"openai/{config['model_name']}",
            api_key=config['api_key'],
            api_base=config['api_base'],
            temperature=config.get('temperature', 0.5)
        )

    def generate_persona(self, data: PersonaRequest) -> str:
        """
        Generates a master prompt using DSPy ChainOfThought.

        Args:
            data (PersonaRequest): The validated request parameters.

        Returns:
            str: The generated system prompt.
        """
        try:
            with dspy.context(lm=self.lm):
                execution_uuid = str(uuid.uuid4())
                generator = dspy.ChainOfThought(DebatePersonaGenerator)
                result = generator(
                    topic=data.topic,
                    stance=data.stance,
                    debate_style=data.debate_style,
                    random_seed=execution_uuid,
                    user_constraints=data.user_constraints or ""
                )
                logger.info(f"Persona generated successfully for topic: {data.topic}")
                return result.master_prompt
        except Exception as e:
            logger.error(f"DSPy Generation Error: {str(e)}")
            raise e
            
    def execute_turn(self, data: DebateTurnRequest):
        """
        Executes a single turn in the debate room using ChainOfThought.
        
        Args:
            data (DebateTurnRequest): The turn parameters.
        Returns:
            Prediction object containing argument and metadata.
        """
        try:
            with dspy.context(lm=self.lm):
                debater = dspy.ChainOfThought(DebatePersona)
                execution_uuid = str(uuid.uuid4())
                # Map the Pydantic model to DSPy InputFields
                response = debater(
                    system_prompt=data.persona,
                    debate_topic=data.topic,
                    context=f"{data.theme} | {data.context}",
                    chat_history=data.history,
                    stance_strategy=data.strategy,
                    custom_instructions=data.instructions,
                    random_seed=execution_uuid,
                    external_evidence=data.evidence
                )
                logger.info(f"Turn executed for topic: {data.topic}")
                return response
        except Exception as e:
            logger.error(f"DSPy Turn Execution Error: {str(e)}")
            raise e