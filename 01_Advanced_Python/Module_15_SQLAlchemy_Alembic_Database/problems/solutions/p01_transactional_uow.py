"""Problem 01 — Unit of Work Transaction Manager

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


class UnitOfWork:
    def __init__(self):
        self.state = 'idle'
        self.log = []
    def __enter__(self):
        self.state = 'active'
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.state = 'rolled_back'
            self.log.append('rollback')
            return False
        self.state = 'committed'
        self.log.append('commit')
        return True
