"""Beginner playground for Module 10 - Reasoning Under Uncertainty.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Sample Space and Probability Axioms
sample_space = {"heads": 0.5, "tails": 0.5}
assert sum(sample_space.values()) == 1.0
assert all(0.0 <= p <= 1.0 for p in sample_space.values())
print(f"Valid probability distribution over {list(sample_space.keys())}")

# -------------------------------------------- 2. Conditional Probability and Bayes' Theorem
p_disease = 0.01          # Prior P(D)
p_pos_given_disease = 0.95 # Sensitivity P(+|D)
p_pos_given_healthy = 0.05 # False positive rate P(+|H)

p_healthy = 1.0 - p_disease
p_pos = p_pos_given_disease * p_disease + p_pos_given_healthy * p_healthy
p_disease_given_pos = (p_pos_given_disease * p_disease) / p_pos

assert 0.15 < p_disease_given_pos < 0.20
assert p_disease_given_pos > p_disease, "Posterior must exceed prior on positive test"
print(f"Prior: {p_disease:.1%}, Posterior given positive test: {p_disease_given_pos:.1%}")

# -------------------------------------------- 3. Independence of Random Variables
p_a = 0.4
p_b = 0.5
p_a_and_b = 0.2

is_independent = abs(p_a_and_b - (p_a * p_b)) < 1e-6
assert is_independent is True
assert (p_a * p_b) == 0.2
print(f"Events A and B are independent: P(A)*P(B) = {p_a * p_b} == P(A and B) = {p_a_and_b}")

print()
print("All checks passed.")
