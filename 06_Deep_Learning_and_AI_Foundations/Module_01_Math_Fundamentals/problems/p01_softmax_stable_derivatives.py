"""Problem 01 — Softmax Stable Derivatives

Topic: 01 Math Fundamentals
Target: Production-grade implementation

Compute numerically stable softmax probabilities using max subtraction.

Example:
    >>> softmax_stable_derivatives([1000.0, 1001.0, 1002.0])
    [0.09, 0.2447, 0.6652]

Hints:
    Hint 1: Softmax only depends on the DIFFERENCES between logits, so
        shifting every logit by the same constant before exponentiating
        leaves the final probabilities unchanged.
    Hint 2: Subtract `max(logits)` from every entry before calling `exp`,
        then divide each `exp(z_i - max)` by the sum of all of them.
    Hint 3: Without the max-subtraction shift, `exp(1000.0)` overflows to
        `inf` (as this test's inputs would trigger) — with it, the largest
        shifted value is always exactly 0, keeping every `exp` call in a
        safe range. Round each output probability to 4 decimals, and return
        `[]` for empty input.
"""

from __future__ import annotations


def softmax_stable_derivatives(logits: list[float]) -> list[float]:
    """Compute softmax with max subtraction:
    p_i = exp(z_i - max(z)) / sum(exp(z_j - max(z)))
    Returns list of probabilities rounded to 4 decimals.
    """
    raise NotImplementedError("Implement softmax_stable_derivatives")
