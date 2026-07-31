from pydantic import BaseModel, Field
from typing import List, Optional

# --- Request Models ---

class GuideRequest(BaseModel):
    subject: str = Field(..., example="FastAPI")
    goal: str = Field(..., example="Become Python Expert")
    current_level: str = Field(..., example="Intermediate")
    count: int = Field(default=3, ge=1, le=10)
    history: List[str] = Field(default_factory=list)
    instructions: Optional[str] = Field(None, example="Clean folder structure")

class DailyPlannerRequest(BaseModel):
    master_topic: str = Field(..., example="React.js")
    subtopic_preference: Optional[str] = Field(None, example="Compound Component Pattern")
    # Changed from Literal to str
    user_level: str = Field(..., example="intermediate")
    target_mastery: str = Field(..., example="architectural-design")
    existing_knowledge: str = Field(..., example="Can build basic components and use hooks")
    learning_focus: str = Field(..., example="practical")
    history: Optional[str] = Field(None, example="State management with Redux")

class ProjectArchitectRequest(BaseModel):
    master_topic: str = Field(..., example="Backend Engineering")
    subtopic_focus: str = Field(..., example="WebSockets & Real-time Communication")
    target_mastery: str = Field(..., example="architectural-design")
    preferred_industry: Optional[str] = Field(None, example="Healthcare")


class WhatToLearnRequest(BaseModel):
    broader_topic: str = Field(..., example="Software Engineering")
    specific_interest: str = Field(..., example="Web Development with Python")
    learned_before: str = Field(..., example="Basic Python and introductory Web concepts")
    previous_suggestions: List[str] = Field(
        default_factory=list, 
        example=["Decorators in Python", "Basic Flask Routing"]
    )
    custom_user_input: Optional[str] = Field(
        None, 
        example="I want to focus on security and databases today."
    )
    topic_level: str = Field(..., example="intermediate")
# --- Response Models ---

class Task(BaseModel):
    title: str
    description: str
    difficulty: str
    learning_outcomes: List[str]
    estimated_hours: int

class GuideResponse(BaseModel):
    mentor_feedback: str
    tasks: List[Task]

class DailyPlannerResponse(BaseModel):
    learning_objective: str
    mastery_gap_analysis: str
    structured_roadmap: List[str]
    recommended_exercise: str
    resource_suggestions: str

class ProjectArchitectResponse(BaseModel):
    project_name: str
    industry_context: str
    problem_statement: str
    technical_requirements: List[str]
    stretch_goals: List[str]
    validation_criteria: str
    random_seed: str 

class LearningTopicSuggestion(BaseModel):
    topic_name: str
    reason: str

class WhatToLearnResponse(BaseModel):
    recommendations: List[LearningTopicSuggestion]


class ProjectIdea(BaseModel):
    title: str = Field(..., description="A professional project name")
    problem: str = Field(..., description="The specific industry pain point")
    key_features: str = Field(..., description="Summary of the 3 most important features")

class ProjectSuggestorRequest(BaseModel):
    topic: str = Field(..., example="Vector Databases")
    industry: str = Field(..., example="Healthcare")
    num_use_cases: int = Field(default=3, ge=1, le=10)
    user_instructions: Optional[str] = Field(None, example="Focus on cost-saving")
    existing_suggestions: List[str] = Field(
        default_factory=list, 
        example=["AI Patient Triage", "Medical Record Indexer"]
    )

class ProjectSuggestorResponse(BaseModel):
    brief_strategy: str
    projects: List[ProjectIdea]