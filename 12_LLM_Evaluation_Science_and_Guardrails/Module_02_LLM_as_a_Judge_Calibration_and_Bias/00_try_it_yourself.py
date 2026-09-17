"""Beginner playground for Module 02 - LLM as a Judge Calibration & Bias.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Position Bias Detection via Order Swapping
# Swap inputs: score(A, B) vs score(B, A)
trial1_winner = "Candidate A"  # Model 1 was in position A
trial2_winner = "Candidate A"  # Model 2 was in position A

position_bias_detected = (trial1_winner == "Candidate A" and trial2_winner == "Candidate A")
assert position_bias_detected is True, "Judge always votes for position A regardless of content"
print("Position bias confirmed: order swapping detected primacy effect.")

# -------------------------------------------- 2. Verbosity Bias Length Normalization
raw_score = 9.0
word_count = 600
target_length = 200

length_penalty = max(0.0, (word_count - target_length) * 0.005)
calibrated_score = raw_score - length_penalty

assert length_penalty == 2.0
assert calibrated_score == 7.0
print(f"Calibrated score: {calibrated_score} (down from raw {raw_score} after length penalty)")

# -------------------------------------------- 3. Cohen's Kappa Inter-Rater Agreement
p_observed = 0.85
p_chance = 0.50
kappa = (p_observed - p_chance) / (1.0 - p_chance)

assert kappa == 0.70
assert kappa > 0.60, "Substantial agreement"
print(f"Inter-rater agreement Cohen's Kappa: {kappa:.2f}")

print()
print("All checks passed.")
