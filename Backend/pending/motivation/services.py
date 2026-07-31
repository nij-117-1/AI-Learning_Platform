import dspy
import logging
from datetime import date
from typing import Dict, Any
from config import master_llm_config as config
from learning.motivation.schemas import MotivationRequest, ReflectionRequest
from typing import Dict, Any, List, Literal, Optional
import uuid
logger = logging.getLogger(__name__)

class MotivationalQuoteGenerator(dspy.Signature):
    """
    You are a world-class motivational coach and philosopher. 
    Your goal is to provide a highly personalized, impactful quote 
    based on the user's current emotional state and the specific date/context.
    """
    random_seed: str = dspy.InputField(
        description="A unique UUID or seed to ensure randomness in the generation process."
    )
    seed_topic: str = dspy.InputField(description="A keyword or topic to anchor the quote (e.g., Discipline, Loss, Success).")
    current_date: str = dspy.InputField(description="Today's date to help align with seasons or specific historical context.")
    quote_type: Literal["stoic", "modern", "poetic", "tough-love"] = dspy.InputField(description="The stylistic delivery of the quote.")
    user_feeling: str = dspy.InputField(description="How the user describes their current emotional state.")
    
    quote: str = dspy.OutputField(description="The generated motivational quote.")
    author_persona: str = dspy.OutputField(description="The persona/name attributed to the quote (e.g., 'The Stoic Path' or 'The Modern Hustler').")
    actionable_insight: str = dspy.OutputField(description="A 1-sentence micro-habit or action the user can take right now.")

class ReflectionPromptGenerator(dspy.Signature):
    """
    You are a compassionate journaling coach. Your mission is to help users 
    transition from reactive thinking to deep self-awareness. Use the user's 
    mood and goals to craft questions that bypass surface-level answers.
    """
    random_seed: str = dspy.InputField(
        description="A unique UUID or seed to ensure randomness in the generation process."
    )
    current_mood: str = dspy.InputField(description="User's mood today (e.g., 'anxious about work').")
    goal_alignment: str = dspy.InputField(description="Which personal goal or value they want to focus on.")
    recent_patterns: Optional[str] = dspy.InputField(
        default=None, 
        description="Summarized mood/progress trends from the past week."
    )
    
    prompts: List[str] = dspy.OutputField(description="A list of 3 powerful, open-ended questions designed for deep journaling.")
    perspective_shift: str = dspy.OutputField(description="One transformative 'What if' sentence to reframe the user's current challenge.")


class MotivationService:
    @staticmethod
    def generate_motivation_quote(data: MotivationRequest) -> Dict[str, Any]:
        """
        Generates a motivational response using DSPy and OpenAI.

        Args:
            data (MotivationRequest): The user input data.

        Returns:
            Dict[str, Any]: The processed quote and meta-data.
        """
        logger.info(f"Generating {data.quote_type} motivation for topic: {data.seed_topic}")
        
        lm = dspy.LM(
            model=f"openai/{config['model_name']}",
            api_key=config['api_key'],
            api_base=config['api_base'],
            temperature=config.get('temperature', 0.5)
        )

        today_str = str(date.today())

        with dspy.settings.context(lm=lm):
            execution_uuid = str(uuid.uuid4())
            generator = dspy.ChainOfThought(MotivationalQuoteGenerator)
            prediction = generator(
                seed_topic=data.seed_topic,
                current_date=today_str,
                quote_type=data.quote_type,
                random_seed=execution_uuid ,
                user_feeling=data.user_feeling
            )

            return {
                "quote": prediction.quote,
                "author_persona": prediction.author_persona,
                "actionable_insight": prediction.actionable_insight,
                "current_date": today_str
            }

    @staticmethod
    def generate_reflection_session(data: ReflectionRequest) -> Dict[str, Any]:
        """
        Generates journaling prompts and a perspective shift using DSPy.

        Args:
            data (ReflectionRequest): The user's mood and goal context.

        Returns:
            Dict[str, Any]: The generated prompts and reframing thought.
        """
        logger.info(f"Generating reflection prompts for mood: {data.current_mood[:20]}...")
        
        lm = dspy.LM(
            model=f"openai/{config['model_name']}",
            api_key=config['api_key'],
            api_base=config['api_base'],
            temperature=0.6
        )

        with dspy.settings.context(lm=lm):
            coach = dspy.ChainOfThought(ReflectionPromptGenerator)
            generator = dspy.ChainOfThought(MCQGenerator)
            prediction = coach(
                current_mood=data.current_mood,
                goal_alignment=data.goal_alignment,
                random_seed=execution_uuid ,
                recent_patterns=data.recent_patterns or "No specific patterns recorded."
            )

            return {
                "prompts": prediction.prompts,
                "perspective_shift": prediction.perspective_shift
            }