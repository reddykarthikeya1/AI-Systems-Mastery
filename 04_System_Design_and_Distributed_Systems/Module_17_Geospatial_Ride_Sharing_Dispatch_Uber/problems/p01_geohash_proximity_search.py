"""Problem 01 — Geohash Proximity Search

Topic: 17 Geospatial Ride Sharing Dispatch Uber
Target: Production-grade implementation

Find drivers sharing geohash spatial prefix with passenger location.

Example:
    >>> geohash_proximity_search('9q8yy0', {'d1': '9q8yy1', 'd2': '9q8yy9', 'd3': '9q8zaa', 'd4': '8k1111'}, 5)
    ['d1', 'd2']

Hints:
    Hint 1: A geohash string is a coarse spatial index -- two locations
        sharing a longer common prefix are physically closer, so
        "nearby" reduces to a plain string prefix check.
    Hint 2: Slice the passenger's geohash down to `prefix_len`, then
        filter driver_id/geohash pairs whose geohash starts with that
        prefix, sorting the surviving ids before returning.
    Hint 3: Only the PASSENGER's geohash gets truncated to `prefix_len`
        before comparing -- a driver geohash shorter than `prefix_len`
        must simply fail the `startswith` check rather than crash or
        false-positive; results must come back sorted by driver_id, not
        left in dict insertion order.
"""

from __future__ import annotations


def geohash_proximity_search(passenger_geohash: str, drivers: dict[str, str], prefix_len: int = 4) -> list[str]:
    """drivers maps driver_id -> driver_geohash.
    Return driver_ids whose geohash starts with passenger_geohash[:prefix_len], sorted by driver_id.
    """
    raise NotImplementedError("Implement geohash_proximity_search")
