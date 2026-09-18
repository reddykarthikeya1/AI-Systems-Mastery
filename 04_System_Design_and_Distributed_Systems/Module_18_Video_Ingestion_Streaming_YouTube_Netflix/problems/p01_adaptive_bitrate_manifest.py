"""Problem 01 — Adaptive Bitrate Manifest

Topic: 18 Video Ingestion Streaming YouTube Netflix
Target: Production-grade implementation

Generate HLS media playlist segment durations and chunk byte ranges.

Example:
    >>> adaptive_bitrate_manifest(15.0, 6.0)
    [(0, 6.0), (1, 6.0), (2, 3.0)]

Hints:
    Hint 1: This is repeated subtraction -- keep carving fixed-size
        chunks off the remaining duration until less than a full chunk is
        left over.
    Hint 2: Use a while loop tracking the remaining duration and a
        segment index counter, appending
        `(index, min(remaining, segment_target_sec))` on each iteration.
    Hint 3: A `total_duration_sec` of 0 (or negative) must return an empty
        list rather than looping forever; end the loop on a small epsilon
        (e.g. `remaining > 0.001`) instead of `> 0`, so floating-point
        residue doesn't produce one extra near-zero segment, and round
        each segment's duration to 2 decimals.
"""

from __future__ import annotations


def adaptive_bitrate_manifest(total_duration_sec: float, segment_target_sec: float = 6.0) -> list[tuple[int, float]]:
    """Slice video into segments: each segment has index (0-based) and duration.
    All segments except possibly the last have duration = segment_target_sec.
    The last segment has remaining duration rounded to 2 decimals.
    Returns list of (segment_index, duration).
    """
    raise NotImplementedError("Implement adaptive_bitrate_manifest")
