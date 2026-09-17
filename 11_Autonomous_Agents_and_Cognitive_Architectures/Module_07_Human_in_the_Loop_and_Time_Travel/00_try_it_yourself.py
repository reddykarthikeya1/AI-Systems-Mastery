"""Beginner playground for Module 07 - Human-in-the-Loop & Time Travel.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import json

# -------------------------------------------- 1. Approval Interrupt Gate
def requires_human_approval(action_type):
    critical_actions = {"transfer_money", "delete_record", "deploy_production"}
    return action_type in critical_actions

assert requires_human_approval("transfer_money") is True
assert requires_human_approval("search_database") is False
print("Approval gate correctly categorized sensitive actions.")

# -------------------------------------------- 2. Approval / Rejection State Fork
state = {"action": "delete_table", "status": "pending_approval"}
human_approved = False

if not human_approved:
    state["status"] = "rejected"
    state["feedback"] = "User disallowed table deletion. Archive instead."

assert state["status"] == "rejected"
assert "Archive instead" in state["feedback"]
print(f"Handled human feedback: {state['feedback']}")

# -------------------------------------------- 3. Time Travel State Rewind
history = ["state_0", "state_1_bad", "state_2_crashed"]
rewound_state = history[0]
assert rewound_state == "state_0"
print(f"Time travel rewound state back to: {rewound_state}")

print()
print("All checks passed.")
