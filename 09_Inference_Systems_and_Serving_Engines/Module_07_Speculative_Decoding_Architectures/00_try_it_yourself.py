"""Beginner playground for Module 07 - Speculative Decoding Architectures.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Draft Model Proposal and Target Verification
K = 4
draft_tokens = ["in", "the", "middle", "of"]
target_agreements = [True, True, True, False]  # Agrees on first 3, rejects 4th

accepted_tokens = []
for token, agreed in zip(draft_tokens, target_agreements):
    if agreed:
        accepted_tokens.append(token)
    else:
        break

assert len(accepted_tokens) == 3
assert accepted_tokens == ["in", "the", "middle"]
print(f"Speculative decode accepted {len(accepted_tokens)} of {K} tokens in a single target forward pass.")

# -------------------------------------------- 2. Speedup Factor under Acceptance Rate Alpha
alpha = 0.80  # 80% acceptance rate
expected_tokens_per_step = 1.0 + (K * alpha)

assert expected_tokens_per_step == 4.2
print(f"Expected generated tokens per large model step: {expected_tokens_per_step:.1f} tokens.")

# -------------------------------------------- 3. Exact Output Distribution Invariance
p_target = 0.60
p_draft = 0.40
accept_prob = min(1.0, p_target / p_draft)

assert accept_prob == 1.0
assert min(1.0, 0.20 / 0.40) == 0.50
print(f"Speculative acceptance probability calculated: {accept_prob:.2f}")

print()
print("All checks passed.")
