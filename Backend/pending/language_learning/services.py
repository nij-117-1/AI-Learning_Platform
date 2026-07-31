import dspy
import logging
from typing import List, Dict, Optional, Literal
from config import master_llm_config as config
from learning.language_learning.models import LanguageSessionRequest, LanguageSessionResponse, IdiomDecodeRequest, IdiomDecodeResponse

logger = logging.getLogger(__name__)

class LanguageLearningTranslator(dspy.Signature):
    """
    You are an adaptive Language Coach. You handle two scenarios:
    1. If 'text_to_translate' is provided: Translate it and explain the grammar.
    2. If 'text_to_translate' is empty: Suggest a 'Topic of the Day' based on the 
       user's level and interests from the chat history.
    """
    # Context & Session Inputs
    seed_context: str = dspy.InputField(desc="The core teaching persona (e.g., 'Focus on Castilian Spanish', 'Travel-centric Vocabulary').")
    text_to_translate: Optional[str] = dspy.InputField(desc="Specific text from the user, or None if they just want to chat/learn.")
    target_lang: str = dspy.InputField(desc="The language the user is currently learning.")
    user_level: Literal["Beginner", "Intermediate", "Advanced"] = dspy.InputField()
    
    # Chat Loop
    chat_history: List[Dict[str, str]] = dspy.InputField(desc="Past interactions to maintain context.")
    user_input: str = dspy.InputField(desc="The user's direct message (could be 'Translate this' or 'What should I learn today?').")

    # Learning Outputs
    rationale: str = dspy.OutputField(desc="Strategic reasoning: Why this translation or topic was chosen.")
    answer_message: str = dspy.OutputField(desc="Friendly response to the user's immediate question or greeting.")
    original_text: Optional[str] = dspy.OutputField(desc="Echo of the input text (or the suggested phrase if input was empty).")
    translated_text: str = dspy.OutputField(desc="The translated version or the 'phrase of the day'.")
    points_to_keep_in_mind: List[str] = dspy.OutputField(desc="Crucial grammar tips, cultural context, or common pitfalls.")
    what_to_learn_today_suggestion: Optional[str] = dspy.OutputField(desc="A specific theme or grammar point suggested for today's study.")

class IdiomaticNuanceChatbot(dspy.Signature):
    """
    You are a Cultural Linguist and Pragmatic Coach. Your goal is to decode 
    the 'cultural logic' behind idioms and slang. You help learners understand 
    not just what an expression means, but WHEN and WHY to use it to avoid 
    socially inappropriate 'fluent fool' mistakes.
    """
    # Contextual Inputs
    seed_context: str = dspy.InputField(desc="The specific cultural or regional focus (e.g., 'British English', 'Business Context').")
    target_expression: str = dspy.InputField(desc="The idiom, phrasal verb, or slang term to decode.")
    user_l1_equivalent: Optional[str] = dspy.InputField(default=None, desc="Direct translation in the user's native language.")
    
    # Chat Loop Inputs
    chat_history: List[Dict[str, str]] = dspy.InputField(desc="Previous turns in the decoding session.")
    user_input: str = dspy.InputField(desc="User's latest question or attempt to use the phrase in a sentence.")

    # Pragmatic Outputs
    rationale: str = dspy.OutputField(desc="Strategic reasoning: Identifying the origin and common pitfalls of this phrase.")
    literal_breakdown: str = dspy.OutputField(desc="Word-for-word explanation showing why literal translation fails.")
    cultural_logic: str = dspy.OutputField(desc="The underlying conceptual metaphor or historical context.")
    register_spectrum: Dict[str, str] = dspy.OutputField(desc="Social contexts: intimate, casual, professional, formal.")
    emotional_valence: str = dspy.OutputField(desc="The 'vibe' of the phrase (e.g., sarcastic, affectionate, hostile).")
    false_friend_warning: bool = dspy.OutputField(desc="True if the phrase is commonly confused with something else in L1.")
    usage_correction: str = dspy.OutputField(desc="Feedback on the user's attempt to use the phrase, or a perfect example sentence.")




class LanguageLearningService:
    def __init__(self):
        """Initializes the DSPy LM using the master config."""
        self.lm = dspy.LM(
            model=f"openai/{config['model_name']}",
            api_key=config['api_key'],
            api_base=config['api_base'],
            temperature=config.get('temperature', 0.7)
        )

    def process_session(self, data: LanguageSessionRequest) -> LanguageSessionResponse:
        """
        Executes a DSPy ChainOfThought turn.
        
        Args:
            data: The validated session request.
            
        Returns:
            LanguageSessionResponse: The processed learning output.
        """
        try:
            with dspy.context(lm=self.lm):
                predictor = dspy.ChainOfThought(LanguageLearningTranslator)
                prediction = predictor(
                    seed_context=data.seed_context,
                    text_to_translate=data.text_to_translate,
                    target_lang=data.target_lang,
                    user_level=data.user_level,
                    chat_history=data.chat_history,
                    user_input=data.user_input
                )
                
                return LanguageSessionResponse(
                    answer_message=prediction.answer_message,
                    original_text=prediction.original_text,
                    translated_text=prediction.translated_text,
                    points_to_keep_in_mind=prediction.points_to_keep_in_mind,
                    what_to_learn_today_suggestion=prediction.what_to_learn_today_suggestion,
                    rationale=prediction.rationale
                )
        except Exception as e:
            logger.error(f"Error in LanguageLearningService: {str(e)}")
            raise e

    def decode_expression(self, data: IdiomDecodeRequest) -> IdiomDecodeResponse:
        """Processes the idiomatic turn using ChainOfThought."""
        try:
            with dspy.context(lm=self.lm):
                decoder = dspy.ChainOfThought(IdiomaticNuanceChatbot)
                response = decoder(
                    seed_context=data.seed_context,
                    target_expression=data.target_expression,
                    user_l1_equivalent=data.user_l1_equivalent,
                    chat_history=data.chat_history,
                    user_input=data.user_input
                )
                
                return IdiomDecodeResponse(
                    rationale=response.rationale,
                    literal_breakdown=response.literal_breakdown,
                    cultural_logic=response.cultural_logic,
                    register_spectrum=response.register_spectrum,
                    emotional_valence=response.emotional_valence,
                    false_friend_warning=response.false_friend_warning,
                    usage_correction=response.usage_correction
                )
        except Exception as e:
            logger.error(f"IdiomDecoderService Failure: {str(e)}")
            raise e