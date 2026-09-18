"""Problem 01 — Sliding Idempotency Deduplicator

Target: Production-grade implementation

Example:
    >>> stream = [('k1', 'val1'), ('k2', 'val2'), ('k1', 'val1_dup'), ('k3', 'val3')]
    >>> deduplicate_events(stream)
    [('k1', 'val1'), ('k2', 'val2'), ('k3', 'val3')]

Hints:
    Hint 1: This models an idempotency key store: once a key has been seen,
        every later event carrying that same key is a retry/duplicate and
        must be discarded, not merged or overwritten.
    Hint 2: Walk the list once, keeping a set of keys seen so far and a
        separate output list you append the first-seen `(key, payload)` pairs
        to — a single linear pass is enough.
    Hint 3: Keep the FIRST payload for a repeated key, not the latest one
        (the duplicate's payload is discarded even if it differs), and
        preserve the original event order in the output.
"""

from __future__ import annotations


def deduplicate_events(events: list[tuple[str, str]]) -> list[tuple[str, str]]:
    raise NotImplementedError('Implement deduplicate_events')
