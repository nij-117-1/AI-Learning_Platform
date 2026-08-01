import dspy
import random
import logging
from typing import Literal
from fastapi import HTTPException
from config import master_llm_config as config
from practice.iq_generator.schemas import RiddleRequest, EvaluationRequest
from practice.iq_generator.schemas import (
    RiddleRequest, EvaluationRequest, 
    BridgeRequest, SocraticRequest, BiasRequest, PuzzleRequest, PuzzleEvaluationRequest
)
from typing import Literal, Optional
import uuid
logger = logging.getLogger(__name__)

class AdaptiveRiddleGenerator(dspy.Signature):
    """
    Generates personalized riddles that adapt to the user's cognitive level.
    Uses a seed for variability to ensure unique puzzles.
    """
    field_of_interest: str = dspy.InputField(description="The topic (e.g. Space, History).")
    target_domain: Literal["verbal", "mathematical", "spatial", "lateral"] = dspy.InputField(description="Cognitive domain.")
    difficulty_level: Literal["novice", "intermediate", "expert", "genius"] = dspy.InputField(description="Difficulty tier.")
    seed: int = dspy.InputField(description="A random seed for variety.")
    
    riddle_text: str = dspy.OutputField(description="The riddle/puzzle text.")
    solution: str = dspy.OutputField(description="Clear explanation of the logic.")
    cognitive_trigger: str = dspy.OutputField(description="The mental hook being trained.")

class RiddleEvaluator(dspy.Signature):
    """
    Evaluates the user's answer. Determines correctness and provides feedback.
    """
    riddle_text: str = dspy.InputField(description="The original riddle.")
    solution: str = dspy.InputField(description="The correct answer.")
    user_answer: str = dspy.InputField(description="The user's attempt or request for help.")
    
    is_correct: bool = dspy.OutputField(description="True if the answer is logically correct.")
    feedback: str = dspy.OutputField(description="Feedback or a hint if incorrect. Do not reveal the answer.")
    thought_redirection: str = dspy.OutputField(description="Instruction on how to shift their perspective.")
    
class ConceptualBridgeBuilder(dspy.Signature):
    """
    Forces connections between unrelated domains to enhance cognitive flexibility.
    Targets: Creativity, analogical thinking, and knowledge transfer.
    """
    concept_a: str = dspy.InputField(description="First concept (e.g., 'Photosynthesis').")
    concept_b: str = dspy.InputField(description="Second seemingly unrelated concept (e.g., 'Blockchain').")
    abstraction_depth: Literal["surface", "structural", "systemic"] = dspy.InputField(
        description="How deep the analogy should be."
    )
    seed: int = dspy.InputField(description="Seed for variation in creative connections.")

    structural_analogy: str = dspy.OutputField(
        description="Deep structural similarity between the concepts."
    )
    bridging_narrative: str = dspy.OutputField(
        description="A story that connects A to B in 2-3 sentences."
    )
    insight_question: str = dspy.OutputField(
        description="A question that forces the user to find a missing link."
    )
    cognitive_flexibility_score: int = dspy.OutputField(
        description="Estimated IQ points impact: 1-5 (5 being high transfer learning potential)."
    )

class SocraticChallenger(dspy.Signature):
    """
    Challenges user's reasoning rather than providing answers.
    Targets: Intellectual humility, logical consistency, and argumentation skills.
    Continuously probes the user's logic based on their current statement and past history.
    """
    conversation_history: str = dspy.InputField(
        description="The log of previous exchanges to avoid repetition and deepen the challenge."
    )
    user_statement: str = dspy.InputField(description="The user's latest opinion or rebuttal.")
    confidence_level: Literal["low", "medium", "high", "certain"] = dspy.InputField(
        description="The user's perceived certainty in their current stance."
    )
    
    logical_fallacy_check: Optional[str] = dspy.OutputField(
        description="If present, name the fallacy (e.g., Strawman, Ad Hominem); else 'None detected'."
    )
    falsification_question: str = dspy.OutputField(
        description="A pithy question that asks: 'What evidence would prove you wrong?'"
    )
    edge_case_scenario: str = dspy.OutputField(
        description="A 'What if...' scenario where the user's current logic leads to a contradiction."
    )
    refined_perspective: str = dspy.OutputField(
        description="A bridge: 'A more nuanced way to look at this might be...'"
    )

class CognitiveBiasInoculator(dspy.Signature):
    """
    Simulates a 'System 1 vs System 2' training session.
    Triggers a bias in the user, waits for their response, and then explains the logic.
    """
    conversation_history: str = dspy.InputField(description="Previous scenarios or user reactions.")
    target_bias: Literal["anchoring", "availability", "confirmation", "sunk_cost", "framing"] = dspy.InputField(
        description="Bias to train against."
    )
    user_interest: str = dspy.InputField(description="User's field (e.g., 'trading', 'dating', 'engineering').")
    
    # AI response fields
    scenario_setup: str = dspy.OutputField(
        description="A stealthy scenario that ends with a question for the user."
    )
    intuitive_trap: str = dspy.OutputField(
        description="The 'gut feeling' or biased answer the user likely had."
    )
    rational_analysis: str = dspy.OutputField(
        description="Detailed breakdown of how the bias works and what the rational path is."
    )
    real_world_application: str = dspy.OutputField(
        description="A practical tip for spotting this specific bias in their work/life."
    )


class AdaptivePuzzleGenerator(dspy.Signature):
    """
    Generates highly personalized puzzles and brain teasers. 
    The agent adapts the complexity and logic style based on the target domain, 
    puzzle type, and difficulty tier to provide a tailored cognitive challenge.
    """
    
    field_of_interest: str = dspy.InputField(
        description="The thematic topic (e.g., Cyberpunk, Ancient Egypt, Quantum Physics)."
    )
    puzzle_type: Literal["riddle", "logic grid", "sequence", "wordplay", "cipher"] = dspy.InputField(
        description="The specific format of the puzzle."
    )
    target_domain: Literal["verbal", "mathematical", "spatial", "lateral"] = dspy.InputField(
        description="The primary cognitive skill the puzzle should exercise."
    )
    difficulty_level: Literal["novice", "intermediate", "expert", "genius"] = dspy.InputField(
        description="The depth of reasoning required to solve the puzzle."
    )
    seed: int = dspy.InputField(
        description="A numerical seed to ensure variety and uniqueness in generation."
    )

    puzzler_persona: str = dspy.OutputField(
        description="A short flavor-text description of the entity presenting the puzzle."
    )
    puzzle_text: str = dspy.OutputField(
        description="The actual content of the puzzle or brain teaser."
    )
    solution: str = dspy.OutputField(
        description="The correct answer with a step-by-step logical breakdown."
    )
    cognitive_trigger: str = dspy.OutputField(
        description="Analysis of the mental 'trap' or insight required to solve it."
    )


class PuzzleEvaluator(dspy.Signature):
    """
    Evaluates a user's response to a puzzle. It determines logical correctness, 
    calculates how close the user was, and provides targeted hints without spoiling the solution.
    """
    puzzle_context: str = dspy.InputField(description="The full text of the puzzle/challenge.")
    puzzle_type: str = dspy.InputField(description="The type of puzzle (e.g., cipher, logic grid, sequence).")
    official_solution: str = dspy.InputField(description="The factual correct answer and logic.")
    user_response: str = dspy.InputField(description="The user's input, answer, or query.")

    is_correct: bool = dspy.OutputField(description="Boolean indicating if the answer matches the solution's logic.")
    accuracy_score: float = dspy.OutputField(description="A score from 0.0 to 1.0 representing how close the user was.")
    evaluation_feedback: str = dspy.OutputField(description="Encouraging feedback. If wrong, point out the logical flaw.")
    hint_redirection: Optional[str] = dspy.OutputField(description="A nudge toward the right path. Only provide if is_correct is False.")
    metacognitive_prompt: str = dspy.OutputField(description="A question to help the user rethink their approach (e.g., 'What if you looked at the numbers in reverse?').")


class IQService:

    @staticmethod
    def _get_lm():
        return dspy.LM(
            model=f"openai/{config['model_name']}",
            api_key=config['api_key'],
            api_base=config['api_base'],
            temperature=config.get('temperature', 0.7)
        )

    @staticmethod
    def generate_puzzle(data: PuzzleRequest):
        """
        Generates a puzzle using ChainOfThought. Seed is generated via UUID internally.
        
        Args:
            data: PuzzleRequest parameters.
        Returns:
            Dictionary matching PuzzleResponse schema.
        """
        try:
            # Generate internal unique seed from UUID
            internal_seed = uuid.uuid4().int % (10**6)
            
            lm = IQService._get_lm()
            with dspy.context(lm=lm):
                puzzle_agent = dspy.ChainOfThought(AdaptivePuzzleGenerator)
                result = puzzle_agent(
                    field_of_interest=data.field_of_interest,
                    puzzle_type=data.puzzle_type,
                    target_domain=data.target_domain,
                    difficulty_level=data.difficulty_level,
                    seed=internal_seed
                )
                
                return {
                    "puzzler_persona": result.puzzler_persona,
                    "puzzle_text": result.puzzle_text,
                    "solution": result.solution,
                    "cognitive_trigger": result.cognitive_trigger
                }
        except Exception as e:
            logger.error(f"Failed to generate puzzle: {str(e)}")
            raise HTTPException(status_code=500, detail="Puzzle generation engine failure.")

    @staticmethod
    def evaluate_puzzle(data: PuzzleEvaluationRequest):
        """
        Evaluates a puzzle attempt using ChainOfThought logic.
        """
        try:
            # We use a lower temperature for evaluation for more consistent logic
            lm = IQService._get_lm()
            with dspy.context(lm=lm):
                eval_agent = dspy.ChainOfThought(PuzzleEvaluator)
                result = eval_agent(
                    puzzle_context=data.puzzle_context,
                    puzzle_type=data.puzzle_type,
                    official_solution=data.official_solution,
                    user_response=data.user_response
                )
                
                return {
                    "is_correct": bool(result.is_correct),
                    "accuracy_score": float(result.accuracy_score),
                    "evaluation_feedback": result.evaluation_feedback,
                    "hint_redirection": result.hint_redirection if not result.is_correct else None,
                    "metacognitive_prompt": result.metacognitive_prompt
                }
        except Exception as e:
            logger.error(f"Puzzle evaluation failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Evaluation service error.")

    
    @staticmethod
    def generate_riddle(data: RiddleRequest):
        """
        Generates a riddle using DSPy logic.
        
        Args:
            data: The parameters for riddle generation.
        Returns:
            A generated riddle object.
        Raises:
            HTTPException: If the LLM provider fails.
        """
        try:
            internal_seed = uuid.uuid4().int % (10**6)
            lm = dspy.LM(
                model=f"openai/{config['model_name']}",
                api_key=config['api_key'],
                api_base=config['api_base'],
                temperature=config.get('temperature', 0.7)
            )
            
            with dspy.context(lm=lm):
                generator = dspy.Predict(AdaptiveRiddleGenerator)
                response = generator(
                    field_of_interest=data.field_of_interest,
                    target_domain=data.target_domain,
                    difficulty_level=data.difficulty_level,
                    seed=internal_seed
                )
                return response
        except Exception as e:
            logger.error(f"Error generating riddle: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate puzzle.")

    @staticmethod
    def evaluate_answer(data: EvaluationRequest):
        """
        Evaluates user input against the solution.
        """
        try:
            lm = dspy.LM(
                model=f"openai/{config['model_name']}",
                api_key=config['api_key'],
                api_base=config['api_base'],
                temperature=0.2
            )
            
            with dspy.context(lm=lm):
                evaluator = dspy.Predict(RiddleEvaluator)
                return evaluator(
                    riddle_text=data.riddle_text,
                    solution=data.solution,
                    user_answer=data.user_answer
                )
        except Exception as e:
            logger.error(f"Error evaluating answer: {str(e)}")
            raise HTTPException(status_code=500, detail="Evaluation service unavailable.")

    @staticmethod
    def build_bridge(data: BridgeRequest):
        """
        Triggers the AI to find a creative link between two disparate ideas.
        Uses ChainOfThought for deep reasoning.
        """
        try:
            lm = dspy.LM(
                model=f"openai/{config['model_name']}",
                api_key=config['api_key'],
                api_base=config['api_base'],
                temperature=config.get('temperature', 0.8),
                cache=False
            )
            
            with dspy.context(lm=lm):
                # Using ChainOfThought for complex analogical reasoning
                bridge_tool = dspy.ChainOfThought(ConceptualBridgeBuilder)
                result = bridge_tool(
                    concept_a=data.concept_a,
                    concept_b=data.concept_b,
                    abstraction_depth=data.abstraction_depth,
                    seed=random.randint(1, 100000)
                )
                return result
        except Exception as e:
            logger.error(f"Error building conceptual bridge: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail="Failed to generate conceptual bridge."
            )

    @staticmethod
    def get_socratic_challenge(data: SocraticRequest):
        """
        Processes a single turn of the Socratic dialogue.
        
        Args:
            data: The history, user input, and confidence level.
        Returns:
            A structured logical challenge.
        """
        try:
            lm = dspy.LM(
                model=f"openai/{config['model_name']}",
                api_key=config['api_key'],
                api_base=config['api_base'],
                temperature=0.4  # Lower temperature for logical consistency
            )
            
            # Format list of strings into a cohesive prompt context
            formatted_history = "\n".join(data.conversation_history) if data.conversation_history else "No prior history."
            
            with dspy.context(lm=lm):
                challenger = dspy.ChainOfThought(SocraticChallenger)
                response = challenger(
                    conversation_history=formatted_history,
                    user_statement=data.user_statement,
                    confidence_level=data.confidence_level
                )
                return response
        except Exception as e:
            logger.error(f"Socratic Service Error: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail="The Socratic Challenger is currently unavailable."
            )
    @staticmethod
    def inoculate_bias(data: BiasRequest):
        """
        Creates a 'trap' scenario to train against cognitive biases.
        """
        try:
            # Handle random bias selection
            selected_bias = data.target_bias
            if not selected_bias:
                selected_bias = random.choice(["anchoring", "availability", "confirmation", "sunk_cost", "framing"])

            lm = dspy.LM(
                model=f"openai/{config['model_name']}",
                api_key=config['api_key'],
                api_base=config['api_base'],
                temperature=0.7 
            )
            
            formatted_history = "\n".join(data.conversation_history) if data.conversation_history else "New session."
            
            with dspy.context(lm=lm):
                # ChainOfThought helps the AI architect a believable 'trap'
                inoculator = dspy.ChainOfThought(CognitiveBiasInoculator)
                response = inoculator(
                    conversation_history=formatted_history,
                    target_bias=selected_bias,
                    user_interest=data.user_interest
                )
                # Ensure the selected bias is returned in the response
                response.target_bias = selected_bias
                return response
                
        except Exception as e:
            logger.error(f"Bias Inoculator Error: {str(e)}")
            raise HTTPException(status_code=500, detail="Bias training service unavailable.")