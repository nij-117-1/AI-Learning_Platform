import dspy
from typing import Optional, Literal, Dict
from config import master_llm_config as config

# config ={
#     "model_name": "qwen3-vl-235b-instruct",
#     "api_key": "amd-hcbu-unix-2025",
#     "api_base": "https://litellm.45-76-29-2.nip.io/v1",
#     "temperature": 0.4
# }


# 1. Define the Signature
class MermaidGenerator(dspy.Signature):
    """
    You are an expert Mermaid.js developer. Your task is to generate or update 
    Mermaid.js syntax for diagrams (flowcharts, sequence diagrams, class diagrams, etc.).
    
    Rules:
    1. Return ONLY the Mermaid.js code block within the 'updated_code' field.
    2. If 'existing_code' is provided, modify it based on the instruction.
    3. Ensure the syntax is correct and can be rendered by Mermaid loaders.
    """
    user_instruction: str = dspy.InputField(description="Specific visual change or diagram request.")
    context: Optional[str] = dspy.InputField(description="Business logic or technical context for the diagram content.")
    existing_code: Optional[str] = dspy.InputField(default=None, description="Current Mermaid code to be refined.")

    
    updated_code: str = dspy.OutputField(description="The final valid Mermaid.js code starting with the diagram type (e.g., 'graph TD'). Do not include markdown code delimiters")
    answer_message: str = dspy.OutputField(description="A brief explanation of what was added or changed.")

# 2. Implementation Function
def execute_mermaid_task(instruction: str, context: str = "", code: str = None):
    """
    Executes the Mermaid generation/edit task using the DSPy framework.
    """
    lm = dspy.LM(
        model=f"openai/{config['model_name']}",
        api_key=config['api_key'],
        # Use .get() for optional keys to avoid KeyErrors
        api_base=config.get('api_base'),
        temperature=config.get('temperature', 0.5),
        max_tokens=15000,
    )

    with dspy.context(lm=lm):
        # We use Predict here for Mermaid as the syntax is text-heavy and straightforward, 
        # but ChainOfThought is an option if logic is complex.
        generator = dspy.Predict(MermaidGenerator)
        
        response = generator(
            user_instruction=instruction,
            context=context,
            existing_code=code
        )
        
        return response


import dspy
from typing import Optional, List, Dict, Any

# 1. Define the Signature
class DrawIOCodeGenerator(dspy.Signature):
    """
    You are an expert Draw.io (diagrams.net) architect. Your goal is to generate or 
    edit XML/mxGraph code for diagrams based on user instructions.
    
    If 'existing_code' is provided, modify it according to the instructions.
    If 'existing_code' is empty, generate a new diagram from scratch.
    Ensure the XML is valid and compatible with Draw.io import.
    """
    user_instruction: str = dspy.InputField(description="What the user wants to build or change in the diagram.")
    context: Optional[str] = dspy.InputField(description="Background info about the system, flow, or business logic.")
    existing_code: Optional[str] = dspy.InputField(default=None, description="The current Draw.io XML/mxGraph code to be edited.")
    
    
    updated_code: str = dspy.OutputField(description="The complete, valid Draw.io XML/mxGraph code. Do not include markdown code delimiters")
    answer_message: str = dspy.OutputField(description="A concise explanation of the changes or the logic used to build the diagram.")

# 2. Implementation Wrapper
def execute_drawio_task( instruction: str, context: str = "", code: str = None):
    """
    Executes the DrawIO generation or editing task.
    """
    # Configure the LM
    lm = dspy.LM(
        model=f"openai/{config['model_name']}",
        api_key=config['api_key'],
        # Use .get() for optional keys to avoid KeyErrors
        api_base=config.get('api_base'),
        temperature=config.get('temperature', 0.5),
        max_tokens=15000
    )

    with dspy.context(lm=lm):
        # We use ChainOfThought for diagramming because layout logic 
        # requires "reasoning" about coordinates and connections.
        generator = dspy.Predict(DrawIOCodeGenerator)
        
        response = generator(
            user_instruction=instruction,
            context=context,
            existing_code=code
        )
        
        return response
