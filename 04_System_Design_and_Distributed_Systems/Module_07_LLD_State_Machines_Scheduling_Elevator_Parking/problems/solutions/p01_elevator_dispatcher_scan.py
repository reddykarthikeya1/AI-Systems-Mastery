"""Reference Solution — Problem 01: Elevator Dispatcher Scan

Topic: 07 LLD State Machines Scheduling Elevator Parking
"""

from __future__ import annotations


def elevator_dispatcher_scan(current_floor: int, direction: str, requests: list[int]) -> list[int]:
    req_set = sorted(set(requests))
    if not req_set:
        return []
    if direction == 'UP':
        up = [f for f in req_set if f >= current_floor]
        down = [f for f in req_set if f < current_floor]
        return up + sorted(down, reverse=True)
    else:
        down = [f for f in req_set if f <= current_floor]
        up = [f for f in req_set if f > current_floor]
        return sorted(down, reverse=True) + up
