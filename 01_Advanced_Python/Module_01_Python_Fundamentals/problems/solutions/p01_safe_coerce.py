"""Problem 01 — Safe Type Coercion Utility

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def safe_coerce(val: object, target_type: str, default: object = None) -> object:
    if val is None:
        return default
    try:
        if target_type == 'int':
            return int(float(val))
        elif target_type == 'float':
            import math
            f = float(val)
            return default if math.isnan(f) or math.isinf(f) else f
        elif target_type == 'bool':
            if isinstance(val, str):
                s = val.strip().lower()
                if s in ('true', '1', 'yes'): return True
                if s in ('false', '0', 'no'): return False
                return default
            return bool(val)
        return default
    except Exception:
        return default
