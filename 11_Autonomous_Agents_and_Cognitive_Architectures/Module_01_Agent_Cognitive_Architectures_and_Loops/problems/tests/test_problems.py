"""Tests for React Thought Action Parser."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_react_thought_action_parser import react_thought_action_parser
except ImportError:
    from p01_react_thought_action_parser import react_thought_action_parser


def test_react_thought_action_parser():
    text = """Thought: Need to search temperature
Action: search_weather
Action Input: Paris
"""
    p = react_thought_action_parser(text)
    assert p['thought'] == "Need to search temperature"
    assert p['action'] == "search_weather"
    assert p['action_input'] == "Paris"
    assert p['final_answer'] is None
