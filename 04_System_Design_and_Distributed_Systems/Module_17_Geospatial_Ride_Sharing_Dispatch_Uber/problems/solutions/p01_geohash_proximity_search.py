"""Reference Solution — Problem 01: Geohash Proximity Search

Topic: 17 Geospatial Ride Sharing Dispatch Uber
"""

from __future__ import annotations


def geohash_proximity_search(passenger_geohash: str, drivers: dict[str, str], prefix_len: int = 4) -> list[str]:
    pref = passenger_geohash[:prefix_len]
    return sorted(d for d, gh in drivers.items() if gh.startswith(pref))
