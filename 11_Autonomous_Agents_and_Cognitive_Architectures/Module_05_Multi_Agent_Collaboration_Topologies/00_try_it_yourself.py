"""Beginner playground for Module 05 - Multi-Agent Collaboration Topologies.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Supervisor Router Delegation
def supervisor_route(task):
    if "code" in task.lower() or "bug" in task.lower():
        return "coder_agent"
    elif "search" in task.lower() or "who" in task.lower():
        return "researcher_agent"
    return "general_agent"

assert supervisor_route("Fix the bug in main.py") == "coder_agent"
assert supervisor_route("Who won the 2024 Nobel prize?") == "researcher_agent"
print("Supervisor successfully routed specialized tasks to domain agents.")

# -------------------------------------------- 2. Majority Vote Consensus Protocol
from collections import Counter
votes = ["approve", "approve", "reject"]
counts = Counter(votes)
winner, win_count = counts.most_common(1)[0]

assert winner == "approve"
assert win_count == 2
print(f"Consensus achieved: '{winner}' with {win_count}/3 votes.")

# -------------------------------------------- 3. Hand-Off Protocol Context Forwarding
hand_off = {"from": "researcher", "to": "writer", "summary": "Found 3 key sources."}
assert hand_off["to"] == "writer"
assert len(hand_off["summary"]) > 0
print(f"Hand-off verified from {hand_off['from']} to {hand_off['to']}.")

print()
print("All checks passed.")
