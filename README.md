# PromptForge AI – Intelligent Prompt Optimizer

Generative AI Capstone Project 2026

PromptForge AI converts simple user instructions into clear, detailed,
structured and reusable AI prompts.

## 1. Features

- Simple Streamlit web interface
- Local Llama 3.2 model through Ollama
- No external AI API required
- Prompt optimization
- Detailed, concise and professional versions
- Objective/context/audience/requirements/tone/output/constraints extraction
- Pydantic structured-output validation
- JSON export
- Original vs optimized prompt comparison
- Error handling for Ollama connection and invalid model output
- Automated tests with pytest

## 2. Architecture

User
  ↓
Streamlit
  ↓
Python
  ↓
Prompt Optimization Instructions
  ↓
Ollama
  ↓
Llama 3.2
  ↓
JSON
  ↓
Pydantic Validation
  ↓
Optimized Prompt
  ↓
Streamlit

## 3. Requirements

Recommended:

- Python 3.10 or newer
- Ollama installed
- Llama 3.2 model downloaded
- 8 GB RAM or more is recommended for local model use

## 4. Installation

### Step 1 – Create a virtual environment

Windows:

    python -m venv venv
    venv\Scripts\activate

macOS/Linux:

    python3 -m venv venv
    source venv/bin/activate

### Step 2 – Install Python packages

    pip install -r requirements.txt

### Step 3 – Install and start Ollama

Install Ollama from the official Ollama website.

Then download the model:

    ollama pull llama3.2

Test the model:

    ollama run llama3.2

If the model opens an interactive chat, Ollama is working.

### Step 4 – Run PromptForge AI

    python run.py

Or directly:

    streamlit run app/app.py

Streamlit will display a local URL, normally:

    http://localhost:8501

## 5. How to Use

1. Open the application.
2. Enter a simple instruction.
3. Click "Optimize Prompt".
4. Wait for Llama 3.2 to generate the structured result.
5. Compare the original and optimized prompts.
6. Inspect objective, context, audience, requirements, tone, output format and constraints.
7. Download the validated JSON if needed.

You can also click "Generate 3 Versions" to create:

- Detailed
- Concise
- Professional

## 6. Example

Input:

    Make a presentation about climate change.

The application should generate a prompt that specifies useful details such as
the audience, topics, presentation structure, tone, output format and
constraints while preserving the original topic.

## 7. Testing

Run:

    pytest -q

The tests validate:

- Pydantic prompt schema
- JSON extraction
- Prompt construction

The tests do not require Ollama because they test deterministic application
components. Full end-to-end testing requires Ollama and Llama 3.2.

## 8. Project Structure

    PromptForge_AI/
    ├── app/
    │   ├── __init__.py
    │   ├── app.py
    │   ├── models.py
    │   └── prompt_engine.py
    ├── data/
    │   └── sample_prompts.json
    ├── tests/
    │   ├── test_models.py
    │   └── test_prompt_engine.py
    ├── docs/
    ├── requirements.txt
    ├── run.py
    └── README.md

## 9. Important

This project intentionally runs the LLM locally through Ollama.

Do not add API keys or passwords to the source code.

The application optimizes prompts; it does not guarantee that every downstream
AI model will produce a perfect answer.

## 10. Capstone Report

The accompanying capstone report should contain:

1. Problem Statement
2. Objectives and Scope
3. Solution and Features
4. Tech Stack
5. Knowledge Base and Data
6. System Architecture
7. Implementation Highlights
8. Testing and Results
9. Evaluation and Metrics
10. Screenshots
11. Challenges and Learnings
12. Future Improvements
13. Conclusion
14. References and Links
