"""Problem 01 — Circuit Breaker State Machine

Target: Production-grade implementation

Example:
    >>> cb = CircuitBreaker(failure_threshold=2)
    >>> cb.allow_request()
    True
    >>> cb.record_failure()
    >>> cb.record_failure()
    >>> cb.state
    'OPEN'
    >>> cb.allow_request()
    False
    >>> cb.record_success()
    >>> cb.state
    'CLOSED'

Hints:
    Hint 1: This is a small state machine, not a counter you check inline —
        `state` should be the single source of truth that `allow_request`
        reads, updated only by the two `record_*` methods.
    Hint 2: Track a consecutive-failure count and a `state` string
        ('CLOSED'/'OPEN'); `record_failure` increments the count and flips to
        'OPEN' once it reaches `failure_threshold`, while `record_success`
        resets both.
    Hint 3: A single success must fully reset the breaker (failure count back
        to 0, state back to 'CLOSED') even after it has tripped open — the
        test explicitly recloses an OPEN circuit this way — and
        `allow_request` simply reflects whether `state` is not `'OPEN'`.
"""

from __future__ import annotations


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3):
        raise NotImplementedError('Implement CircuitBreaker')
