"""Tests for Conversation Buffer Window Summary."""
from __future__ import annotations

import pytest
from p01_conversation_buffer_window_summary import conversation_buffer_window_summary


def test_conversation_buffer_window_summary():
    msgs = ["msg1", "msg2", "msg3", "msg4"]
    summ, rem = conversation_buffer_window_summary(msgs, 2)
    assert summ == "Summary of 2 earlier turns: msg1; msg2"
    assert rem == ["msg3", "msg4"]
