"""Reference solution — Problem 01: Classify Empirical Growth Rate

Pattern:    Complexity analysis
Complexity: Time O(k), Space O(k) for k measurements
"""

from __future__ import annotations


def classify_growth(timings: list[tuple[int, float]]) -> str:
    if len(timings) < 2:
        return "O(1)"

    ratios = []
    for (_, t_prev), (_, t_next) in zip(timings, timings[1:]):
        if t_prev <= 0:
            continue
        ratios.append(t_next / t_prev)

    if not ratios:
        return "O(1)"

    mean = sum(ratios) / len(ratios)

    # Boundaries sit at the midpoints between the ideal ratios 1, 2 and 4, so a
    # noisy measurement has to be badly wrong to change the classification.
    if mean < 1.5:
        return "O(1)"
    if mean < 3.0:
        return "O(n)"
    return "O(n^2)"
