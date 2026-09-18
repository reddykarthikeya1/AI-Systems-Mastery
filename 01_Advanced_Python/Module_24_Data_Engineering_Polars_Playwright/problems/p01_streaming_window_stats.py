"""Problem 01 — Single-Pass Rolling Mean & Max

Target: Production-grade implementation

Example:
    >>> rolling_window_stats([1.0, 2.0, 3.0, 4.0], 2)
    [(1.5, 2.0), (2.5, 3.0), (3.5, 4.0)]
    >>> rolling_window_stats([], 2)
    []

Hints:
    Hint 1: Recomputing the sum (or scanning for the max) from scratch for
        every window position is wasteful — as the window slides by one
        element, most of the work from the previous position can be reused.
    Hint 2: Maintain a running sum incrementally (add the incoming element,
        subtract the one that just fell out of the window) for the mean, and
        re-derive `max()` over the current window slice for each position.
    Hint 3: There's one tuple of `(mean, max)` per valid window position —
        `len(stream) - window_size + 1` of them — so a `window_size` larger
        than the stream (or `<= 0`, or an empty stream) must return `[]`
        rather than a partial or malformed window; the mean is rounded to 3
        decimal places.
"""

from __future__ import annotations


def rolling_window_stats(stream: list[float], window_size: int) -> list[tuple[float, float]]:
    raise NotImplementedError('Implement rolling_window_stats')
