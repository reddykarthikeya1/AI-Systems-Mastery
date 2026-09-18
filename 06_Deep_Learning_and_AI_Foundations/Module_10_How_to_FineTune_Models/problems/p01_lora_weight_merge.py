"""Problem 01 — Lora Weight Merge

Topic: 10 How to FineTune Models
Target: Production-grade implementation

Merge low-rank adapter delta into base weight: W_merged = W_base + (alpha / r) * (B x A).

Example:
    >>> lora_weight_merge([[1.0, 0.0], [0.0, 1.0]], [[1.0], [0.0]], [[0.5, 0.5]], alpha=4.0, r=1)
    [[3.0, 2.0], [0.0, 1.0]]

Hints:
    Hint 1: LoRA never multiplies two full d_out x d_in matrices together —
        the adapter's whole point is that B @ A stays low-rank (rank r),
        which is what makes it cheap, and it is only ADDED on top of the
        frozen base weight.
    Hint 2: Compute the matrix product `B @ A` (B is d_out x r, A is r x
        d_in, so entry (i, j) sums over the r shared dimension), scale the
        result by `alpha / r`, then add it elementwise to `W_base`.
    Hint 3: The inner product's contraction dimension is `r`, not
        `len(B[i])` or some other length — use the `r` parameter directly
        as the loop bound for the sum over k, since that's the rank of the
        adapter regardless of how B/A happen to be shaped. Round every
        merged entry to 4 decimal places.
"""

from __future__ import annotations


def lora_weight_merge(W_base: list[list[float]], B: list[list[float]], A: list[list[float]], alpha: float = 16.0, r: int = 4) -> list[list[float]]:
    """B is (d_out x r), A is (r x d_in).
    Returns W_merged = W_base + (alpha / r) * (B @ A) rounded to 4 decimals.
    """
    raise NotImplementedError("Implement lora_weight_merge")
