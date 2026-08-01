from typing import List, Dict, Optional
import dspy

class ScenarioGenerator(dspy.Signature):
    """
    You are a Negotiation Scenario Creator. Your job is to generate realistic,
    engaging negotiation scenarios for practice. Each scenario should include
    clear roles, conflicting interests, and enough context for both parties
    to have a meaningful discussion.
    """
    difficulty: str = dspy.InputField(description="Difficulty level: 'beginner', 'intermediate', 'advanced'")
    domain: str = dspy.InputField(description="Domain of negotiation (e.g., 'salary', 'real estate', 'business deal', 'diplomatic')")
    scenario: Dict = dspy.OutputField(description="""
        A dictionary containing:
        - 'title': A catchy scenario title
        - 'context': Background situation description (2-3 sentences)
        - 'your_role': The practice user's role/title
        - 'your_goal': What the user wants to achieve
        - 'your_constraints': Limits or restrictions the user faces
        - 'opponent_role': The AI opponent's role/title
        - 'opponent_goal': What the opponent wants to achieve
        - 'opponent_constraints': Limits the opponent faces
        - 'key_issues': List of 2-4 negotiable items/topics
        - 'starting_stance_opponent': How the opponent should open (first message)
    """)

class OpponentResponse(dspy.Signature):
    """
    You are playing the role of a negotiation counterparty. Stay in character
    based on the scenario details provided. Your goal is to represent the
    opponent's interests realistically — be cooperative but also advocate for
    their position. Do NOT reveal hidden constraints unless strategically
    appropriate during the negotiation.
    """
    scenario_context: str = dspy.InputField(description="Full scenario background and roles.")
    opponent_role: str = dspy.InputField(description="Your role/persona in this negotiation.")
    opponent_goal: str = dspy.InputField(description="What you want to achieve.")
    opponent_constraints: str = dspy.InputField(description="Your limitations and constraints.")
    conversation_history: str = dspy.InputField(description="Full negotiation transcript so far.")
    user_last_message: str = dspy.InputField(description="The user's most recent message.")
    
    response: str = dspy.OutputField(description=
        "Your reply as the opponent. Stay in character. 1-3 sentences typically."
    )
    internal_position: Dict = dspy.OutputField(description="""
        Your current internal state (not shared with user):
        - 'satisfaction': 0-10, how satisfied you are with progress
        - 'willingness_to_concede': 'high', 'medium', 'low'
        - 'concessions_made': List of things you've already given up
        - 'key_demands': What you still want
    """)

class MessageAnalyzer(dspy.Signature):
    """
    You are a negotiation coach analyzing a single message from a trainee.
    Identify what negotiation tactics, techniques, and communication
    approaches were used.
    """
    message: str = dspy.InputField(description="The user's last message to the opponent.")
    scenario_context: str = dspy.InputField(description="Brief scenario context.")
    
    tactics_used: List[str] = dspy.OutputField(description="""
        List of detected tactics, e.g.:
        - 'anchoring', 'reciprocity', 'framing', 'active_listening',
        - 'emotion_appeal', 'deadline_pressure', 'objective_criteria',
        - 'collaborative', 'competitive', 'compromise'
    """)
    effectiveness_rating: int = dspy.OutputField(
        description="Rate the message effectiveness from 1-10."
    )
    feedback_snippet: str = dspy.OutputField(
        description="One sentence of immediate feedback."
    )

class FeedbackEvaluator(dspy.Signature):
    """
    You are an expert negotiation coach. You've observed an entire
    negotiation practice session between a trainee and a simulated
    counterparty. Provide comprehensive feedback and a performance
    assessment.
    """
    scenario_context: str = dspy.InputField(description="Full scenario with roles and goals.")
    full_conversation: str = dspy.InputField(description="Complete negotiation transcript.")
    final_outcome: str = dspy.InputField(description="How the negotiation ended (agreement, impasse, etc.)")
    
    overall_score: int = dspy.OutputField(description="Overall performance score from 0-100.")
    scores_by_category: Dict = dspy.OutputField(description="""
        Scores (0-10) for each dimension:
        - 'preparation': Did they understand their role and goals?
        - 'communication': Were they clear, respectful, professional?
        - 'strategy': Did they use effective negotiation tactics?
        - 'listening': Did they respond to the opponent's points?
        - 'problem_solving': Did they seek creative solutions?
        - 'flexibility': Were they appropriately flexible?
    """)
    strengths: List[str] = dspy.OutputField(description="3-5 things they did well.")
    areas_for_improvement: List[str] = dspy.OutputField(description="3-5 areas to improve.")
    key_takeaways: List[str] = dspy.OutputField(description="3 memorable lessons from this session.")
    suggested_resources: List[str] = dspy.OutputField(description="2-3 book/article/video suggestions.")

class NegotiationPracticeSession:
    def __init__(self, model_name, api_key, api_base):
        self.lm = dspy.LM(
            model=f'openai/{model_name}',
            api_key=api_key,
            api_base=api_base,
            temperature=0.4,
            stop=None,
            cache=False
        )
        
        self.scenario_gen = dspy.Predict(ScenarioGenerator)
        self.opponent = dspy.Predict(OpponentResponse)
        self.analyzer = dspy.Predict(MessageAnalyzer)
        self.evaluator = dspy.Predict(FeedbackEvaluator)
        
        self.conversation = []
        self.scenario = None
        
    def start_session(self, difficulty="intermediate", domain="business"):
        with dspy.context(lm=self.lm):
            result = self.scenario_gen(difficulty=difficulty, domain=domain)
            self.scenario = result.scenario
            self.conversation = [{
                "role": "opponent",
                "message": self.scenario["starting_stance_opponent"]
            }]
            return self.scenario, self.scenario["starting_stance_opponent"]
    
    def user_turn(self, user_message: str):
        self.conversation.append({"role": "user", "message": user_message})
        
        history_str = "\n".join([
            f"[{m['role']}]: {m['message']}" for m in self.conversation
        ])
        
        with dspy.context(lm=self.lm):
            # Optional: analyze the user's message
            analysis = self.analyzer(
                message=user_message,
                scenario_context=str(self.scenario)
            )
            
            # Get opponent response
            response = self.opponent(
                scenario_context=str(self.scenario),
                opponent_role=self.scenario["opponent_role"],
                opponent_goal=self.scenario["opponent_goal"],
                opponent_constraints=self.scenario["opponent_constraints"],
                conversation_history=history_str,
                user_last_message=user_message
            )
        
        self.conversation.append({
            "role": "opponent",
            "message": response.response
        })
        
        return response.response, analysis
    
    def end_session(self, outcome_description: str):
        history_str = "\n".join([
            f"[{m['role']}]: {m['message']}" for m in self.conversation
        ])
        
        with dspy.context(lm=self.lm):
            evaluation = self.evaluator(
                scenario_context=str(self.scenario),
                full_conversation=history_str,
                final_outcome=outcome_description
            )
            return evaluation

if __name__ == "__main__":
    # Setup
    session = NegotiationPracticeSession(
        model_name="qwen3vl",
        api_key="sk-8529084399-hcbu",
        api_base="https://litellm.207-148-10-192.nip.io/v1"
    )
    
    # Start new scenario
    scenario, opening = session.start_session(
        difficulty="intermediate", 
        domain="salary"
    )
    print(f"📋 SCENARIO: {scenario['title']}")
    print(f"🎭 You are: {scenario['your_role']}")
    print(f"🎯 Your goal: {scenario['your_goal']}")
    print(f"\n💬 Opponent opens: {opening}")
    
    # Conversation loop
    max_turns = 8
    for turn in range(max_turns):
        user_msg = input(f"\n✅ Your response (turn {turn+1}): ")
        
        if user_msg.lower() in ["end", "quit"]:
            break
            
        opponent_reply, analysis = session.user_turn(user_msg)
        print(f"\n🔴 Opponent: {opponent_reply}")
        print(f"💡 Tactic tips: {analysis.feedback_snippet}")
    
    # End session
    outcome = input("\n📝 How did it end? (Describe the outcome): ")
    result = session.end_session(outcome)
    
    print(f"\n{'='*50}")
    print(f"📊 FINAL SCORE: {result.overall_score}/100")
    print(f"⭐ Strengths: {', '.join(result.strengths[:3])}")
    print(f"🔧 Improve: {', '.join(result.areas_for_improvement[:3])}")
    print(f"📖 Takeaways: {', '.join(result.key_takeaways)}")