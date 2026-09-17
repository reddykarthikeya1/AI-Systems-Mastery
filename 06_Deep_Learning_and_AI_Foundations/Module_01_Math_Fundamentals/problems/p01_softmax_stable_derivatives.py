"""Problem 01 — Softmax Stable Derivatives

Topic: 01 Math Fundamentals
Target: Production-grade implementation

Compute numerically stable softmax probabilities using max subtraction.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def softmax_stable_derivatives(logits: list[float]) -> list[float]:
    """Compute softmax with max subtraction:
    p_i = exp(z_i - max(z)) / sum(exp(z_j - max(z)))
    Returns list of probabilities rounded to 4 decimals.
    """
    raise NotImplementedError("Implement softmax_stable_derivatives")
