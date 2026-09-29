from typing import List
from pydantic import BaseModel, Field


class PromptResult(BaseModel):
    """Validated structured result returned by the local LLM."""

    objective: str = Field(description="The main task the user wants completed.")
    context: str = Field(description="Relevant background or context for the task.")
    audience: str = Field(description="The intended audience of the final response.")
    requirements: List[str] = Field(default_factory=list)
    tone: str = Field(description="Recommended tone/style.")
    output_format: str = Field(description="Expected response format.")
    constraints: List[str] = Field(default_factory=list)
    optimized_prompt: str = Field(description="The final reusable optimized prompt.")


class PromptVersions(BaseModel):
    detailed: PromptResult
    concise: PromptResult
    professional: PromptResult
