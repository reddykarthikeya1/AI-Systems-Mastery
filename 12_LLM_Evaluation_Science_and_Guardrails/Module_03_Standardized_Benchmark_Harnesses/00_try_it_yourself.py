"""Beginner playground for Module 03 - Standardized Benchmark Harnesses.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Few-Shot Prompt Construction
exemplars = [
    {"q": "What is 2+2?", "a": "4"},
    {"q": "What is 3+5?", "a": "8"}
]
test_q = "What is 7+4?"
prompt = ""
for ex in exemplars:
    prompt += f"Q: {ex['q']}\nA: {ex['a']}\n\n"
prompt += f"Q: {test_q}\nA:"

assert "2+2" in prompt
assert "7+4" in prompt
assert prompt.endswith("A:")
print(f"Standard 2-shot benchmark prompt assembled:\n{prompt}")

# -------------------------------------------- 2. Multiple-Choice Log-Likelihood Evaluation
log_probs = {"A": -1.2, "B": -0.3, "C": -2.5, "D": -3.1}
best_choice = max(log_probs, key=log_probs.get)

assert best_choice == "B"
assert log_probs[best_choice] == -0.3
print(f"Highest probability choice selected: Option {best_choice}")

# -------------------------------------------- 3. Pass@K Metric Math (HumanEval)
n = 10  # 10 samples generated
c = 3   # 3 correct samples
# Pass@1 = c / n
pass_at_1 = c / n
assert pass_at_1 == 0.30
print(f"HumanEval Pass@1: {pass_at_1:.1%}")

print()
print("All checks passed.")
