"""Problem 01 — Token Bucket Rate Limiter

Target: Production-grade implementation

Example:
    >>> b = TokenBucket(2.0, 1.0)
    >>> b.allow(0.0)
    True
    >>> b.allow(0.0)
    True
    >>> b.allow(0.0)
    False
    >>> b.allow(1.0)
    True

Hints:
    Hint 1: Tokens aren't decremented on a timer — they are refilled lazily,
        computed from how much wall-clock time has passed since the bucket
        was last touched.
    Hint 2: Track `tokens` and `last_time` as instance state; on each `allow`
        call, add `elapsed * fill_rate` to `tokens` (capped at `capacity`)
        before checking whether enough tokens are available to spend.
    Hint 3: The bucket starts full (`tokens = capacity`) and `last_time`
        starts as `None`, so the very first call must treat elapsed time as
        zero instead of computing a bogus (or crashing) time delta; also cap
        refills at `capacity` so tokens never grow unbounded.
"""

from __future__ import annotations


class TokenBucket:
    def __init__(self, capacity: float, fill_rate: float):
        raise NotImplementedError('Implement TokenBucket')
