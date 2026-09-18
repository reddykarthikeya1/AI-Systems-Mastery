"""Tests for Langgraph State Reducer."""
from __future__ import annotations

import pytest
from p01_langgraph_state_reducer import langgraph_state_reducer


def test_langgraph_state_reducer():
    init = {'messages': ['hello'], 'iteration': 0}
    patch = {'messages': ['world'], 'iteration': 1}
    res = langgraph_state_reducer(init, patch)
    assert res['messages'] == ['hello', 'world']
    assert res['iteration'] == 1
