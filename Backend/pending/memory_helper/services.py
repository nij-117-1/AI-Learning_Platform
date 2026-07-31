import dspy
import logging
from typing import List, Dict, Any
from config import master_llm_config as config
from learning.memory_helper.schemas import MemoryRequest
from typing import List, Dict, Optional, Literal

logger = logging.getLogger(__name__)

class MemoryAgent(dspy.Signature):
    """
    You are a Memory Specialist. Your goal is to transform complex information 
    into memorable chunks using cognitive science techniques. 
    You create structured study aids, mnemonics, or mental frameworks 
    to help humans retain data long-term.
    """
    content_to_remember: str = dspy.InputField(description="The facts, data, or topic the user wants to memorize.")
    preferred_technique: Optional[str] = dspy.InputField(
        default="Best Fit", 
        description="Optional: Specific technique like 'Mnemonics', 'Feynman Technique', or 'Method of Loci'."
    )
    
    explanation: str = dspy.OutputField(description="A brief explanation of why this technique works for this data.")
    memory_hooks: List[Dict[str, str]] = dspy.OutputField(description="""
        A list of memory aids. Each item contains:
        - 'concept': The specific piece of info.
        - 'hook': The mnemonic, visualization, or shortcut to remember it.
    """)
    retention_plan: str = dspy.OutputField(description="A simple 3-step plan to review this information.")

class MemoryService:
    def __init__(self):  # Fixed: Double underscores
        try:
            # Note: Ensure dspy version is 2.5+. Older versions use dspy.OpenAI()
            self.lm = dspy.LM(
                model=f"openai/{config['model_name']}",
                api_key=config['api_key'],
                api_base=config['api_base'],
                cache=False, # Often helps with debugging
                temperature=config.get('temperature', 0.5)
            )
        except Exception as e:
            logger.error(f"Configuration error: {e}")
            raise RuntimeError("LLM Configuration is incomplete.")

    def run_agent(self, request_data: MemoryRequest) -> Any:
        with dspy.context(lm=self.lm):
            # Fixed: Changed MemoryAgentSignature to MemoryAgent
            agent = dspy.ChainOfThought(MemoryAgent)
            try:
                response = agent(
                    content_to_remember=request_data.topic,
                    preferred_technique=request_data.technique
                )
                return response
            except Exception as e:
                logger.error(f"DSPy Error: {str(e)}")
                raise e