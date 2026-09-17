"""Problem 01 — Rotary Position Embedding

Topic: 08 LLM From Scratch
Target: Production-grade implementation

Apply 2D rotary embedding (RoPE) rotation to vector pair (x0, x1) at token position m with frequency theta.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def rotary_position_embedding(x0: float, x1: float, m: int, theta: float = 10000.0) -> tuple[float, float]:
    """Angle phi = m / (theta ** 0) = m.
    Rotate:
    x0_rot = x0 * cos(phi) - x1 * sin(phi)
    x1_rot = x0 * sin(phi) + x1 * cos(phi)
    Returns (x0_rot, x1_rot) rounded to 4 decimals.
    """
    raise NotImplementedError("Implement rotary_position_embedding")
