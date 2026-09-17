"""Reference Solution — Problem 01: Multi Head Attention Mask

Topic: 06 Transformers
"""

from __future__ import annotations


def multi_head_attention_mask(scores: list[list[float]], neg_inf: float = -1e9) -> list[list[float]]:
    n = len(scores)
    res = []
    for i in range(n):
        row = []
        for j in range(n):
            if j > i:
                row.append(neg_inf)
            else:
                row.append(scores[i][j])
        res.append(row)
    return res
