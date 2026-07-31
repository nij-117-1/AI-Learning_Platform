import dspy
from typing import List, Literal, Optional , Dict

class HybridUserResponseGrader(dspy.Signature):
    """
    You are an expert Evaluator. You will grade a user's submission which may 
    consist of text, an image (handwriting, diagram, screenshot), or both.
    Your task is to synthesize all provided inputs, compare them against the 
    target objective, and provide a structured evaluation.
    """
    scenario: str = dspy.InputField(description="The context of the task.")
    question_asked: str = dspy.InputField(description="The specific question the user is answering.")
    
    # Optional inputs for flexibility
    user_answer_text: Optional[str] = dspy.InputField(default=None, description="The textual part of the user's response.")
    user_answer_image: Optional[dspy.Image] = dspy.InputField(default=None, description="The visual part of the user's response (e.g., photo of handwriting).")
    
    target_objective: str = dspy.InputField(description="The goal the user needs to achieve.")
    expected_level: Literal["beginner", "intermediate", "expert"] = dspy.InputField(description="Required depth.")

    # Model Reasoning Outputs
    combined_analysis: str = dspy.OutputField(description="A synthesized summary of both the text and image inputs provided by the user.")
    score: float = dspy.OutputField(description="Score from 0.0 to 10.0.")
    strengths: List[str] = dspy.OutputField(description="Positive aspects of the submission.")
    weaknesses: List[str] = dspy.OutputField(description="Gaps or errors found in text or image.")
    detailed_feedback: str = dspy.OutputField(description="Constructive advice for improvement.")
    is_target_met: bool = dspy.OutputField(description="Whether the objective was achieved.")

# 2. Define the DSPy Module
class PerformanceGrader(dspy.Module):
    def __init__(self):
        super().__init__()
        # ChainOfThought handles the 'reasoning' step automatically
        self.grader = dspy.ChainOfThought(HybridUserResponseGrader)

    def forward(self, scenario, question, target, level, text_answer=None, image_path=None):
        # Handle the image if provided
        img = dspy.Image(image_path) if image_path else None
        
        return self.grader(
            scenario=scenario,
            question_asked=question,
            user_answer_text=text_answer,
            user_answer_image=img,
            target_objective=target,
            expected_level=level
        )

        
class UserResponseGrader(dspy.Signature):
    """
    You are an expert Evaluator. Your task is to grade a user's response based on 
    how well it addresses a specific scenario, meets the target objectives, 
    and matches the expected expertise level. 
    """

    scenario: str = dspy.InputField(description="The context or situation the user was responding to.")
    question_asked: str = dspy.InputField(description="The specific question the user had to answer.")
    user_answer: str = dspy.InputField(description="The actual response provided by the user.")
    target_objective: str = dspy.InputField(description="What the user was supposed to achieve (e.g., 'Persuade the client', 'Explain technical debt').")
    expected_level: Literal["beginner", "intermediate", "expert"] = dspy.InputField(description="The depth and complexity expected in the answer.")

    score: float = dspy.OutputField(description="A score from 0.0 to 10.0 based on accuracy, depth, and tone.")
    strengths: List[str] = dspy.OutputField(description="What the user did well.")
    weaknesses: List[str] = dspy.OutputField(description="Where the user fell short or provided incorrect info.")
    detailed_feedback: str = dspy.OutputField(description="Constructive advice on how to reach the next proficiency level.")
    is_target_met: bool = dspy.OutputField(description="Whether the user successfully achieved the 'target_objective'.")

