"""Problem 01 — Geohash Proximity Search

Topic: 17 Geospatial Ride Sharing Dispatch Uber
Target: Production-grade implementation

Find drivers sharing geohash spatial prefix with passenger location.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def geohash_proximity_search(passenger_geohash: str, drivers: dict[str, str], prefix_len: int = 4) -> list[str]:
    """drivers maps driver_id -> driver_geohash.
    Return driver_ids whose geohash starts with passenger_geohash[:prefix_len], sorted by driver_id.
    """
    raise NotImplementedError("Implement geohash_proximity_search")
