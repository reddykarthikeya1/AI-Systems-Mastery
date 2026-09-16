#!/usr/bin/env python3
"""Broken Two-Tier Cache demonstrating wall-clock TTL and cached None traps."""

import time

class BrokenCache:
    def __init__(self):
        self._cache = {}

    def set(self, key: str, value: object, ttl_seconds: float):
        # Subject to NTP clock adjustments, daylight saving jumps, or system clock changes.
        expires_at = time.time() + ttl_seconds
        self._cache[key] = (value, expires_at)

    def get(self, key: str) -> object:
        if key not in self._cache:
            return None
        val, expires_at = self._cache[key]
        if time.time() > expires_at:
            del self._cache[key]
            return None
        # between a cache hit of None and a cache miss!
        return val

if __name__ == "__main__":
    cache = BrokenCache()
    cache.set("user_404", None, 60.0)
    res = cache.get("user_404")
    print(f"Cached None lookup: {res} (Indistinguishable from cache miss!)")
