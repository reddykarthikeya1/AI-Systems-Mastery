"""Problem 01 — Sliding Idempotency Deduplicator

Target: Production-grade implementation
"""

from __future__ import annotations


def deduplicate_events(events: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen = set()
    result = []
    for key, payload in events:
        if key not in seen:
            seen.add(key)
            result.append((key, payload))
    return result
