"""Reference Solution — Problem 01: Circuit Breaker State Machine

Topic: 06 GoF Design Patterns Scalable Systems
"""

from __future__ import annotations


def circuit_breaker_state_machine(events: list[tuple[str, int]], failure_threshold: int = 3, reset_timeout: int = 60) -> list[str]:
    state = 'CLOSED'
    consecutive_failures = 0
    trip_ts = 0
    result = []
    
    for outcome, ts in events:
        if state == 'OPEN':
            if ts >= trip_ts + reset_timeout:
                state = 'HALF_OPEN'
        
        if state == 'CLOSED':
            if outcome == 'FAILURE':
                consecutive_failures += 1
                if consecutive_failures >= failure_threshold:
                    state = 'OPEN'
                    trip_ts = ts
                    consecutive_failures = 0
            else:
                consecutive_failures = 0
        elif state == 'HALF_OPEN':
            if outcome == 'SUCCESS':
                state = 'CLOSED'
                consecutive_failures = 0
            else:
                state = 'OPEN'
                trip_ts = ts
        result.append(state)
    return result
