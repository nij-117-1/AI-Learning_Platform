from pydantic import BaseModel, Field
from typing import Literal, Optional
from pydantic import BaseModel, Field
from typing import Literal

class RiddleRequest(BaseModel):
    field_of_interest: str = Field(..., example="Ancient Architecture")
    # Now accepts any string, not just specific categories
    target_domain: str 
    difficulty_level: str

class RiddleResponse(BaseModel):
    riddle_text: str
    solution: str
    cognitive_trigger: str

class EvaluationRequest(BaseModel):
    riddle_text: str
    solution: str
    user_answer: str

class EvaluationResponse(BaseModel):
    is_correct: bool
    feedback: str
    thought_redirection: str




class BridgeRequest(BaseModel):
    concept_a: str = Field(..., example="Photosynthesis")
    concept_b: str = Field(..., example="Blockchain")
    abstraction_depth: str = "structural"

class BridgeResponse(BaseModel):
    structural_analogy: str
    bridging_narrative: str
    insight_question: str
    cognitive_flexibility_score: int

from pydantic import BaseModel, Field
from typing import Literal, List, Optional

# ... (Previous schemas remain)

class SocraticRequest(BaseModel):
    conversation_history: List[str] = Field(
        default=[], 
        description="List of previous exchanges to maintain context."
    )
    user_statement: str = Field(..., example="I believe technology always improves human happiness.")
    confidence_level: str = "medium"

class SocraticResponse(BaseModel):
    logical_fallacy_check: str
    falsification_question: str
    edge_case_scenario: str
    refined_perspective: str

class BiasRequest(BaseModel):
    conversation_history: List[str] = Field(default=[])
    user_interest: str = Field(..., example="Crypto Trading")
    target_bias: Optional[str] = None

class BiasResponse(BaseModel):
    target_bias: str
    scenario_setup: str
    intuitive_trap: str
    rational_analysis: str
    real_world_application: str


class PuzzleRequest(BaseModel):
    field_of_interest: str = Field(..., example="Deep Sea Exploration")
    puzzle_type: str
    target_domain: str
    difficulty_level: str

class PuzzleResponse(BaseModel):
    puzzler_persona: str
    puzzle_text: str
    solution: str
    cognitive_trigger: str

class PuzzleEvaluationRequest(BaseModel):
    puzzle_context: str = Field(..., description="The full text of the puzzle.")
    puzzle_type: str = Field(..., description="Type of puzzle (e.g., cipher, logic grid).")
    official_solution: str = Field(..., description="The factual correct answer and logic.")
    user_response: str = Field(..., description="The user's input/answer.")

class PuzzleEvaluationResponse(BaseModel):
    is_correct: bool
    accuracy_score: float = Field(..., ge=0, le=1)
    evaluation_feedback: str
    hint_redirection: Optional[str] = None
    metacognitive_prompt: str