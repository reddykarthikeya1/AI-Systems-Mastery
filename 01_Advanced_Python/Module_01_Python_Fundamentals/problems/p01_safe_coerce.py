"""Problem 01 — Safe Type Coercion Utility

Target: Production-grade implementation

Example:
    >>> safe_coerce('42', 'int')
    42
    >>> safe_coerce('bad', 'int', default=-1)
    -1

Hints:
    Hint 1: `None` and any value that fails conversion should fall back to
        `default` instead of raising — the function must never propagate an
        exception to the caller.
    Hint 2: Wrap the conversion attempt in a try/except, and dispatch on
        `target_type` ('int', 'float', 'bool') to decide how to interpret
        `val` before converting it.
    Hint 3: 'bool' needs its own string parsing (e.g. 'true'/'1'/'yes' vs.
        'false'/'0'/'no', case-insensitively) since `bool('false')` is truthy;
        and 'float' must treat NaN/inf results as failures that fall back to
        `default` rather than valid floats.
"""

from __future__ import annotations


def safe_coerce(val: object, target_type: str, default: object = None) -> object:
    raise NotImplementedError('Implement safe_coerce')
