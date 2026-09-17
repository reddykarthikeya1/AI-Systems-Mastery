"""Reference Solution — Problem 01: Lora Weight Merge

Topic: 10 How to FineTune Models
"""

from __future__ import annotations


def lora_weight_merge(W_base: list[list[float]], B: list[list[float]], A: list[list[float]], alpha: float = 16.0, r: int = 4) -> list[list[float]]:
    d_out = len(B)
    d_in = len(A[0])
    scale = alpha / float(r)
    merged = []
    for i in range(d_out):
        row = []
        for j in range(d_in):
            delta = sum(B[i][k] * A[k][j] for k in range(r))
            row.append(round(W_base[i][j] + scale * delta, 4))
        merged.append(row)
    return merged
