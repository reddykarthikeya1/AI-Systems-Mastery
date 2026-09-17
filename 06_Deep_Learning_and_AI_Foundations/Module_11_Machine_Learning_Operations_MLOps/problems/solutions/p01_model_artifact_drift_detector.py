"""Reference Solution — Problem 01: Model Artifact Drift Detector

Topic: 11 Machine Learning Operations MLOps
"""

from __future__ import annotations


def model_artifact_drift_detector(baseline_counts: list[int], current_counts: list[int]) -> float:
    import math
    b_total = sum(baseline_counts)
    c_total = sum(current_counts)
    eps = 1e-6
    psi = 0.0
    for b_c, c_c in zip(baseline_counts, current_counts):
        b_pct = (b_c / b_total) if b_total > 0 else eps
        c_pct = (c_c / c_total) if c_total > 0 else eps
        b_pct = max(b_pct, eps)
        c_pct = max(c_pct, eps)
        psi += (c_pct - b_pct) * math.log(c_pct / b_pct)
    return round(psi, 4)
