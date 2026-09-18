"""Problem 01 — Evaluate Window Frame

Topic: 02 Modern SQL Mastery Advanced Queries
Target: Production-grade implementation

Compute moving sum over ROWS BETWEEN 1 PRECEDING AND CURRENT ROW.

Example:
    >>> evaluate_window_frame([10.0, 20.0, 30.0, 40.0])
    [10.0, 30.0, 50.0, 70.0]

Hints:
    Hint 1: Each output row only ever looks at itself and the one row
        directly above it, so this is a purely local computation with no
        need to hold the whole window frame in memory at once.
    Hint 2: A single pass with a running "previous value" variable (or
        indexing values[i-1]) is enough — no separate window buffer or
        prefix-sum array is required.
    Hint 3: The very first row has no preceding row, so its frame sum is
        just itself (treat the missing predecessor as 0.0); an empty input
        list must return an empty list rather than raising.
"""

from __future__ import annotations


def evaluate_window_frame(values: list[float]) -> list[float]:
    """Compute moving sum for each index over ROWS BETWEEN 1 PRECEDING AND CURRENT ROW."""
    raise NotImplementedError("Implement evaluate_window_frame")
