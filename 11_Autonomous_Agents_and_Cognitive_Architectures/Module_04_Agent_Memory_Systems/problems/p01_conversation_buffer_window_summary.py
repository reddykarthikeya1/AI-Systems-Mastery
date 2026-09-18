"""Problem 01 — Conversation Buffer Window Summary

Topic: 04 Agent Memory Systems
Target: Production-grade implementation

Prune conversation history keeping last k messages and summarizing evicted turns.

Example:
    >>> conversation_buffer_window_summary(['msg1', 'msg2', 'msg3', 'msg4'], 2)
    ('Summary of 2 earlier turns: msg1; msg2', ['msg3', 'msg4'])

Hints:
    Hint 1: Think of this as a sliding window — the last k messages stay
        untouched as "remaining", and everything older than that gets
        collapsed into one summary sentence.
    Hint 2: Use negative slicing: messages[:-k] for the evicted (older)
        turns and messages[-k:] for the remaining (recent) ones, then join
        the evicted list with "; " inside the summary string.
    Hint 3: The summary wording is exact and checked by string equality —
        "Summary of {N} earlier turns: " followed by the evicted messages
        joined with "; " (semicolon-space) — so match the count, phrasing,
        and punctuation precisely, not just the general idea.
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
