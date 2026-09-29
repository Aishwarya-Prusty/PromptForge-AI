import json
import re
from typing import Any, Dict

from pydantic import ValidationError

from .models import PromptResult


SYSTEM_PROMPT = """
You are PromptForge AI, an expert prompt optimization assistant.

Your job is to transform a user's simple or poorly written instruction into
a clear, specific, useful prompt for a Generative AI system.

IMPORTANT RULES:
1. Preserve the user's original intent. Never replace the requested task with
   a different task.
2. Do not invent personal facts, dates, names, statistics, sources, or claims.
3. Add useful structure only when it helps the requested task.
4. Identify the objective, context, audience, requirements, tone, output format,
   and constraints.
5. If the user did not provide enough information, make conservative,
   clearly generic assumptions rather than inventing specific facts.
6. The optimized prompt must be directly reusable by another AI model.
7. Return ONLY valid JSON matching this schema:

{
  "objective": "string",
  "context": "string",
  "audience": "string",
  "requirements": ["string"],
  "tone": "string",
  "output_format": "string",
  "constraints": ["string"],
  "optimized_prompt": "string"
}
"""


def build_user_prompt(user_input: str, style: str = "detailed") -> str:
    style_instruction = {
        "detailed": "Create a comprehensive but focused optimized prompt.",
        "concise": "Create a compact optimized prompt with only the most useful details.",
        "professional": "Create a polished professional prompt suitable for academic or workplace use.",
    }.get(style, "Create a clear optimized prompt.")

    return f"""
Optimization style: {style}
{style_instruction}

User's original instruction:
---BEGIN USER INPUT---
{user_input}
---END USER INPUT---

Return the required JSON object only.
"""


def extract_json(text: str) -> Dict[str, Any]:
    """Extract a JSON object even if the model accidentally adds code fences."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start >= 0 and end > start:
            return json.loads(cleaned[start:end + 1])
        raise


def optimize_with_ollama(user_input: str, model: str = "llama3.2", style: str = "detailed"):
    """
    Call Ollama's local HTTP API.
    Returns (PromptResult, raw_response_text).
    """
    try:
        import requests
    except ImportError as exc:
        raise RuntimeError("The requests package is missing. Run: pip install -r requirements.txt") from exc

    if not user_input.strip():
        raise ValueError("Please enter a prompt before optimizing it.")

    payload = {
        "model": model,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.2
        },
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(user_input, style)},
        ],
    }

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Could not connect to Ollama. Make sure Ollama is running and "
            "Llama 3.2 is installed with: ollama pull llama3.2"
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "Ollama took too long to respond. Try a shorter input or a smaller local model."
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Ollama request failed: {exc}") from exc

    data = response.json()
    raw = data.get("message", {}).get("content", "")
    if not raw:
        raise RuntimeError("Ollama returned an empty model response.")

    try:
        parsed = extract_json(raw)
        result = PromptResult.model_validate(parsed)
    except (json.JSONDecodeError, ValidationError, TypeError) as exc:
        raise RuntimeError(
            "The model returned output that did not match the required PromptForge structure. "
            f"Raw output: {raw[:500]}"
        ) from exc

    return result, raw


def optimize_all_versions(user_input: str, model: str = "llama3.2"):
    results = {}
    raw_outputs = {}
    for style in ("detailed", "concise", "professional"):
        result, raw = optimize_with_ollama(user_input, model=model, style=style)
        results[style] = result
        raw_outputs[style] = raw
    return results, raw_outputs
