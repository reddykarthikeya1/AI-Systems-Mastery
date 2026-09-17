"""Problem 01 — Bson Size Validator

Topic: 10 MongoDB Document Modeling BSON
Target: Production-grade implementation

Compute approximate BSON byte size and validate 16MB document boundary.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def bson_size_validator(doc: dict, max_bytes: int = 16 * 1024 * 1024) -> tuple[bool, int]:
    """Calculate approximate BSON serialized size:
    - 4 bytes doc length header + 1 byte null terminator
    - each key: 1 byte type + len(key_utf8) + 1 byte null
    - int value: 8 bytes
    - float value: 8 bytes
    - str value: 4 bytes length + len(str_utf8) + 1 byte null
    - bool value: 1 byte
    - nested dict: recursively calculated doc size
    Returns (is_valid, computed_bytes).
    """
    raise NotImplementedError("Implement bson_size_validator")
