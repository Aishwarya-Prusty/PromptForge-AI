import json
import time
from datetime import datetime
from pathlib import Path

import streamlit as st

from .models import PromptResult
from .prompt_engine import optimize_all_versions, optimize_with_ollama


st.set_page_config(
    page_title="PromptForge AI",
    page_icon="✨",
    layout="wide",
)

# -------------------------
# Styling
# -------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 3rem;
        font-weight: 750;
        margin-bottom: 0;
    }
    .subtitle {
        font-size: 1.15rem;
        color: #667085;
        margin-top: 0.2rem;
        margin-bottom: 1.5rem;
    }
    .prompt-box {
        background: #f7f8fa;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 18px;
        white-space: pre-wrap;
    }
    .small-label {
        font-size: 0.85rem;
        font-weight: 650;
        color: #667085;
        text-transform: uppercase;
        letter-spacing: .04em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "result" not in st.session_state:
    st.session_state.result = None
if "versions" not in st.session_state:
    st.session_state.versions = None
if "original" not in st.session_state:
    st.session_state.original = ""

st.markdown('<div class="main-title">✨ PromptForge AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Turn simple instructions into clear, structured and reusable AI prompts.</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("⚙️ Settings")
    model = st.text_input("Ollama model", value="llama3.2")
    st.caption("The model must be installed locally in Ollama.")

    st.divider()
    st.subheader("What PromptForge does")
    st.write("1. Understands your instruction")
    st.write("2. Identifies missing prompt components")
    st.write("3. Builds a structured prompt")
    st.write("4. Validates the result with Pydantic")
    st.write("5. Lets you copy/export the result")

    st.divider()
    st.caption("No external AI API is required.")

examples = {
    "Presentation": "Make a presentation about climate change.",
    "Coding": "Write a Python program to manage student marks.",
    "Resume": "Create a resume for a software engineer.",
    "Learning": "Explain machine learning to a beginner.",
    "Email": "Write an email asking my professor for two days leave.",
}

selected_example = st.selectbox(
    "Try an example",
    ["Custom"] + list(examples.keys()),
)

default_text = examples.get(selected_example, st.session_state.original)

user_input = st.text_area(
    "Your simple instruction",
    value=default_text,
    height=150,
    placeholder="Example: Make a presentation about artificial intelligence.",
)

col1, col2, col3 = st.columns(3)

with col1:
    optimize_clicked = st.button("✨ Optimize Prompt", type="primary", use_container_width=True)

with col2:
    versions_clicked = st.button("🔄 Generate 3 Versions", use_container_width=True)

with col3:
    clear_clicked = st.button("🗑️ Clear", use_container_width=True)

if clear_clicked:
    st.session_state.result = None
    st.session_state.versions = None
    st.session_state.original = ""
    st.rerun()

if optimize_clicked:
    if not user_input.strip():
        st.error("Please enter an instruction first.")
    else:
        with st.spinner("Llama 3.2 is optimizing your prompt..."):
            start = time.perf_counter()
            try:
                result, raw = optimize_with_ollama(
                    user_input.strip(),
                    model=model.strip() or "llama3.2",
                    style="detailed",
                )
                elapsed = time.perf_counter() - start
                st.session_state.result = result
                st.session_state.original = user_input.strip()
                st.session_state.versions = None
                st.session_state.elapsed = elapsed
                st.session_state.raw = raw
            except Exception as exc:
                st.error(str(exc))

if versions_clicked:
    if not user_input.strip():
        st.error("Please enter an instruction first.")
    else:
        with st.spinner("Generating detailed, concise and professional versions..."):
            start = time.perf_counter()
            try:
                results, raw_outputs = optimize_all_versions(
                    user_input.strip(),
                    model=model.strip() or "llama3.2",
                )
                elapsed = time.perf_counter() - start
                st.session_state.versions = results
                st.session_state.result = None
                st.session_state.original = user_input.strip()
                st.session_state.elapsed = elapsed
                st.session_state.raw = raw_outputs
            except Exception as exc:
                st.error(str(exc))

if st.session_state.result:
    result: PromptResult = st.session_state.result

    st.divider()
    st.subheader("Original vs Optimized")

    left, right = st.columns(2)
    with left:
        st.markdown("**Original instruction**")
        st.markdown(f'<div class="prompt-box">{st.session_state.original}</div>', unsafe_allow_html=True)
    with right:
        st.markdown("**Optimized prompt**")
        st.code(result.optimized_prompt, language="text")

    st.caption(f"Generation time: {st.session_state.get('elapsed', 0):.2f} seconds")

    st.divider()
    st.subheader("🧩 Prompt Structure")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Objective**")
        st.write(result.objective)

        st.markdown("**Context**")
        st.write(result.context)

        st.markdown("**Audience**")
        st.write(result.audience)

        st.markdown("**Tone**")
        st.write(result.tone)

    with c2:
        st.markdown("**Output format**")
        st.write(result.output_format)

        st.markdown("**Requirements**")
        for item in result.requirements:
            st.write(f"• {item}")

        st.markdown("**Constraints**")
        for item in result.constraints:
            st.write(f"• {item}")

    json_data = result.model_dump()

    st.divider()
    st.subheader("📦 Validated JSON")
    st.json(json_data)

    download_data = json.dumps(
        {
            "original_prompt": st.session_state.original,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "result": json_data,
        },
        indent=2,
    )

    st.download_button(
        "⬇️ Download JSON",
        data=download_data,
        file_name="promptforge_result.json",
        mime="application/json",
    )

if st.session_state.versions:
    st.divider()
    st.subheader("🔄 Prompt Versions")

    tabs = st.tabs(["Detailed", "Concise", "Professional"])
    names = ["detailed", "concise", "professional"]

    for tab, name in zip(tabs, names):
        result = st.session_state.versions[name]
        with tab:
            st.code(result.optimized_prompt, language="text")
            st.markdown("**Objective:**")
            st.write(result.objective)
            st.markdown("**Requirements:**")
            for item in result.requirements:
                st.write(f"• {item}")

    all_json = {
        name: result.model_dump()
        for name, result in st.session_state.versions.items()
    }

    st.download_button(
        "⬇️ Download all versions as JSON",
        data=json.dumps(all_json, indent=2),
        file_name="promptforge_versions.json",
        mime="application/json",
    )

st.divider()
st.caption("PromptForge AI • Generative AI Capstone Project 2026 • Python + Streamlit + Ollama + Llama 3.2 + Pydantic")
