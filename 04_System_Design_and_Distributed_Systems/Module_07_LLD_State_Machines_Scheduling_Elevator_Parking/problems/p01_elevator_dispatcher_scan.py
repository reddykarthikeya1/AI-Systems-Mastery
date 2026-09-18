"""Problem 01 — Elevator Dispatcher Scan

Topic: 07 LLD State Machines Scheduling Elevator Parking
Target: Production-grade implementation

SCAN (LOOK) elevator floor scheduling servicing pending calls.

Example:
    >>> elevator_dispatcher_scan(5, 'UP', [2, 8, 3, 7, 5])
    [5, 7, 8, 3, 2]

Hints:
    Hint 1: SCAN visits everything "ahead" of the car in its current
        direction of travel first, then reverses for the rest — it does
        not answer calls in the order they were requested.
    Hint 2: De-duplicate and sort the requests, split them relative to
        `current_floor` into an "ahead" group and a "behind" group, order
        each group appropriately, and concatenate the two.
    Hint 3: A request exactly at `current_floor` belongs in the "ahead"
        group when moving UP (the test shows floor 5 serviced first while
        going UP from floor 5); the "behind" group must be reversed —
        descending for UP, ascending for DOWN — since the car only
        reaches it after finishing the ahead group.
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
