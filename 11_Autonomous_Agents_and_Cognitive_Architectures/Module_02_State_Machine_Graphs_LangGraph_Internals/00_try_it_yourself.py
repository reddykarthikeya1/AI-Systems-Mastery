"""Beginner playground for Module 02 - State Machine Graphs (LangGraph Internals).

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import copy

# -------------------------------------------- 1. State Dictionary Transition Invariant
state = {"query": "Find books", "results": [], "step": 0}

def search_node(s):
    return {"results": ["Book A", "Book B"], "step": s["step"] + 1}

updates = search_node(state)
new_state = {**state, **updates}

assert new_state["step"] == 1
assert len(new_state["results"]) == 2
assert new_state["query"] == "Find books"
print(f"State transition successful: {new_state}")

# -------------------------------------------- 2. Conditional Routing Edges
def route_next(s):
    if len(s["results"]) > 0:
        return "summarize"
    return "retry_search"

next_node = route_next(new_state)
assert next_node == "summarize"
assert route_next({"results": []}) == "retry_search"
print(f"Conditional edge routed to '{next_node}' based on search results.")

# -------------------------------------------- 3. Cycle and Checkpoint Snapshots
checkpoints = []
checkpoints.append(copy.deepcopy(state))
checkpoints.append(copy.deepcopy(new_state))

assert len(checkpoints) == 2
assert checkpoints[0]["step"] == 0
assert checkpoints[1]["step"] == 1
print("Checkpoint history captured across state transitions.")

print()
print("All checks passed.")
