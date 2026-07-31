import dspy
import logging
from typing import List, Dict, Optional, Any
import string
from typing import List, Optional, Literal
from learning.guides.schemas import (
    GuideRequest, GuideResponse, 
    DailyPlannerRequest, DailyPlannerResponse,
    ProjectArchitectRequest, ProjectArchitectResponse, ProjectSuggestorRequest, ProjectSuggestorResponse, ProjectIdea
)
from learning.guides.schemas import (
    WhatToLearnRequest, WhatToLearnResponse, 
    LearningTopicSuggestion
)
from config import master_llm_config as config
import random
import uuid
logger = logging.getLogger(__name__)

class TaskGivingAgent(dspy.Signature):
    """
    You are a Mentor and Skill Master. Your goal is to generate actionable, 
    highly relevant tasks/projects to help a user master a specific skill.
    Consider their current level and previous work to ensure a logical 
    progression in difficulty and complexity.
    """
    random_seed: str = dspy.InputField(
        description="A unique UUID or seed to ensure randomness in the generation process."
    )
    learning_subject: str = dspy.InputField(description="What the user is currently learning.")
    target_goal: str = dspy.InputField(description="The end goal or dream project the user wants to achieve.")
    current_level: str = dspy.InputField(description="The user's skill level (e.g., Beginner, Intermediate, Advanced).")
    num_tasks: int = dspy.InputField(description="The number of tasks/projects to generate.")
    previous_tasks: Optional[List[str]] = dspy.InputField(default=[], description="List of tasks the user has already completed.")
    custom_instructions: Optional[str] = dspy.InputField(default=None, description="Specific preferences (e.g., 'focus on backend', 'no external libraries').")

    mentor_feedback: str = dspy.OutputField(description="A brief, encouraging assessment of the user's progress and the logic behind the new tasks.")
    task_list: List[Dict[str, Any]] = dspy.OutputField(description="""
        A structured list of tasks. Each task must contain:
        - 'title': Name of the project/task
        - 'description': Detailed explanation of what to build
        - 'difficulty': (Easy/Medium/Hard) relative to current level
        - 'learning_outcomes': Key concepts this task will reinforce
        - 'estimated_hours': Estimated time to complete
    """)

class ProjectSuggestor(dspy.Signature):
    """
    You are a Strategic Innovation Consultant. Your task is to generate a specific 
    number of high-impact, real-world project use cases based on a primary topic 
    and industry. Each project must be distinct, technically challenging, 
    and solve a legitimate professional pain point.
    """
    
    topic: str = dspy.InputField(description="The core technology or subject matter (e.g., Vector Databases, LLMs, Blockchain).")
    industry: str = dspy.InputField(description="The vertical to apply the technology (e.g., Supply Chain, Legal, Healthcare).")
    num_use_cases: int = dspy.InputField(description="The exact number of unique project ideas to generate.")
    existing_suggestions: Optional[List[str]] = dspy.InputField(
        default=[], 
        desc="A list of project titles or concepts already suggested. DO NOT repeat these."
    )
    user_instructions: Optional[str] = dspy.InputField(
        default="", 
        desc="Specific constraints or preferences (e.g., 'Focus on cost-saving', 'Use Python only', 'Target SME businesses')."
    )
    random_seed: str = dspy.InputField(description="A unique seed to ensure creativity and variety in results.")

    brief_strategy: str = dspy.OutputField(description="A short overview of how the topic transforms the industry.")
    projects: List[Dict[str, str]] = dspy.OutputField(description="""
        A list of project objects. Each object must contain:
        - 'title': A professional project name.
        - 'problem': The specific industry pain point being addressed.
        - 'key_features': A summary of the 3 most important technical features.
    """)

class DailyLearningPlanner(dspy.Signature):
    """
    Expert Educational Consultant. Design a roadmap that bridges current knowledge 
    to a specific target mastery level, ensuring continuity from previous work.
    """
    random_seed: str = dspy.InputField(
        description="A unique UUID or seed to ensure randomness in the generation process."
    )
    master_topic: str = dspy.InputField(desc="The broad field (e.g., 'DevOps', 'Machine Learning').")
    subtopic_preference: Optional[str] = dspy.InputField(desc="Specific area to focus on today.")
    
    user_level: Literal["beginner", "intermediate", "advanced"] = dspy.InputField(desc="Current level.")
    target_mastery: Literal["familiarity", "competency", "expert-level troubleshooting", "architectural-design"] = dspy.InputField(
        desc="The depth of understanding the user wants to reach by end of day."
    )
    
    existing_knowledge: str = dspy.InputField(desc="What the user already knows.")
    learning_focus: Literal["practical", "debugging", "theoretical", "project-based"] = dspy.InputField()
    previously_learned_topics: Optional[str] = dspy.InputField(desc="Context from the previous session.")
    
    learning_objective: str = dspy.OutputField(desc="Clear statement of achievement.")
    mastery_gap_analysis: str = dspy.OutputField(desc="A brief note on what is missing to reach the target_mastery.")
    structured_roadmap: List[str] = dspy.OutputField(desc="Step-by-step tasks.")
    recommended_exercise: str = dspy.OutputField(desc="A challenge designed to test the target mastery level.")
    resource_suggestions: str = dspy.OutputField()


class RealWorldProjectArchitect(dspy.Signature):
    """
    You are a Senior Product Architect. Given a Master Topic and a specific Subtopic, 
    generate a unique, high-impact real-world project idea. 
    Use the 'random_seed' to ensure the project concept is creative and distinct.
    """
    random_seed: str = dspy.InputField(
        description="A unique UUID or seed to ensure randomness in the generation process."
    )
    master_topic: str = dspy.InputField(desc="The broad field of study.")
    subtopic_focus: str = dspy.InputField(desc="The specific niche to master today.")
    target_mastery: str = dspy.InputField(desc="The skill level to reach (e.g. competency, architectural).")
    random_seed: str = dspy.InputField(desc="A unique string to force creative variety.")
    preferred_industry: Optional[str] = dspy.InputField(desc="User's choice of industry (e.g., Healthcare, Gaming, Space Exploration).")

    project_name: str = dspy.OutputField(desc="A unique, professional name for the project.")
    industry_context: str = dspy.OutputField(desc="The industry this project belongs to (e.g., Healthcare, FinTech, EdTech).")
    problem_statement: str = dspy.OutputField(desc="The real-world problem this project solves.")
    
    technical_requirements: List[str] = dspy.OutputField(desc="List of specific features that must be implemented to ensure 'Full Knowledge'.")
    stretch_goals: List[str] = dspy.OutputField(desc="Advanced features to move from competency to expert-level.")
    validation_criteria: str = dspy.OutputField(desc="How the user can prove the project is successful and mastery is achieved.")


class WhatToLearnToday(dspy.Signature):
    """
    Personalized learning recommender. Analyze user interests, history, and 
    specifically avoid repeating previous suggestions. Tailor the response 
    to any custom user instructions provided.
    """
    broader_topic: str = dspy.InputField(description="The general domain (e.g., Computer Science, Cooking).")
    specific_interest: str = dspy.InputField(description="The specific sub-topic the user wants to focus on.")
    learned_before: str = dspy.InputField(description="Background knowledge to avoid teaching basics.")
    
    previous_suggestions: Optional[List[str]] = dspy.InputField(
        default=[], 
        description="A list of topics already suggested to the user. DO NOT repeat these."
    )
    custom_user_input: Optional[str] = dspy.InputField(
        default=None, 
        description="Any specific user constraints or requests (e.g., 'focus on practical projects')."
    )
    
    topic_level: str = dspy.InputField(description="Difficulty: Beginner, Intermediate, or Advanced.")
    seed_uuid: str = dspy.InputField(description="Unique hash to ensure non-deterministic outputs.")

    recommendations: List[Dict[str, str]] = dspy.OutputField(description="""
        A list of 2-3 new topics. Each contains:
        - 'topic_name': The specific subject name.
        - 'reason': Why this is a good next step given the user's history and custom input.
    """)

    
class GuideService:
    @staticmethod
    async def generate_guide(data: GuideRequest) -> GuideResponse:
        """
        Executes the DSPy ChainOfThought to generate a learning path.
        
        Args:
            data: The validated GuideRequest object.
            
        Returns:
            GuideResponse: The structured mentor feedback and tasks.
        """
        try:
            lm = dspy.LM(
                model=f"openai/{config['model_name']}",
                api_key=config['api_key'],
                api_base=config['api_base'],
                temperature=0.4
            )

            with dspy.context(lm=lm):
                execution_uuid = str(uuid.uuid4())
                generator = dspy.ChainOfThought(TaskGivingAgent)
                prediction = generator(
                    learning_subject=data.subject,
                    target_goal=data.goal,
                    current_level=data.current_level,
                    num_tasks=data.count,
                    previous_tasks=data.history,
                    random_seed=execution_uuid ,
                    custom_instructions=data.instructions or "Focus on best practices."
                )
                
                return GuideResponse(
                    mentor_feedback=prediction.mentor_feedback,
                    tasks=prediction.task_list
                )
        except Exception as e:
            logger.error(f"Error generating guide: {str(e)}", exc_info=True)
            raise e
            
    @staticmethod
    async def generate_daily_plan(data: DailyPlannerRequest) -> DailyPlannerResponse:
        """
        Generates a focused daily study plan using DSPy.
        """
        try:
            lm = dspy.LM(
                model=f"openai/{config['model_name']}",
                api_key=config['api_key'],
                api_base=config['api_base'],
                temperature=0.4
            )

            with dspy.context(lm=lm):
                execution_uuid = str(uuid.uuid4())
                planner = dspy.ChainOfThought(DailyLearningPlanner)
                response = planner(
                    master_topic=data.master_topic,
                    subtopic_preference=data.subtopic_preference or "Logical progression",
                    user_level=data.user_level,
                    target_mastery=data.target_mastery,
                    existing_knowledge=data.existing_knowledge,
                    learning_focus=data.learning_focus,
                    random_seed=execution_uuid ,
                    previously_learned_topics=data.history or "None"
                )
                
                return DailyPlannerResponse(
                    learning_objective=response.learning_objective,
                    mastery_gap_analysis=response.mastery_gap_analysis,
                    structured_roadmap=response.structured_roadmap,
                    recommended_exercise=response.recommended_exercise,
                    resource_suggestions=response.resource_suggestions
                )
        except Exception as e:
            logger.error(f"Error in Daily Planner: {str(e)}", exc_info=True)
            raise e

    @staticmethod
    async def generate_unique_project(data: ProjectArchitectRequest) -> ProjectArchitectResponse:
        """
        Generates a unique project blueprint using random seeds and high temperature.
        """
        try:
            # Internal seed generation for variety
            seed = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            
            lm = dspy.LM(
                model=f"openai/{config['model_name']}",
                api_key=config['api_key'],
                api_base=config['api_base'],
                temperature=0.9  # High temperature for creativity
            )

            with dspy.context(lm=lm):
                execution_uuid = str(uuid.uuid4())
                architect = dspy.ChainOfThought(RealWorldProjectArchitect)
                response = architect(
                    master_topic=data.master_topic,
                    subtopic_focus=data.subtopic_focus,
                    target_mastery=data.target_mastery,
                    random_seed=execution_uuid ,
                    preferred_industry=data.preferred_industry or "General Tech",
                    
                )
                
                return ProjectArchitectResponse(
                    project_name=response.project_name,
                    industry_context=response.industry_context,
                    problem_statement=response.problem_statement,
                    technical_requirements=response.technical_requirements,
                    stretch_goals=response.stretch_goals,
                    validation_criteria=response.validation_criteria,
                    random_seed=seed
                )
        except Exception as e:
            logger.error(f"Error in Project Architect: {str(e)}", exc_info=True)
            raise e


    @staticmethod
    async def suggest_next_topics(data: WhatToLearnRequest) -> WhatToLearnResponse:
        """
        Executes the Enhanced WhatToLearnToday logic using DSPy ChainOfThought.
        """
        try:
            lm = dspy.LM(
                model=f"openai/{config['model_name']}",
                api_key=config['api_key'],
                api_base=config['api_base'],
                temperature=0.7
            )
            with dspy.context(lm=lm):
                recommender = dspy.ChainOfThought(WhatToLearnToday)
                
                prediction = recommender(
                    broader_topic=data.broader_topic,
                    specific_interest=data.specific_interest,
                    learned_before=data.learned_before,
                    previous_suggestions=data.previous_suggestions,
                    custom_user_input=data.custom_user_input,
                    topic_level=data.topic_level,
                    seed_uuid=str(uuid.uuid4())
                )
                
                # Extract recommendations and map to schema
                suggestions = [
                    LearningTopicSuggestion(**item) for item in prediction.recommendations
                ]
                
                return WhatToLearnResponse(
                    recommendations=suggestions
                )
                
        except Exception as e:
            logger.error(f"Error in Enhanced WhatToLearn Service: {str(e)}", exc_info=True)
            raise e


    @staticmethod
    async def suggest_projects(data: ProjectSuggestorRequest) -> ProjectSuggestorResponse:
        """
        Generates high-impact industry project use cases using DSPy.
        
        Args:
            data: Validated ProjectSuggestorRequest.
            
        Returns:
            ProjectSuggestorResponse: Strategic overview and project list.
        """
        try:
            lm = dspy.LM(
                model=f"openai/{config['model_name']}",
                api_key=config['api_key'],
                api_base=config.get('api_base'),
                temperature=0.7  # Balanced for creativity and professional tone
            )
            
            with dspy.context(lm=lm):
                # Generate unique UUID for randomness
                execution_uuid = str(uuid.uuid4())
                
                generator = dspy.ChainOfThought(ProjectSuggestor)
                prediction = generator(
                    topic=data.topic,
                    industry=data.industry,
                    num_use_cases=data.num_use_cases,
                    existing_suggestions=data.existing_suggestions,
                    user_instructions=data.user_instructions or "No specific instructions.",
                    random_seed=execution_uuid
                )
                
                # Mapping the dynamic DSPy OutputField to Pydantic objects
                project_list = [
                    ProjectIdea(**proj) for proj in prediction.projects
                ]
                
                return ProjectSuggestorResponse(
                    brief_strategy=prediction.brief_strategy,
                    projects=project_list
                )
        except Exception as e:
            logger.error(f"Project Suggestion Error: {str(e)}", exc_info=True)
            raise e