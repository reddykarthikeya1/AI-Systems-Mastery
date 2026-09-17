"""Reference Solution — Problem 01: Langgraph State Reducer

Topic: 02 State Machine Graphs LangGraph Internals
"""

from __future__ import annotations


def langgraph_state_reducer(current_state: dict, incoming_patch: dict) -> dict:
    new_state = dict(current_state)
    for k, v in incoming_patch.items():
        if k == 'messages' and isinstance(new_state.get(k), list) and isinstance(v, list):
            new_state[k] = new_state[k] + v
        else:
            new_state[k] = v
    return new_state
