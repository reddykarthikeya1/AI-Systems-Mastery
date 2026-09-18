"""Problem 01 — Token Bucket Rate Limiter

Target: Production-grade implementation
"""

from __future__ import annotations


class TokenBucket:
    def __init__(self, capacity: float, fill_rate: float):
        self.capacity = capacity
        self.fill_rate = fill_rate
        self.tokens = capacity
        self.last_time = None
    def allow(self, current_time: float, tokens: float = 1.0) -> bool:
        if self.last_time is None:
            self.last_time = current_time
        elapsed = current_time - self.last_time
        self.tokens = min(self.capacity, self.tokens + elapsed * self.fill_rate)
        self.last_time = current_time
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
