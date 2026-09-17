"""Problem 01 — Conversation Buffer Window Summary

Topic: 04 Agent Memory Systems
Target: Production-grade implementation

Prune conversation history keeping last k messages and summarizing evicted turns.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def conversation_buffer_window_summary(messages: list[str], k: int = 2) -> tuple[str, list[str]]:
    """If len(messages) <= k: summary is "", remaining is messages.
    If len(messages) > k:
    evicted = messages[:-k]
    summary = f"Summary of {len(evicted)} earlier turns: " + "; ".join(evicted)
    remaining = messages[-k:]
    Returns (summary, remaining).
    """
    raise NotImplementedError("Implement conversation_buffer_window_summary")
