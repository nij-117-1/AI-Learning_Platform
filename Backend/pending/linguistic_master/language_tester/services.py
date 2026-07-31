import dspy
import logging
from typing import List, Dict, Any, Literal, Optional
from core.config import settings
from .schemas import AssessmentRequest, AssessmentResponse
from .schemas import FIBRequest, EvaluationRequest
from .schemas import TranslationChallengeRequest
from .schemas import RoleplayRequest
import random
logger = logging.getLogger(__name__)

class LanguageMCQEvaluator(dspy.Signature):
    """
    You are an Adaptive Language Examiner. 
    Generate a specific number of Multiple Choice Questions (MCQs) to evaluate 
    proficiency in a target language. Scale the vocabulary and grammar complexity 
    strictly according to the CEFR level provided.
    """
    # Inputs
    target_language: str = dspy.InputField(desc="The language being tested (e.g., Italian, Korean).")
    native_language: str = dspy.InputField(desc="The user's native language for explanations and reference")
    level: Literal["A1", "A2", "B1", "B2", "C1", "C2"] = dspy.InputField(desc="CEFR proficiency level.")
    num_questions: int = dspy.InputField(desc="The total number of questions to generate.")
    scenario: str = dspy.InputField(desc="Context for questions (e.g., 'Ordering at a restaurant', 'Business meeting').")
    user_details: str = dspy.InputField(desc="Persona info to personalize the questions.")
    seed: str = dspy.InputField(desc="A unique string/number to ensure different questions on every run.")
    custom_instructions: Optional[str] = dspy.InputField(desc="Specific focus (e.g., 'only use past tense', 'no formal pronouns').")

    # Outputs
    level_rationale: str = dspy.OutputField(desc="Briefly explain why these questions fit the requested CEFR level.")
    assessment_title: str = dspy.OutputField(desc="A creative title for this specific test set.")
    questions: List[Dict[str, Any]] = dspy.OutputField(desc="""
        A list of MCQ objects. Each object must contain:
        - 'id': unique question ID
        - 'text': The question 
        - 'options': {'A': '...', 'B': '...', 'C': '...', 'D': '...'}
        - 'correct': The letter (A, B, C, or D)
        - 'explanation': Why the answer is correct (in the native language)
        """)
    

# ==========================================
# 1. THE FILL-IN-THE-BLANK GENERATOR MODULE
# ==========================================
class FillInTheBlankGenerator(dspy.Signature):
    """
    You are a Language Tutor. Generate 'Fill in the Blank' sentences.
    The sentence should have one clear missing part (indicated by '____').
    Tailor the vocabulary to the user's profile and CEFR level.
    """
    target_language: str = dspy.InputField(desc="The language to practice.")
    level: Literal["A1", "A2", "B1", "B2", "C1", "C2"] = dspy.InputField()
    num_questions: int = dspy.InputField(desc="Number of sentences to generate.")
    scenario: str = dspy.InputField(desc="Context (e.g., 'At the Pharmacy', 'Office Gossip').")
    user_details: str = dspy.InputField(desc="User's background to make sentences relatable.")
    seed: str = dspy.InputField(desc="Seed for randomness.")

    questions: List[Dict[str, str]] = dspy.OutputField(desc="""
        List of objects:
        - 'sentence': The sentence with '____'
        - 'correct_word': The missing word/phrase
        - 'hint': A clue in the target language
        - 'context_clue': Translation of the sentence in the native language
    """)

# ==========================================
# 2. THE ANSWER EVALUATOR MODULE
# ==========================================
class WordEvaluator(dspy.Signature):
    """
    You are a Linguistic Grader. Compare the User's Answer with the Correct Word.
    Determine if it is Correct, Incorrect, or 'Close' (Typo/Partial).
    Provide grammatical feedback.
    """
    sentence_context: str = dspy.InputField(desc="The full sentence where the word fits.")
    correct_word: str = dspy.InputField(desc="The expected answer.")
    user_answer: str = dspy.InputField(desc="What the user typed.")
    
    is_correct: bool = dspy.OutputField(desc="True if the answer is functionally correct.")
    status: Literal["correct", "typo", "incorrect"] = dspy.OutputField()
    feedback: str = dspy.OutputField(desc="Brief explanation of the mistake or praise.")
    improvement_tip: Optional[str] = dspy.OutputField(desc="Grammar rule related to this specific error.")


class TranslationChallengeGenerator(dspy.Signature):
    """
    You are a Bilingual Assessment Expert. 
    Generate a translation challenge that tests either 'Active Production' 
    (Native to Target) or 'Passive Recognition' (Target to Native).
    The challenge must be contextually relevant to the user's scenario and level.
    """
    # Inputs
    target_language: str = dspy.InputField(desc="The language the user is learning.")
    native_language: str = dspy.InputField(desc="The user's primary language.")
    level: Literal["A1", "A2", "B1", "B2", "C1", "C2"] = dspy.InputField()
    scenario: str = dspy.InputField(desc="Setting (e.g., 'Navigating a Train Station', 'Technical Brainstorming').")
    user_persona: str = dspy.InputField(desc="Who the user is (e.g., 'Student', 'CEO', 'Tourist').")
    test_type: Literal["translate_to_target", "translate_to_native", "explain_meaning"] = dspy.InputField(
        desc="Direction of the test: Native->Target, Target->Native, or explaining nuance."
    )
    seed: str = dspy.InputField(desc="Randomness seed to vary the sentences.")
    custom_instructions: Optional[str] = dspy.InputField(desc="e.g., 'use informal pronouns', 'focus on medical terms'.")

    # Outputs
    challenge_instruction: str = dspy.OutputField(desc="Specific instruction for the user (e.g., 'Translate this to Spanish').")
    source_text: str = dspy.OutputField(desc="The text provided to the user to process.")
    correct_reference: str = dspy.OutputField(desc="The ideal translation or explanation.")
    vocabulary_highlights: List[str] = dspy.OutputField(desc="Key words to pay attention to in this challenge.")
    cultural_tip: Optional[str] = dspy.OutputField(desc="A note on why this specific phrasing is used in the target culture.")


class RoleplayChatEvaluator(dspy.Signature):
    """
    You are a Language Immersion Coach. 
    Your goal is to sustain a realistic conversation in the Target Language.
    You act as a specific character (e.g., a grumpy waiter, a helpful doctor).
    You must evaluate the user's response for fluency while keeping the 
    conversation moving forward naturally.
    """
    # Inputs (Contextual)
    target_language: str = dspy.InputField(desc="Language of the conversation.")
    level: Literal["A1", "A2", "B1", "B2", "C1", "C2"] = dspy.InputField()
    scenario: str = dspy.InputField(desc="Setting (e.g., 'At a Police Station reporting a lost bag').")
    user_persona: str = dspy.InputField(desc="The role the user is playing.")
    chat_history: List[Dict[str, str]] = dspy.InputField(desc="The previous turns of the conversation.")
    user_latest_response: str = dspy.InputField(desc="The user's most recent chat message.")
    seed: str = dspy.InputField(desc="Seed to determine the AI character's personality.")

    # Outputs
    linguistic_critique: str = dspy.OutputField(desc="Feedback on user's grammar/vocabulary in the latest turn.")
    fluency_score: int = dspy.OutputField(desc="1-10 score of the user's latest response.")
    ai_character_response: str = dspy.OutputField(desc="The AI's next line in character (Target Language).")
    suggested_strategies: List[str] = dspy.OutputField(desc="Ways the user could have phrased things better.")
    is_goal_achieved: bool = dspy.OutputField(desc="Has the user successfully completed the scenario goal?")



class LanguageTesterService:
    @staticmethod
    def generate_assessment(data: AssessmentRequest) -> Dict[str, Any]:
        """
        Triggers the DSPy engine to create language MCQs.
        
        Args:
            data: The AssessmentRequest validated schema.
            
        Returns:
            A dictionary matching AssessmentResponse schema.
        """
        logger.info(f"Generating {data.level} {data.target_language} assessment for scenario: {data.scenario}")
        
        lm = dspy.LM(
            model=f"openai/{settings.MODEL_NAME}",
            api_key=settings.OPENAI_API_KEY,
            api_base=settings.API_BASE,
            temperature=settings.TEMPERATURE,
            cache=False
        )

        with dspy.context(lm=lm):
            generator = dspy.ChainOfThought(LanguageMCQEvaluator)
            response = generator(
                target_language=data.target_language,
                native_language=data.native_language,
                level=data.level,
                num_questions=data.num_questions,
                scenario=data.scenario,
                user_details=data.user_details,
                seed=data.seed,
                custom_instructions=data.custom_instructions
            )
            
            return {
                "assessment_title": response.assessment_title,
                "level_rationale": response.level_rationale,
                "questions": response.questions
            }

    @classmethod
    def generate_fib_questions(cls, data: FIBRequest) -> Dict[str, Any]:
        """Generates fill-in-the-blank questions using DSPy."""
        lm = dspy.LM(
            model=f"openai/{settings.MODEL_NAME}",
            api_key=settings.OPENAI_API_KEY,
            api_base=settings.API_BASE,
            temperature=settings.TEMPERATURE,
            cache=False
        )
        with dspy.context(lm=lm):
            generator = dspy.Predict(FillInTheBlankGenerator)
            response = generator(
                target_language=data.target_language,
                level=data.level,
                num_questions=data.num_questions,
                scenario=data.scenario,
                user_details=data.user_details,
                seed=data.seed
            )
            return {"questions": response.questions}

    @classmethod
    def evaluate_answer(cls, data: EvaluationRequest) -> Dict[str, Any]:
        """Evaluates a user answer against the correct word."""
        lm = dspy.LM(
            model=f"openai/{settings.MODEL_NAME}",
            api_key=settings.OPENAI_API_KEY,
            api_base=settings.API_BASE,
            temperature=settings.TEMPERATURE,
            cache=False
        )
        with dspy.context(lm=lm):
            evaluator = dspy.Predict(WordEvaluator)
            response = evaluator(
                sentence_context=data.sentence_context,
                correct_word=data.correct_word,
                user_answer=data.user_answer
            )
            return {
                "is_correct": response.is_correct,
                "status": response.status,
                "feedback": response.feedback,
                "improvement_tip": response.improvement_tip
            }

    @classmethod
    def generate_translation_task(cls, data: TranslationChallengeRequest) -> Dict[str, Any]:
        """
        Orchestrates the Translation Challenge generation with deterministic randomness.
        """
        # 1. Deterministic selection of test type based on seed
        random_gen = random.Random(data.seed)
        test_modes = ["translate_to_target", "translate_to_native", "explain_meaning"]
        chosen_mode = random_gen.choice(test_modes)

        lm = dspy.LM(
            model=f"openai/{settings.MODEL_NAME}",
            api_key=settings.OPENAI_API_KEY,
            api_base=settings.API_BASE,
            temperature=settings.TEMPERATURE,
            cache=False
        )

        with dspy.context(lm=lm):
            # Use ChainOfThought for high-quality translation tasks
            generator = dspy.ChainOfThought(TranslationChallengeGenerator)
            response = generator(
                target_language=data.target_language,
                native_language=data.native_language,
                level=data.level,
                scenario=data.scenario,
                user_persona=data.user_persona,
                test_type=chosen_mode,
                seed=data.seed,
                custom_instructions=data.custom_instructions
            )

            return {
                "test_type": chosen_mode,
                "challenge_instruction": response.challenge_instruction,
                "source_text": response.source_text,
                "correct_reference": response.correct_reference,
                "vocabulary_highlights": response.vocabulary_highlights,
                "cultural_tip": response.cultural_tip
            }

    @classmethod
    def continue_roleplay(cls, data: RoleplayRequest) -> Dict[str, Any]:
        """
        Simulates a turn in an immersive language roleplay.
        """
        logger.info(f"Continuing roleplay in {data.target_language} for scenario: {data.scenario}")
        
        # Converging to 0.8 temperature for creative/conversational flow
        lm = dspy.LM(
            model=f"openai/{settings.MODEL_NAME}",
            api_key=settings.OPENAI_API_KEY,
            api_base=settings.API_BASE,
            temperature=settings.TEMPERATURE,
            cache=False
        )

        with dspy.context(lm=lm):
            # Using ChainOfThought to allow the model to critique grammar before replying
            simulator = dspy.ChainOfThought(RoleplayChatEvaluator)
            
            # Convert Pydantic history objects to raw dicts for DSPy
            history_dicts = [msg.model_dump() for msg in data.chat_history]

            response = simulator(
                target_language=data.target_language,
                level=data.level,
                scenario=data.scenario,
                user_persona=data.user_persona,
                chat_history=history_dicts,
                user_latest_response=data.user_latest_response,
                seed=data.seed
            )

            return {
                "linguistic_critique": response.linguistic_critique,
                "fluency_score": response.fluency_score,
                "ai_character_response": response.ai_character_response,
                "suggested_strategies": response.suggested_strategies,
                "is_goal_achieved": response.is_goal_achieved
            }