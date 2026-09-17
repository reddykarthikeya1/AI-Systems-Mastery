"""Pytest suite for Tool Execution and Constrained Generation problem bank."""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

# Test the solution by default, or stub if imported from problems/
SOL_DIR = Path(__file__).resolve().parent.parent / "solutions"
PROB_DIR = Path(__file__).resolve().parent.parent
if str(SOL_DIR) not in sys.path:
    sys.path.insert(0, str(SOL_DIR))

from p01_evaluate_react_trace import evaluate_react_trace


def test_evaluate_react_trace():
    trace = [
        {"type": "thought", "content": "Need current weather"},
        {"type": "action", "content": "get_weather('Seattle')"},
        {"type": "observation", "content": "65F, sunny"},
        {"type": "finish", "content": "Weather is 65F"}
    ]
    assert evaluate_react_trace(trace)["success"] == True
    # Exceeded budget
    assert evaluate_react_trace(trace, max_steps=2)["status"] == "BUDGET_EXCEEDED"

