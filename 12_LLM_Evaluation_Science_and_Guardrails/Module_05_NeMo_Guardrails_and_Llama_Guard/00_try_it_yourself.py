"""Beginner playground for Module 05 - NeMo Guardrails & Llama Guard.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import json

# -------------------------------------------- 1. Safety Category Classification
categories = {
    "S1": "Violent Crimes",
    "S2": "Non-Violent Crimes",
    "S3": "Sex-Related Crimes",
    "S4": "Child Exploitation",
    "S5": "Defamation"
}
assert len(categories) == 5
assert categories["S1"] == "Violent Crimes"
print(f"Safety taxonomy mapped {len(categories)} hazard categories.")

# -------------------------------------------- 2. Colang Flow Control Simulation
def colang_guard(user_intent):
    if user_intent == "ask_about_competitor":
        return "I can only discuss our company's product features."
    return "proceed"

action = colang_guard("ask_about_competitor")
assert action.startswith("I can only discuss")
assert colang_guard("ask_pricing") == "proceed"
print(f"Colang flow redirected off-topic intent: '{action}'")

# -------------------------------------------- 3. Binary Safe/Unsafe Classification Parsing
classifier_output = "unsafe\nS2"
lines = classifier_output.split("\n")
is_safe = lines[0].strip() == "safe"
violated_category = lines[1].strip() if not is_safe else None

assert is_safe is False
assert violated_category == "S2"
print(f"Moderation verdict: safe={is_safe}, violation={violated_category}")

print()
print("All checks passed.")
