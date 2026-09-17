"""Tests for LLM Context Window Token Truncator."""
from __future__ import annotations

import pytest
from p01_sliding_token_budget import fit_prompt_budget


def test_sliding_token_budget():
    sys_msg = 'System'
    msgs = ['Hello', 'How are you?', 'Tell me a story about algorithms!']
    res = fit_prompt_budget(sys_msg, msgs, 20)
    assert res[0] == sys_msg
    assert len(res) >= 2
