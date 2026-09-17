"""Problem 01 — Multi Head Attention Mask

Topic: 06 Transformers
Target: Production-grade implementation

Apply causal autoregressive upper triangular mask to attention scores.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def multi_head_attention_mask(scores: list[list[float]], neg_inf: float = -1e9) -> list[list[float]]:
    """Mask positions where j > i with neg_inf.
    scores is square N x N matrix.
    Returns masked matrix.
    """
    raise NotImplementedError("Implement multi_head_attention_mask")
