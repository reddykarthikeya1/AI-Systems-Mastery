"""Reference Solution — Problem 01: Tensor Broadcast Strides

Topic: 03 PyTorch Fundamentals
"""

from __future__ import annotations


def tensor_broadcast_strides(shape_a: list[int], shape_b: list[int]) -> list[int]:
    out = []
    ra = list(reversed(shape_a))
    rb = list(reversed(shape_b))
    n = max(len(ra), len(rb))
    for i in range(n):
        da = ra[i] if i < len(ra) else 1
        db = rb[i] if i < len(rb) else 1
        if da == db:
            out.append(da)
        elif da == 1:
            out.append(db)
        elif db == 1:
            out.append(da)
        else:
            raise ValueError("Incompatible broadcast shapes")
    return list(reversed(out))
