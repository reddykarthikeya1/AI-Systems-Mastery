"""Reference Solution — Problem 01: compute_matrix_metric

Topic: Linear Systems and Geometric Maps
"""

from __future__ import annotations

import numpy as np

def compute_matrix_metric(matrix: list[list[float]]) -> dict[str, float]:
    arr = np.array(matrix, dtype=float)
    if arr.size == 0 or arr.ndim != 2:
        return {"trace": 0.0, "frobenius_norm": 0.0}
    trace_val = float(np.trace(arr)) if arr.shape[0] == arr.shape[1] else 0.0
    frob_val = float(np.linalg.norm(arr, 'fro'))
    return {"trace": round(trace_val, 4), "frobenius_norm": round(frob_val, 4)}

