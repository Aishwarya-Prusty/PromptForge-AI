# PromptForge AI – 2 to 3 Minute Demo Script

## 0:00–0:20 – Introduction

"PromptForge AI is a Generative AI application that converts simple user
instructions into structured and optimized prompts. It is designed for users
who know what they want from AI but do not know how to write an effective
prompt."

## 0:20–0:45 – Show the interface

Open the Streamlit application.

Say:

"The application has a simple input area. I can enter a normal instruction
without using any advanced prompt engineering."

Enter:

    Make a presentation about climate change.

## 0:45–1:20 – Optimize

Click Optimize Prompt.

Say:

"PromptForge sends the instruction to Llama 3.2 running locally through Ollama.
The model identifies useful prompt components and generates a structured
version."

Show:

- Objective
- Context
- Audience
- Requirements
- Tone
- Output format
- Constraints

## 1:20–1:50 – Compare

Show the original and optimized prompt.

Say:

"The important point is that the system does not simply make the prompt longer.
It makes the objective and expected output clearer while preserving the
original intent."

## 1:50–2:15 – Structured validation

Show the JSON section.

Say:

"The model output is validated using Pydantic. This makes the output
predictable and easier for the Python application to process."

## 2:15–2:40 – Multiple versions

Click Generate 3 Versions.

Show:

- Detailed
- Concise
- Professional

Say:

"The same user request can also be converted into different prompt styles."

## 2:40–3:00 – Technology summary

"PromptForge AI uses Python, Streamlit, Ollama, Llama 3.2, Pydantic and JSON.
The major Generative AI concept demonstrated is local LLM-based prompt
optimization with structured output validation."
