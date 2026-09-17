"""Problem 01 — Subclass Auto-Registration Metaclass

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


class RegistryMeta(type):
    registry = {}
    def __new__(mcls, name, bases, attrs):
        raise NotImplementedError('Implement RegistryMeta')
