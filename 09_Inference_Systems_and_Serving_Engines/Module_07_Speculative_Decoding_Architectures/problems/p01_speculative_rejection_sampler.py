"""Problem 01 — Speculative Rejection Sampler

Topic: 07 Speculative Decoding Architectures
Target: Production-grade implementation

Determine accepted draft tokens comparing target model and draft model probabilities.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def speculative_rejection_sampler(draft_probs: list[float], target_probs: list[float], rand_draws: list[float]) -> int:
    """Evaluate accepted draft tokens in sequence:
    Accept token i if rand_draws[i] <= min(1.0, target_probs[i] / draft_probs[i]).
    First rejected token halts evaluation.
    Returns count of accepted tokens.
    """
    raise NotImplementedError("Implement speculative_rejection_sampler")
