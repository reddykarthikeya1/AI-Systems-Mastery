"""Unit tests for Tool Execution Engine."""

from __future__ import annotations

import time
import pytest
from tool_execution_engine import ToolExecutionEngine


def sample_calc(a: int, b: int, operation: str = "add") -> int:
    """Performs basic arithmetic."""
    if operation == "add":
        return a + b
    elif operation == "mul":
        return a * b
    raise ValueError(f"Unknown operation: {operation}")


def slow_tool(duration: float) -> str:
    """Sleeps for a duration."""
    time.sleep(duration)
    return "Finished"


@pytest.fixture
def engine() -> ToolExecutionEngine:
    eng = ToolExecutionEngine(default_timeout_sec=0.5)
    eng.register(sample_calc)
    eng.register(slow_tool)
    return eng


def test_schema_generation(engine: ToolExecutionEngine):
    schemas = engine.get_schemas()
    calc_schema = next(s for s in schemas if s["name"] == "sample_calc")

    assert calc_schema["name"] == "sample_calc"
    assert "a" in calc_schema["parameters"]["properties"]
    assert calc_schema["parameters"]["properties"]["a"]["type"] == "integer"
    assert "a" in calc_schema["parameters"]["required"]
    assert "operation" not in calc_schema["parameters"]["required"]  # has default


def test_valid_dispatch_with_coercion(engine: ToolExecutionEngine):
    # Pass 'a' and 'b' as strings to test coercion
    result = engine.dispatch("sample_calc", {"a": "10", "b": 20, "operation": "mul"})
    assert result == "200"


def test_validation_missing_param(engine: ToolExecutionEngine):
    result = engine.dispatch("sample_calc", {"a": 10})
    assert "Validation Error" in result
    assert "Missing required parameter 'b'" in result


def test_timeout_enforcement(engine: ToolExecutionEngine):
    result = engine.dispatch("slow_tool", {"duration": 1.5}, timeout_sec=0.2)
    assert "Execution Timeout" in result
