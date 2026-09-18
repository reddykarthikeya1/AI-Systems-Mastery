"""Problem 01 — Pydantic Schema Field Pruner

Target: Production-grade implementation

Example:
    >>> prune_sensitive_fields(
    ...     {'user': 'alice', 'password_hash': 'secret', 'meta': {'token': 'abc', 'active': True}},
    ...     {'password_hash', 'token'},
    ... )
    {'user': 'alice', 'meta': {'active': True}}

Hints:
    Hint 1: The disallowed set names keys, not values — the same key can appear
        again once you recurse into nested dicts, so pruning has to happen at
        every level, not just the top one.
    Hint 2: Build a new dict rather than mutating the input; recurse on dict
        values, and remember a list can itself contain dicts that need pruning.
    Hint 3: Non-dict, non-list values (numbers, strings, booleans, None) must
        pass through untouched, and an empty dict left after pruning a nested
        level is still valid output — don't drop keys just because their value
        became `{}`.
"""

from __future__ import annotations


def prune_sensitive_fields(payload: dict, disallowed: set[str]) -> dict:
    raise NotImplementedError('Implement prune_sensitive_fields')
