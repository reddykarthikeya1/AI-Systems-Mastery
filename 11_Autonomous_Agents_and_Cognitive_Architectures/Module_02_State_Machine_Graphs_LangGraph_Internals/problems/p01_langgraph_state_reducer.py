"""Problem 01 — Langgraph State Reducer

Topic: 02 State Machine Graphs LangGraph Internals
Target: Production-grade implementation

Execute state reducer across edge transitions with message append rules.

Example:
    >>> langgraph_state_reducer({'messages': ['hi'], 'count': 1}, {'messages': ['there'], 'count': 2})
    {'messages': ['hi', 'there'], 'count': 2}

Hints:
    Hint 1: 'messages' is special-cased — it's the one key where the patch
        should extend history rather than overwrite it; every other key
        behaves like a normal dict update.
    Hint 2: Copy current_state, then loop over incoming_patch.items(): when
        the key is 'messages' and the existing value is a list, concatenate
        the two lists; otherwise just assign the incoming value.
    Hint 3: Only append when the existing 'messages' value (and the
        incoming patch value) are actually lists — if 'messages' hasn't
        been initialized as a list yet, the patch must overwrite/set it
        instead of trying to append to something that isn't a list.
"""

from __future__ import annotations


def langgraph_state_reducer(current_state: dict, incoming_patch: dict) -> dict:
    """State reducer:
    - If key in incoming_patch is 'messages' and existing value is list: append new messages.
    - For any other key: overwrite with incoming_patch[k].
    Returns updated state copy.
    """
    raise NotImplementedError("Implement langgraph_state_reducer")
