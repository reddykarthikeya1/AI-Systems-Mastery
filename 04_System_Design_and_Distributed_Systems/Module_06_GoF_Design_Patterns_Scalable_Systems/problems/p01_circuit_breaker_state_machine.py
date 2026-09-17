"""Problem 01 — Circuit Breaker State Machine

Topic: 06 GoF Design Patterns Scalable Systems
Target: Production-grade implementation

Manage circuit breaker transitions: CLOSED, OPEN, HALF_OPEN.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def circuit_breaker_state_machine(events: list[tuple[str, int]], failure_threshold: int = 3, reset_timeout: int = 60) -> list[str]:
    """events: list of (outcome, timestamp) where outcome is 'SUCCESS' or 'FAILURE'.
    States: 'CLOSED', 'OPEN', 'HALF_OPEN'.
    Starts CLOSED.
    - CLOSED: consecutive failures >= failure_threshold -> OPEN at failure ts.
    - OPEN: if current_ts >= trip_ts + reset_timeout -> transitions to HALF_OPEN to test.
    - HALF_OPEN: 1 SUCCESS -> CLOSED; 1 FAILURE -> OPEN again.
    Returns list of states after each event.
    """
    raise NotImplementedError("Implement circuit_breaker_state_machine")
