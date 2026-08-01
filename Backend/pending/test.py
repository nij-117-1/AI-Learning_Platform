import dspy
from typing import Optional, Any, List, Dict, Literal

# ==============================================================================
# PART 1: THE FOUNDATIONAL FLEXIBLE WRITER
# ==============================================================================

class FlexibleWriter(dspy.Signature):
    """
    You are an adaptable AI agent. Use the provided System Prompt to determine your
    persona and behavioral constraints. Process the input data according to the
    user's specific instructions.
    """
    system_prompt: str = dspy.InputField(desc="The core persona and rules for the AI.")
    input_data: Any = dspy.InputField(desc="The primary data/content to be processed or transformed.")
    additional_user_input: Optional[str] = dspy.InputField(desc="Specific instructions or context from the user.")

    answer_message: str = dspy.OutputField(desc="A conversational summary of what was done.")
    updated_data: Any = dspy.OutputField(desc="The structured result or transformed version of the input data.")


# ==============================================================================
# PART 2: THE HIGH-STAKES EQ TRAINING SIGNATURES
# ==============================================================================

class HighStakesScenarioGenerator(dspy.Signature):
    """
    You are an Elite Corporate Strategist and Simulation Architect.
    Your role is to design the foundational context, stakes, and NPC profiles 
    for high-stakes executive training simulations. You create the 'board' 
    before the 'game' begins.
    """
    # Inputs
    user_role: str = dspy.InputField(desc="The professional role the user is playing (e.g., 'VP of Sales', 'CEO').")
    narrative_arc: str = dspy.InputField(desc="The overarching strategic goal (e.g., 'Deflecting a hostile takeover').")
    learning_focus: Literal["diplomatic_refusal", "assertive_silence", "implied_authority", "strategic_ambiguity"] = dspy.InputField(desc="The core EQ skill to be tested.")
    difficulty_level: Literal["Rising Star", "Seasoned Exec", "Ruthless Board", "Crisis Mode"] = dspy.InputField(desc="The intensity and hostility level of the simulation.")
    industry_context: Optional[str] = dspy.InputField(desc="Specific industry (e.g., 'Biotech', 'FinTech'). Defaults to general corporate.")

    # Outputs
    scenario_title: str = dspy.OutputField(desc="A dramatic, classified-style name for the simulation.")
    setting_description: str = dspy.OutputField(desc="A vivid, sensory description of the physical environment and atmospheric tension.")
    npc_profile: Dict[str, str] = dspy.OutputField(desc="""
        Structured profile of the primary counterpart. Must include:
        - 'name': Full name
        - 'title': Corporate title
        - 'personality': Core behavioral traits
        - 'hidden_motive': What they actually want vs. what they say
        - 'tell': A subtle non-verbal habit when lying or stressed
    """)
    initial_stakes: str = dspy.OutputField(desc="The concrete consequences of failure in this specific scenario.")
    opening_hook: str = dspy.OutputField(desc="The exact inciting incident or first line of dialogue that starts the simulation.")


class HighProfileEQTrainer(dspy.Signature):
    """
    You are a Strategic Communication Coach for Fortune 500 Executives.
    Your goal is to train the user in 'High EQ Diplomacy'—where they must
    communicate power, skepticism, or agreement through subtext rather than
    blunt words. You create a 'Social Chess' environment where the user learns
    to 'say it without saying it.'
    """
    # Chat Loop & Context Inputs
    previous_scenario: Optional[str] = dspy.InputField(desc="The context of the last lesson or meeting.")
    narrative_arc: str = dspy.InputField(desc="The overall goal (e.g., 'Gaining leverage in a merger', 'Deflecting blame').")
    chat_history: List[Dict[str, str]] = dspy.InputField(desc="The record of the dialogue so far.")
    learning_focus: Literal["diplomatic_refusal", "assertive_silence", "implied_authority", "strategic_ambiguity"] = dspy.InputField(desc="The specific EQ skill being practiced in this turn.")

    # Randomization & Control
    seed: str = dspy.InputField(desc="A seed to vary the political tension and personality of the NPCs (usually the NPC's hidden motive).")
    user_customization: Optional[str] = dspy.InputField(desc="Optional user constraints, e.g., 'Make my boss extremely aggressive'.")

    # Simulation Outputs
    rationale: str = dspy.OutputField(desc="The psychological breakdown of why this move is being made by the NPC.")
    meeting_scenario: str = dspy.OutputField(desc="A vivid description of the high-profile setting, the 'vibe', and the NPC's non-verbal cues.")
    npc_dialogue: str = dspy.OutputField(desc="What the high-profile counterparty actually says to the user.")
    eq_coach_message: str = dspy.OutputField(desc="Advice for the user on how to read the subtext and what to 'signal' in their next response.")
    suggested_strategies: List[str] = dspy.OutputField(desc="3 ways to reply: 1. The Direct approach, 2. The Subtle Pivot, 3. The Power Move.")


class EQResponseEvaluator(dspy.Signature):
    """
    You are a Senior Behavioral Analyst.
    Your job is to analyze the user's response in a high-stakes meeting.
    You evaluate the 'Subtext', 'Status Management', and 'Strategic Alignment'.
    You tell the user if they 'lost face', 'held ground', or 'gained leverage'.
    """
    # Context of the turn
    scenario_context: str = dspy.InputField(desc="The immediate situation/setting the user responded to.")
    npc_last_statement: str = dspy.InputField(desc="What the high-profile NPC said or did.")
    user_response: str = dspy.InputField(desc="The actual words or actions the user just took.")
    learning_focus: str = dspy.InputField(desc="The skill being practiced (e.g., 'Strategic Ambiguity').")

    # Analysis Outputs
    subtext_accuracy: str = dspy.OutputField(desc="Did the user correctly 'read' the NPC's hidden intent?")
    status_impact: Literal["Increased", "Maintained", "Diminished", "Completely Lost"] = dspy.OutputField(desc="How the user's social/professional status changed.")
    strategic_grade: Literal["A", "B", "C", "D", "F"] = dspy.OutputField(desc="How well the response aligns with the meeting's long-term goal.")
    strengths: List[str] = dspy.OutputField(desc="What the user did well in this specific turn.")
    critical_flaws: List[str] = dspy.OutputField(desc="Technical or EQ mistakes (e.g., 'Too defensive', 'Gave away too much info').")
    the_rewritten_pro_move: str = dspy.OutputField(desc="How a Master Negotiator would have said the exact same thing to get a better result.")
    coaching_tip: str = dspy.OutputField(desc="A psychological tip for the next turn.")


# ==============================================================================
# PART 3: THE CHAINED DSPY MODULE
# ==============================================================================

class ExecutiveEQPipeline(dspy.Module):
    """
    A complete DSPy Module that chains the Scenario Generator, 
    the EQ Trainer, and the Response Evaluator into a single workflow.
    """
    def __init__(self):
        super().__init__()
        # Initialize the predictors. 
        # We use ChainOfThought for the Evaluator to ensure deep analytical reasoning.
        self.generate_scenario = dspy.Predict(HighStakesScenarioGenerator)
        self.run_training_loop = dspy.Predict(HighProfileEQTrainer)
        self.evaluate_move = dspy.ChainOfThought(EQResponseEvaluator)

    def forward(self, user_role, narrative_arc, learning_focus, difficulty_level, user_response, chat_history):
        
        # 1. SCENARIO GENERATION: Build the world and the NPC
        scenario = self.generate_scenario(
            user_role=user_role,
            narrative_arc=narrative_arc,
            learning_focus=learning_focus,
            difficulty_level=difficulty_level,
            industry_context=None
        )
        
        # 2. INTERACTION: Generate the NPC's reaction based on the generated world
        # We use the NPC's 'hidden_motive' as the seed to ensure psychological consistency
        interaction = self.run_training_loop(
            previous_scenario=scenario.scenario_title,
            narrative_arc=narrative_arc,
            chat_history=chat_history,
            learning_focus=learning_focus,
            seed=scenario.npc_profile.get('hidden_motive', 'Unknown'), 
            user_customization=None
        )
        
        # 3. EVALUATION: Grade the user's response against the NPC's move
        evaluation = self.evaluate_move(
            scenario_context=scenario.setting_description,
            npc_last_statement=interaction.npc_dialogue,
            user_response=user_response,
            learning_focus=learning_focus
        )
        
        # Return a unified prediction object containing all submodule outputs
        return dspy.Prediction(
            scenario=scenario,
            interaction=interaction,
            evaluation=evaluation
        )


# ==============================================================================
# PART 4: EXECUTION & MAIN BLOCK
# ==============================================================================

def configure_dspy(model_name: str, api_key: str, api_base: str, temperature: float = 0.7):
    """Helper to configure the DSPy Language Model."""
    lm = dspy.LM(
        model=f'openai/{model_name}',
        api_key=api_key,
        api_base=api_base,
        temperature=temperature,
        cache=False
    )
    dspy.configure(lm=lm)
    return lm

def run_standalone_scenario_gen(user_inputs: dict):
    """Runs just the Scenario Generator submodule."""
    generator = dspy.Predict(HighStakesScenarioGenerator)
    return generator(**user_inputs)

def run_full_pipeline(user_inputs: dict):
    """Runs the complete chained Executive EQ Pipeline."""
    pipeline = ExecutiveEQPipeline()
    return pipeline(**user_inputs)


if __name__ == "__main__":
    # --- CONFIGURATION ---
    # Replace with your actual API credentials / local LLM endpoint
    config = {
        "model_name": "gpt-4o",  # or gpt-4-turbo, gpt-3.5-turbo, etc.
        "api_key": "your-api-key-here",
        "api_base": "https://api.openai.com/v1", # Or your local proxy like http://localhost:4567/v1
    }
    
    configure_dspy(**config)

    # --- EXAMPLE 1: STANDALONE SCENARIO GENERATOR ---
    print("="*50)
    print("RUNNING STANDALONE SCENARIO GENERATOR")
    print("="*50)
    
    scenario_inputs = {
        "user_role": "Chief Technology Officer",
        "narrative_arc": "Delay a product launch without admitting the code is buggy",
        "learning_focus": "strategic_ambiguity",
        "difficulty_level": "Ruthless Board",
        "industry_context": "FinTech"
    }
    
    scenario_result = run_standalone_scenario_gen(scenario_inputs)
    print(f"\n🎬 SCENARIO: {scenario_result.scenario_title}")
    print(f"🏢 SETTING: {scenario_result.setting_description[:150]}...")
    print(f"🕵️ NPC HIDDEN MOTIVE: {scenario_result.npc_profile.get('hidden_motive', 'N/A')}")
    print(f"🪝 OPENING HOOK: {scenario_result.opening_hook}\n")


    # --- EXAMPLE 2: FULL CHAINED PIPELINE ---
    print("="*50)
    print("RUNNING FULL EXECUTIVE EQ PIPELINE")
    print("="*50)

    pipeline_inputs = {
        "user_role": "Chief Technology Officer",
        "narrative_arc": "Delay a product launch without admitting the code is buggy",
        "learning_focus": "strategic_ambiguity",
        "difficulty_level": "Ruthless Board",
        # The user's response to the NPC's opening hook
        "user_response": "We are currently exploring some final optimization vectors to ensure maximum market impact upon release.",
        "chat_history": []
    }

    full_result = run_full_pipeline(pipeline_inputs)

    # Print Scenario Details
    print(f"\n🎬 SCENARIO: {full_result.scenario.scenario_title}")
    print(f"🕵️ NPC: {full_result.scenario.npc_profile.get('name')} ({full_result.scenario.npc_profile.get('title')})")
    
    # Print Interaction Details
    print(f"\n🗣️ NPC DIALOGUE: {full_result.interaction.npc_dialogue}")
    print(f"🧠 NPC RATIONALE: {full_result.interaction.rationale}")
    print(f"💡 COACH MESSAGE: {full_result.interaction.eq_coach_message}")
    
    # Print Evaluation Details
    print(f"\n--- 📊 PERFORMANCE EVALUATION ---")
    print(f"🏆 Grade: {full_result.evaluation.strategic_grade}")
    print(f"📈 Status Impact: {full_result.evaluation.status_impact}")
    print(f"🎯 Subtext Accuracy: {full_result.evaluation.subtext_accuracy}")
    print(f"✅ Strengths: {', '.join(full_result.evaluation.strengths)}")
    print(f"❌ Critical Flaws: {', '.join(full_result.evaluation.critical_flaws)}")
    print(f"👑 THE PRO MOVE: {full_result.evaluation.the_rewritten_pro_move}")