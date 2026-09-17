"""Reference Solution — Problem 01: Evaluate Window Frame

Topic: 02 Modern SQL Mastery Advanced Queries
"""

from __future__ import annotations


def evaluate_window_frame(values: list[float]) -> list[float]:
    res = []
    for i in range(len(values)):
        prev = values[i-1] if i > 0 else 0.0
        res.append(prev + values[i])
    return res
