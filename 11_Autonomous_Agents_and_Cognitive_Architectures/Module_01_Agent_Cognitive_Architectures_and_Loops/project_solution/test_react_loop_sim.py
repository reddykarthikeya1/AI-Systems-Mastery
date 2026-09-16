"""Unit and integration tests for ReAct Loop Engine."""

from __future__ import annotations

from typing import List
import pytest
from react_loop_sim import ReActLoopEngine


def dummy_search(query: str) -> str:
    if "h100" in query.lower():
        return "700W TDP"
    return "No results"


def dummy_calc(expression: str) -> str:
    return str(eval(expression))


@pytest.fixture
def react_engine() -> ReActLoopEngine:
    tools = {
        "Search": dummy_search,
        "Calculator": dummy_calc,
    }
    return ReActLoopEngine(tools=tools, max_steps=5, cycle_threshold=2)


def test_react_loop_multi_step_success(react_engine: ReActLoopEngine):
    # Simulated scripted responses
    def scripted_llm(prompt: str, reflections: List[str]) -> str:
        if "700W TDP" not in prompt:
            return 'Thought: I must find the TDP of H100.\nAction: Search\nAction Input: {"query": "H100"}'
        elif "16800" not in prompt:
            return 'Thought: I need to calculate total watts over 24h.\nAction: Calculator\nAction Input: {"expression": "700 * 24"}'
        else:
            return 'Thought: Calculation complete.\nFinal Answer: An H100 uses 16800 Wh over 24 hours.'

    trajectory = react_engine.run("Calculate H100 daily energy usage", scripted_llm)
    assert trajectory.success is True
    assert len(trajectory.steps) == 3
    assert trajectory.steps[-1].final_answer == "An H100 uses 16800 Wh over 24 hours."
    assert trajectory.steps[0].action_name == "Search"
    assert "700W TDP" in trajectory.steps[0].observation


def test_cycle_detection_and_reflection(react_engine: ReActLoopEngine):
    # Scripted LLM that repeats identical search
    def looping_llm(prompt: str, reflections: List[str]) -> str:
        if reflections:
            return 'Thought: I was stuck in a loop, terminating.\nFinal Answer: Aborted due to loop.'
        return 'Thought: Searching same thing.\nAction: Search\nAction Input: {"query": "H100"}'

    trajectory = react_engine.run("Test loop goal", looping_llm)
    assert trajectory.success is True
    assert len(trajectory.reflections) > 0
    assert "Cycle Detected" in trajectory.reflections[0]


def test_max_steps_guard(react_engine: ReActLoopEngine):
    # Scripted LLM that never finishes
    def never_ending_llm(prompt: str, reflections: List[str]) -> str:
        step = len(prompt.split("Action:"))
        return f'Thought: Step {step}\nAction: Search\nAction Input: {{"query": "item_{step}"}}'

    trajectory = react_engine.run("Infinite goal", never_ending_llm)
    assert trajectory.success is False
    assert "Exceeded maximum steps" in trajectory.error
