Based on the **IQ Enhancement** concept, here is a modular DSPy toolkit targeting different cognitive domains: **Pattern Recognition**, **Fluid Reasoning**, **Critical Thinking**, **Lateral Thinking**, and **Metacognition**.

Each tool is designed as a `dspy.Signature` that can be used standalone or chained into a personalized training curriculum.

---

### 🧩 **1. Adaptive Riddle Generator** (Fluid Reasoning)
Targets **problem-solving flexibility** and **abstract thinking**.

```python
from typing import Literal, Optional
import dspy

class AdaptiveRiddleGenerator(dspy.Signature):
    """
    Generates personalized riddles that adapt to the user's current cognitive level.
    Targets: Working memory, pattern recognition, and deductive reasoning.
    """
    user_performance_history: Optional[str] = dspy.InputField(
        default=None,
        description="Summary of user's recent solve times and accuracy (e.g., 'solved 3/5 hard riddles, slow on lateral thinking')."
    )
    target_domain: Literal["verbal", "mathematical", "spatial", "lateral"] = dspy.InputField(
        description="Cognitive domain to challenge."
    )
    difficulty_level: Literal["novice", "intermediate", "expert", "genius"] = dspy.InputField(
        description="Current difficulty tier."
    )
    
    riddle_text: str = dspy.OutputField(description="The riddle/puzzle text. Must be solvable but challenging.")
    solution: str = dspy.OutputField(description="Clear explanation of the logic.")
    cognitive_trigger: str = dspy.OutputField(description="Which cognitive bias or pattern this riddle exploits or trains.")
    next_difficulty_recommendation: Literal["novice", "intermediate", "expert", "genius"] = dspy.OutputField(
        description="Recommended next level based on this puzzle's complexity."
    )
```

---

### 🔗 **2. Conceptual Bridge Builder** (Associative/ Creative IQ)
Targets **divergent thinking** and **analogical reasoning** (key for innovation).

```python
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
```

---

### 🧠 **3. Socratic Challenger** (Critical Thinking & Metacognition)
Targets **cognitive reflection** and **bias detection**.

```python
class SocraticChallenger(dspy.Signature):
    """
    Challenges user's reasoning rather than providing answers.
    Targets: Intellectual humility, logical consistency, and argumentation skills.
    """
    user_statement: str = dspy.InputField(description="The user's opinion or conclusion.")
    confidence_level: Literal["low", "medium", "high", "certain"] = dspy.InputField(
        description="How certain the user claims to be."
    )
    
    logical_fallacy_check: Optional[str] = dspy.OutputField(
        description="If present, name the fallacy; else null."
    )
    falsification_question: str = dspy.OutputField(
        description="A question that could prove the user's statement wrong (Karl Popper style)."
    )
    edge_case_scenario: str = dspy.OutputField(
        description="A hypothetical scenario where their logic breaks."
    )
    refined_perspective: str = dspy.OutputField(
        description="A more nuanced version of their original statement."
    )
```

---

### 📊 **4. Pattern Completion Trainer** (Fluid Intelligence)
Raw **IQ-test style** pattern recognition (matrices, sequences).

```python
class PatternCompletionTrainer(dspy.Signature):
    """
    Generates matrix reasoning tasks similar to Raven's Progressive Matrices.
    Targets: Visual-spatial reasoning, inductive logic, and rule extraction.
    """
    complexity: Literal["single_rule", "dual_rules", "hierarchical", "analogical"] = dspy.InputField(
        description="Type of pattern transformation."
    )
    
    pattern_description: str = dspy.OutputField(
        description="Text-based representation of the pattern (e.g., 'Rotation + Size increase')."
    )
    sequence_data: List[Dict[str, Any]] = dspy.OutputField(
        description="""
        A list representing the matrix rows. Each item:
        - 'elements': list of attributes (e.g., ['circle', 'large', 'rotated_90'])
        - 'missing': bool (true if this is the empty slot to fill)
        """
    )
    distractor_options: List[str] = dspy.OutputField(
        description="3 wrong answers that test common cognitive traps."
    )
    correct_answer: str = dspy.OutputField(description="The correct completion.")
    rule_explanation: str = dspy.OutputField(
        description="Step-by-step breakdown of the logical rules governing the pattern."
    )
```

---

### 🔄 **5. Cognitive Bias Inoculator** (Rationality)
Targets **System 2 thinking** (Kahneman's terminology) - overriding instincts.

```python
class CognitiveBiasInoculator(dspy.Signature):
    """
    Presents scenarios designed to trigger specific biases, then reveals the trap.
    Targets: Rational thinking, heuristics awareness, and decision-making quality.
    """
    target_bias: Literal["anchoring", "availability", "confirmation", "sunk_cost", "framing"] = dspy.InputField(
        description="Specific bias to train against."
    )
    context: str = dspy.InputField(description="User's field of interest (e.g., 'finance', 'medicine').")
    
    scenario_setup: str = dspy.OutputField(
        description="A realistic story that stealthily triggers the target bias."
    )
    intuitive_trap: str = dspy.OutputField(
        description="The 'gut feeling' wrong answer most people choose."
    )
    rational_analysis: str = dspy.OutputField(
        description="Slow, System 2 breakdown showing the correct approach."
    )
    real_world_application: str = dspy.OutputField(
        description="How to spot this bias in the user's actual life/work."
    )
```

---

### 🎯 **6. Feynman Simplifier with Gap Detection** (Crystallized Intelligence)
Targets **knowledge compression** and **understanding depth**.

```python
class FeynmanSimplifier(dspy.Signature):
    """
    Forces explanation of complex topics in simple terms, then identifies knowledge gaps.
    Targets: Teaching ability, concept mastery, and explanatory depth.
    """
    complex_topic: str = dspy.InputField(description="Topic to explain (e.g., 'Quantum Entanglement').")
    user_explanation: str = dspy.InputField(description="The user's current attempt at explaining it.")
    target_audience: str = dspy.InputField(
        description="E.g., '5-year-old', 'high school student', 'expert colleague'."
    )
    
    gap_analysis: List[str] = dspy.OutputField(
        description="List of concepts the user glossed over or misunderstood."
    )
    analogy_recommendation: str = dspy.OutputField(
        description="Perfect analogy for this specific topic and audience."
    )
    simplified_version: str = dspy.OutputField(
        description="The gold-standard simple explanation (2-3 sentences max)."
    )
    recursion_prompt: str = dspy.OutputField(
        description="A question to ask the user that forces them to explain a sub-component they missed."
    )
```

---

### 🏗️ **Suggested System Architecture**

Chain these tools into an **IQ Enhancement Pipeline**:

```python
class IQEnhancementOrchestrator(dspy.Signature):
    """
    Acts as a personal trainer for cognitive enhancement.
    """
    user_profile: Dict[str, Any] = dspy.InputField(
        description="Current IQ estimates per domain, strengths, weaknesses."
    )
    daily_time_budget_minutes: int = dspy.InputField()
    
    training_curriculum: List[Dict[str, Any]] = dspy.OutputField(
        description="""
        Ordered list of exercises for the session:
        - 'tool_name': Which signature to use
        - 'parameters': Input values
        - 'cognitive_target': Which skill this hones
        """
    )
    progression_path: str = dspy.OutputField(
        description="Long-term strategy for moving from current to target cognitive level."
    )
```

### 💡 **Why This Works for IQ Enhancement**

1. **Adaptive Difficulty**: The system doesn't bore experts or overwhelm beginners (via performance history tracking)
2. **Transfer Learning**: The Conceptual Bridge Builder explicitly trains the ability to apply knowledge across domains (the definition of fluid intelligence)
3. **Metacognitive Awareness**: Socratic Challenger and Bias Inoculator improve "thinking about thinking"
4. **Dual Process Theory**: Targets both fast intuition (Pattern Completion) and slow logic (Bias Inoculator)

**Pro Tip**: Add a `dspy.ChainOfThought` variant for the Complex Pattern Trainer and Socratic modules—these require step-by-step reasoning traces to be effective tutors.

Would you like me to implement the **chaining logic** that connects these into a daily "Brain Training" flow, or dive deeper into any specific cognitive domain (e.g., spatial reasoning via text description)?