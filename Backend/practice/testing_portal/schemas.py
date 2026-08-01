from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

MCQ_QUESTION_TYPES = Literal["academic", "practical", "scenario-based", "conceptual", "recall"]
MCQ_DIFFICULTY_LEVELS = Literal["beginner", "intermediate", "advanced", "expert"]

THEORETICAL_QUESTION_TYPES = Literal["academic", "practical", "case-study", "philosophical", "architectural"]
THEORETICAL_DIFFICULTY_LEVELS = Literal["basic", "intermediate", "advanced", "architectural"]

ANSWER_RESPONSE_FORMATS = Literal["bullet_points", "paragraph", "step_by_step", "technical_whitepaper"]


class MCQRequest(BaseModel):
    """Request model for generating multiple choice questions."""

    topic: str = Field(..., example="Python Concurrency", description="The subject for the questions")
    question_type: MCQ_QUESTION_TYPES = Field(..., description="The style of the questions to generate")
    num_questions: int = Field(..., gt=0, le=10, description="The number of MCQs to generate")
    difficulty_level: MCQ_DIFFICULTY_LEVELS = Field(..., description="The complexity level of the questions")
    context_setting: str = Field(
        ...,
        example="Senior Backend Engineer Interview",
        description="The scenario (e.g., Job Interview, University Exam)",
    )
    past_questions: Optional[str] = Field(None, description="Previously generated questions to avoid repetition")
    custom_instructions: Optional[str] = Field(None, description="Specific user requirements")


class MCQOption(BaseModel):
    """A set of four answer options for a multiple choice question."""

    A: str = Field(..., description="Option A text")
    B: str = Field(..., description="Option B text")
    C: str = Field(..., description="Option C text")
    D: str = Field(..., description="Option D text")


class MCQItem(BaseModel):
    """A single generated multiple choice question."""

    question_text: str = Field(..., description="The actual question string")
    options: MCQOption = Field(..., description="The four answer options")
    correct_answer: str = Field(..., description="The key of the correct option (e.g., 'A')")


class MCQResponse(BaseModel):
    """Response model containing a list of generated MCQs."""

    questions: List[MCQItem] = Field(..., description="The generated multiple choice questions")
    status: str = "success"


class TheoreticalRequest(BaseModel):
    """Request model for generating open-ended theoretical questions."""

    topic: str = Field(..., example="Microservices", description="The subject or domain for the questions")
    question_type: THEORETICAL_QUESTION_TYPES = Field(..., description="The style of the theoretical question")
    source_context: Optional[str] = Field(None, description="Source text or data for analysis")
    num_questions: int = Field(..., gt=0, le=5, description="The number of questions to generate")
    difficulty_level: THEORETICAL_DIFFICULTY_LEVELS = Field(..., description="The depth and complexity of the questions")
    context_setting: str = Field(
        ...,
        example="High-Tech Enterprise Interview",
        description="The scenario (e.g., Coding Interview, University Exam)",
    )
    past_questions: Optional[str] = Field(None, description="Previously generated questions to ensure variety")
    custom_instructions: Optional[str] = Field(None, example="Focus on speed vs consistency.")


class TheoreticalItem(BaseModel):
    """A single generated open-ended theoretical question."""

    question_text: str = Field(..., description="The descriptive open-ended question")
    focus_area: str = Field(..., description="A brief tag (e.g., 'Scalability', 'Ethics')")
    evaluation_criteria: str = Field(..., description="What a high-quality answer should include")


class TheoreticalResponse(BaseModel):
    """Response model containing a list of generated theoretical questions."""

    questions: List[TheoreticalItem] = Field(..., description="The generated theoretical questions")
    status: str = "success"


class AnswerRequest(BaseModel):
    """Request model for generating a Subject Matter Expert answer."""

    question: str = Field(..., example="Explain Consensus Mechanisms in Blockchain.")
    context: str = Field(..., example="Job Interview for Senior Developer")
    difficulty: str = Field(..., example="Expert", description="The complexity level of the expected answer")
    response_format: ANSWER_RESPONSE_FORMATS = Field(..., description="The structural style of the response")
    custom_instructions: Optional[str] = Field(None, description="Additional specific constraints or information")


class AnswerResponse(BaseModel):
    """Response model containing the generated expert answer."""

    answer_text: str = Field(..., description="The generated response/answer")
    key_concepts_covered: List[str] = Field(..., description="Core concepts or keywords included in the answer")
    status: str = "success"


class MCQSolverRequest(BaseModel):
    """Request model for analyzing an existing MCQ."""

    question: str = Field(..., example="What is the primary function of the mitochondria?")
    options: Dict[str, str] = Field(
        ...,
        example={"A": "Protein synthesis", "B": "ATP production", "C": "Storage", "D": "Waste"},
    )
    context: Optional[str] = Field(None, example="High School Biology Quiz")


class MCQSolverResponse(BaseModel):
    """Response model containing the identified correct option and reasoning."""

    correct_option: Literal["A", "B", "C", "D"] = Field(..., description="The letter of the correct option")
    reasoning: str = Field(..., description="A brief explanation of the correct answer and logic")
    status: str = "success"
