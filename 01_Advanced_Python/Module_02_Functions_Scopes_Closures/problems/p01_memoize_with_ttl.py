"""Problem 01 — Memoization Closure with TTL

Target: Production-grade implementation

Example:
    >>> @memoize_with_ttl(10.0)
    ... def add_one(x):
    ...     return x + 1
    >>> add_one(2)
    3
    >>> add_one(2)
    3
    >>> add_one.stats
    {'hits': 1, 'misses': 1}

Hints:
    Hint 1: The decorator must remember, per distinct call, both the result
        and when it was produced, so a later call within the TTL window can
        reuse it instead of recomputing.
    Hint 2: Build a key from `args` and a sorted, hashable form of `kwargs`
        (dict order isn't guaranteed) and store `(result, timestamp)` per key
        in a closure-captured cache dict; expose a `stats` dict of hit/miss
        counts as an attribute on the wrapper.
    Hint 3: Compare `now - timestamp` against `ttl_seconds` with a strict `<`
        so an entry exactly at the boundary is treated as expired, and make
        sure `@wraps(fn)` is used so the wrapper doesn't shadow the wrapped
        function's identity/metadata.
"""

from __future__ import annotations


def memoize_with_ttl(ttl_seconds: float = 60.0):
    raise NotImplementedError('Implement memoize_with_ttl')
