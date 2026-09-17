"""Reference Solution — Problem 01: Speculative Rejection Sampler

Topic: 07 Speculative Decoding Architectures
"""

from __future__ import annotations


def speculative_rejection_sampler(draft_probs: list[float], target_probs: list[float], rand_draws: list[float]) -> int:
    accepted = 0
    for dp, tp, r in zip(draft_probs, target_probs, rand_draws):
        ratio = min(1.0, (tp / dp) if dp > 0 else 1.0)
        if r <= ratio:
            accepted += 1
        else:
            break
    return accepted
