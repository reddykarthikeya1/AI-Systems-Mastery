"""Problem 01 — Data Descriptor Validation

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


class TypedField:
    def __init__(self, expected_type: type):
        raise NotImplementedError('Implement TypedField')
    def __set_name__(self, owner, name):
        self.name = name
    def __get__(self, instance, owner):
        raise NotImplementedError()
    def __set__(self, instance, value):
        raise NotImplementedError()
