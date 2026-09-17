"""Reference Solution — Problem 01: Bootstrap Confidence Interval

Topic: 12 Statistical Estimation from Samples
"""

from __future__ import annotations


def bootstrap_confidence_interval(estimates: list[float], alpha: float = 0.05) -> tuple[float, float]:
    s = sorted(estimates)
    n = len(s)
    low_idx = int((alpha / 2.0) * n)
    high_idx = int((1.0 - alpha / 2.0) * n) - 1
    high_idx = max(0, min(high_idx, n - 1))
    return (round(s[low_idx], 4), round(s[high_idx], 4))
