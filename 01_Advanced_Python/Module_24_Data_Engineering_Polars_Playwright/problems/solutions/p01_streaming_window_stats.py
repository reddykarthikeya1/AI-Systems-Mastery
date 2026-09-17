"""Problem 01 — Single-Pass Rolling Mean & Max

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def rolling_window_stats(stream: list[float], window_size: int) -> list[tuple[float, float]]:
    if not stream or window_size <= 0 or len(stream) < window_size:
        return []
    res = []
    window = stream[:window_size]
    wsum = sum(window)
    res.append((round(wsum / window_size, 3), max(window)))
    for i in range(window_size, len(stream)):
        wsum += stream[i] - stream[i - window_size]
        window = stream[i - window_size + 1:i + 1]
        res.append((round(wsum / window_size, 3), max(window)))
    return res
