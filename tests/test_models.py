from app.models import PromptResult


def test_prompt_result_validation():
    result = PromptResult(
        objective="Create a presentation",
        context="Climate change",
        audience="Students",
        requirements=["Include causes", "Include effects"],
        tone="Educational",
        output_format="10-slide presentation",
        constraints=["Use simple language"],
        optimized_prompt="Create a 10-slide presentation about climate change for students.",
    )

    assert result.objective == "Create a presentation"
    assert len(result.requirements) == 2
    assert result.optimized_prompt.startswith("Create")
