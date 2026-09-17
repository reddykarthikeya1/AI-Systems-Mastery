"""Problem 01 — Lora Weight Merge

Topic: 10 How to FineTune Models
Target: Production-grade implementation

Merge low-rank adapter delta into base weight: W_merged = W_base + (alpha / r) * (B x A).

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def lora_weight_merge(W_base: list[list[float]], B: list[list[float]], A: list[list[float]], alpha: float = 16.0, r: int = 4) -> list[list[float]]:
    """B is (d_out x r), A is (r x d_in).
    Returns W_merged = W_base + (alpha / r) * (B @ A) rounded to 4 decimals.
    """
    raise NotImplementedError("Implement lora_weight_merge")
