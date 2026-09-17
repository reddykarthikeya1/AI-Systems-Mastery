"""Beginner playground for Module 07 - Automated Red Teaming & Fuzzing.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import random

# -------------------------------------------- 1. Adversarial Prompt Mutation Strategies
def leetspeak_mutate(text):
    mapping = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
    return "".join(mapping.get(ch.lower(), ch) for ch in text)

original = "password"
mutated = leetspeak_mutate(original)

assert mutated == "p@$$w0rd"
assert len(mutated) == len(original)
print(f"Mutated adversarial fuzzing candidate: '{original}' -> '{mutated}'")

# -------------------------------------------- 2. Attack Success Rate (ASR) Metric
total_attacks = 100
successful_breaches = 8
asr = successful_breaches / total_attacks

assert asr == 0.08
assert asr < 0.10, "ASR maintained below 10% tolerance"
print(f"Red teaming Attack Success Rate: {asr:.1%} ({successful_breaches}/{total_attacks})")

# -------------------------------------------- 3. Safety Boundary Exploration Loop
perturbation_levels = [0.1, 0.2, 0.3, 0.4]
assert len(perturbation_levels) == 4
assert perturbation_levels[-1] > perturbation_levels[0]
print("Multi-level fuzzing matrix generated.")

print()
print("All checks passed.")
