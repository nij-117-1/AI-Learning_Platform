import logging
from typing import Any, Optional

import dspy

from core.config import master_llm_config as config
from tools.charts.schemas import ChartRequest, ChartResponse

logger = logging.getLogger(__name__)


class ChartError(Exception):
    """Base exception for all charts module failures."""


class GenerationError(ChartError):
    """Raised when the underlying DSPy pipeline fails to produce content."""


class ChartJSGenerator(dspy.Signature):
    """
    You are an expert Data Visualizer. Your task is to generate clean, responsive
    Chart.js code embedded within a <div> container. Chart.js is already installed
    via npm.

    Rules:
    - Use the provided data to populate the chart.
    - If 'previous_code' is provided, refactor or update it based on 'custom_instructions'.
    - Ensure the output includes the <canvas> element and the <script> block.
    """

    custom_instructions: str = dspy.InputField(description="User preferences for chart type, colors, or labels.")
    data_input: Any = dspy.InputField(description="The raw data (JSON, CSV, or text) to be visualized.")
    previous_code: Optional[str] = dspy.InputField(default=None, description="Existing Chart.js code to modify.")

    answer_message: str = dspy.OutputField(description="A brief explanation of the chart created and how to use it.")
    chart_div_code: str = dspy.OutputField(description="The full HTML/JS code block containing the <div>, <canvas>, and Chart.js logic.")


class ChartService:
    """Business layer wrapping the DSPy Chart.js generation pipeline."""

    def __init__(self) -> None:
        self.lm = dspy.LM(
            model=f"openai/{config['model_name']}",
            api_key=config['api_key'],
            api_base=config['api_base'],
            temperature=config.get('temperature', 0.4),
            cache=False,
        )

    def generate_chart(self, data: ChartRequest) -> ChartResponse:
        """
        Generates Chart.js code using DSPy ChainOfThought.

        Args:
            data (ChartRequest): The validated request schema.

        Returns:
            ChartResponse: The explanation message and generated HTML/JS code.

        Raises:
            GenerationError: If the DSPy pipeline fails to produce content.
        """
        try:
            with dspy.context(lm=self.lm):
                logger.info("Generating Chart.js code via DSPy ChainOfThought")
                generator = dspy.ChainOfThought(ChartJSGenerator)
                response = generator(
                    data_input=data.data_input,
                    custom_instructions=data.custom_instructions,
                    previous_code=data.previous_code,
                )
            return ChartResponse(
                answer_message=response.answer_message,
                chart_div_code=response.chart_div_code,
            )
        except Exception as exc:
            logger.error("Chart generation failed: %s", exc, exc_info=True)
            raise GenerationError(str(exc)) from exc
