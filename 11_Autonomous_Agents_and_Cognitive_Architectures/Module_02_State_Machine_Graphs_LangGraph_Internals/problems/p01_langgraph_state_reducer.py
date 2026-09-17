"""Problem 01 — Langgraph State Reducer

Topic: 02 State Machine Graphs LangGraph Internals
Target: Production-grade implementation

Execute state reducer across edge transitions with message append rules.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def langgraph_state_reducer(current_state: dict, incoming_patch: dict) -> dict:
    """State reducer:
    - If key in incoming_patch is 'messages' and existing value is list: append new messages.
    - For any other key: overwrite with incoming_patch[k].
    Returns updated state copy.
    """
    raise NotImplementedError("Implement langgraph_state_reducer")
