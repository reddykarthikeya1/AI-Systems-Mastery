"""Reference Solution — Problem 01: Conversation Buffer Window Summary

Topic: 04 Agent Memory Systems
"""

from __future__ import annotations


def conversation_buffer_window_summary(messages: list[str], k: int = 2) -> tuple[str, list[str]]:
    if len(messages) <= k:
        return ("", list(messages))
    evicted = messages[:-k]
    summary = f"Summary of {len(evicted)} earlier turns: " + "; ".join(evicted)
    return (summary, list(messages[-k:]))
