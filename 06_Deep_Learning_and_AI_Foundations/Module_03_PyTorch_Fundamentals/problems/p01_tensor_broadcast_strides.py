"""Problem 01 — Tensor Broadcast Strides

Topic: 03 PyTorch Fundamentals
Target: Production-grade implementation

Compute broadcasted output shape and strides for two tensor shapes.

Example:
    >>> tensor_broadcast_strides([8, 1, 64], [7, 64])
    [8, 7, 64]

Hints:
    Hint 1: Broadcasting compares shapes dimension-by-dimension starting
        from the TRAILING (rightmost) axis, so shapes of different lengths
        still line up correctly by their last dimensions.
    Hint 2: Reverse both shape lists, pad the shorter one out with implicit
        1s wherever it runs out of dimensions, then for each aligned pair
        take whichever of the two sizes is not 1 (or the shared size if
        they're equal) — then reverse the result back to normal order.
    Hint 3: Two dimensions are only compatible if they're equal or one of
        them is exactly 1 — anything else (like `[5]` vs `[4]`) must raise
        `ValueError("Incompatible broadcast shapes")` rather than silently
        picking one.
"""

from __future__ import annotations


def tensor_broadcast_strides(shape_a: list[int], shape_b: list[int]) -> list[int]:
    """Align shapes from the right and return broadcasted output shape.
    If dimensions are incompatible (neither equal nor 1), raise ValueError("Incompatible broadcast shapes").
    """
    raise NotImplementedError("Implement tensor_broadcast_strides")
