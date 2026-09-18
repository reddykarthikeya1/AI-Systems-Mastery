"""Problem 01 — Memoization Closure with TTL

Target: Production-grade implementation
"""

from __future__ import annotations


import time
from functools import wraps

def memoize_with_ttl(ttl_seconds: float = 60.0):
    def decorator(fn):
        cache = {}
        stats = {'hits': 0, 'misses': 0}
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in cache:
                val, ts = cache[key]
                if now - ts < ttl_seconds:
                    stats['hits'] += 1
                    return val
            stats['misses'] += 1
            res = fn(*args, **kwargs)
            cache[key] = (res, now)
            return res
        wrapper.stats = stats
        return wrapper
    return decorator
