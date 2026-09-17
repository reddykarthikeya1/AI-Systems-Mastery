"""Problem 01 — Elevator Dispatcher Scan

Topic: 07 LLD State Machines Scheduling Elevator Parking
Target: Production-grade implementation

SCAN (LOOK) elevator floor scheduling servicing pending calls.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def elevator_dispatcher_scan(current_floor: int, direction: str, requests: list[int]) -> list[int]:
    """direction is 'UP' or 'DOWN'.
    Requests are floors to visit.
    If 'UP': visit all requests >= current_floor in ascending order, then reverse to service remaining in descending order.
    If 'DOWN': visit all requests <= current_floor in descending order, then reverse to service remaining in ascending order.
    Returns ordered list of visited floors.
    """
    raise NotImplementedError("Implement elevator_dispatcher_scan")
