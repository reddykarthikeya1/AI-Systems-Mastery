"""Problem 01 — Adaptive Bitrate Manifest

Topic: 18 Video Ingestion Streaming YouTube Netflix
Target: Production-grade implementation

Generate HLS media playlist segment durations and chunk byte ranges.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def adaptive_bitrate_manifest(total_duration_sec: float, segment_target_sec: float = 6.0) -> list[tuple[int, float]]:
    """Slice video into segments: each segment has index (0-based) and duration.
    All segments except possibly the last have duration = segment_target_sec.
    The last segment has remaining duration rounded to 2 decimals.
    Returns list of (segment_index, duration).
    """
    raise NotImplementedError("Implement adaptive_bitrate_manifest")
