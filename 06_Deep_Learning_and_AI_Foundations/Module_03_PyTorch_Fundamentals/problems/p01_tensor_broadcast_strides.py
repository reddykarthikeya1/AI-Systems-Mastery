"""Problem 01 — Tensor Broadcast Strides

Topic: 03 PyTorch Fundamentals
Target: Production-grade implementation

Compute broadcasted output shape and strides for two tensor shapes.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def tensor_broadcast_strides(shape_a: list[int], shape_b: list[int]) -> list[int]:
    """Align shapes from the right and return broadcasted output shape.
    If dimensions are incompatible (neither equal nor 1), raise ValueError("Incompatible broadcast shapes").
    """
    raise NotImplementedError("Implement tensor_broadcast_strides")
