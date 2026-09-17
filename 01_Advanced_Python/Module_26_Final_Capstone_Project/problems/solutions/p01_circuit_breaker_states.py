"""Problem 01 — Circuit Breaker State Machine

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3):
        self.threshold = failure_threshold
        self.failures = 0
        self.state = 'CLOSED'
    def record_success(self):
        self.failures = 0
        self.state = 'CLOSED'
    def record_failure(self):
        self.failures += 1
        if self.failures >= self.threshold:
            self.state = 'OPEN'
    def allow_request(self) -> bool:
        return self.state != 'OPEN'
