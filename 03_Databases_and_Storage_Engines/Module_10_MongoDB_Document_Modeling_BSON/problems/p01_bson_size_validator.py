"""Problem 01 — Bson Size Validator

Topic: 10 MongoDB Document Modeling BSON
Target: Production-grade implementation

Compute approximate BSON byte size and validate 16MB document boundary.

Example:
    >>> doc = {"name": "Alice", "active": True, "score": 42}
    >>> bson_size_validator(doc)
    (True, 45)

Hints:
    Hint 1: A BSON document's size is the sum of a fixed per-document
        overhead plus each field's own key-encoding cost plus its
        value-encoding cost — and nested documents pay that same overhead
        again, recursively.
    Hint 2: Use recursion: a helper that takes a dict, starts a running
        total at the 5-byte document overhead (4-byte length + null
        terminator), adds 1 + len(key) + 1 bytes per key, then dispatches on
        the value's Python type to add the right value size (recursing into
        calc_size for nested dicts).
    Hint 3: Check `isinstance(v, bool)` before `isinstance(v, int)` — in
        Python `bool` is a subclass of `int`, so True/False must be caught
        first or they'll be mis-costed as 8-byte ints instead of 1-byte
        bools; strings also need their UTF-8 byte length, not len(str),
        since multi-byte characters would otherwise undercount.
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
