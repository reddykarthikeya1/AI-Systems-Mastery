"""Reference Solution — Problem 01: Adaptive Bitrate Manifest

Topic: 18 Video Ingestion Streaming YouTube Netflix
"""

from __future__ import annotations


def adaptive_bitrate_manifest(total_duration_sec: float, segment_target_sec: float = 6.0) -> list[tuple[int, float]]:
    if total_duration_sec <= 0:
        return []
    res = []
    rem = total_duration_sec
    idx = 0
    while rem > 0.001:
        dur = min(rem, segment_target_sec)
        res.append((idx, round(dur, 2)))
        rem -= dur
        idx += 1
    return res
