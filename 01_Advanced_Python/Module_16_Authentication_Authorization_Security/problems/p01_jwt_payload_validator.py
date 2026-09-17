"""Problem 01 — JWT Claims Invariant Validator

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def validate_jwt_claims(claims: dict, current_time: int, expected_aud: str, expected_iss: str) -> tuple[bool, str]:
    raise NotImplementedError('Implement validate_jwt_claims')
