"""Problem 01 — Circuit Breaker State Machine

Topic: 06 GoF Design Patterns Scalable Systems
Target: Production-grade implementation

Manage circuit breaker transitions: CLOSED, OPEN, HALF_OPEN.

Example:
    >>> circuit_breaker_state_machine([('FAILURE', 10), ('FAILURE', 11), ('FAILURE', 12), ('SUCCESS', 80)], 3, 60)
    ['CLOSED', 'CLOSED', 'OPEN', 'CLOSED']

Hints:
    Hint 1: Three states form a cycle driven by two separate clocks: a
        consecutive-failure counter while CLOSED, and elapsed wall-clock
        time since the trip while OPEN.
    Hint 2: Track the current state, a `consecutive_failures` counter, and
        the `trip_ts` timestamp of the last trip; walk the events in
        order, appending the resulting state after each one.
    Hint 3: The OPEN -> HALF_OPEN check must use the CURRENT event's
        timestamp before deciding how that same event affects the state
        (the test's ts=80 both triggers HALF_OPEN and, as a SUCCESS,
        immediately closes it in one step); a SUCCESS while CLOSED must
        reset the failure counter to 0.
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
