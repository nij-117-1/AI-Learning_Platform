from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import dspy

class HybridUserResponseGrader(dspy.Signature):
    """
    You are an expert Evaluator. You will grade a user's submission which may 
    consist of text, an image (handwriting, diagram, screenshot), or both.
    Your task is to synthesize all provided inputs, compare them against the 
    target objective, and provide a structured evaluation.
    """
    scenario: str = dspy.InputField(description="The context of the task.")
    question_asked: str = dspy.InputField(description="The specific question the user is answering.")
    target_objective: str = dspy.InputField(description="The goal the user needs to achieve.")
    expected_level: Literal["beginner", "intermediate", "expert"] = dspy.InputField(description="Required depth.")
    # Optional inputs for flexibility
    user_answer_text: Optional[str] = dspy.InputField(default=None, description="The textual part of the user's response.")
    user_answer_image: Optional[dspy.Image] = dspy.InputField(default=None, description="The visual part of the user's response (e.g., photo of handwriting).")
    


    # Model Reasoning Outputs
    combined_analysis: str = dspy.OutputField(description="A synthesized summary of both the text and image inputs provided by the user.")
    score: float = dspy.OutputField(description="Score from 0.0 to 10.0.")
    strengths: List[str] = dspy.OutputField(description="Positive aspects of the submission.")
    weaknesses: List[str] = dspy.OutputField(description="Gaps or errors found in text or image.")
    detailed_feedback: str = dspy.OutputField(description="Constructive advice for improvement.")
    is_target_met: bool = dspy.OutputField(description="Whether the objective was achieved.")

    
class GradingResponse(BaseModel):
    combined_analysis: str
    score: float
    strengths: List[str]
    weaknesses: List[str]
    detailed_feedback: str
    is_target_met: bool
    status: str = "success"