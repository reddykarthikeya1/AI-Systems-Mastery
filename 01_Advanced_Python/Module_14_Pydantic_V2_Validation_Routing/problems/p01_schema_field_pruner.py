"""Problem 01 — Pydantic Schema Field Pruner

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def prune_sensitive_fields(payload: dict, disallowed: set[str]) -> dict:
    raise NotImplementedError('Implement prune_sensitive_fields')
