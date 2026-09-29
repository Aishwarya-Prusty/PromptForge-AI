import json
from app.prompt_engine import extract_json, build_user_prompt


def test_extract_json_from_plain_json():
    text = '{"objective":"test","context":"context"}'
    assert extract_json(text)["objective"] == "test"


def test_extract_json_from_code_fence():
    text = '```json\n{"objective":"test"}\n```'
    assert extract_json(text)["objective"] == "test"


def test_build_user_prompt_contains_input():
    prompt = build_user_prompt("Make a presentation about AI.", "detailed")
    assert "Make a presentation about AI." in prompt
    assert "detailed" in prompt
