"""Beginner playground for Module 14 - Pydantic & Data Validation.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from typing import get_type_hints

# -------------------------------------------- 1. Introspecting Type Annotations
class UserSchema:
    name: str
    age: int
    active: bool

hints = get_type_hints(UserSchema)
assert hints["name"] is str
assert hints["age"] is int
assert hints["active"] is bool
print(f"Extracted type hints: {hints}")

# -------------------------------------------- 2. Runtime Type Coercion and Validation
def validate_payload(data, schema):
    hints = get_type_hints(schema)
    validated = {}
    for key, expected_type in hints.items():
        if key not in data:
            raise ValueError(f"Missing field {key}")
        raw = data[key]
        validated[key] = expected_type(raw)
    return validated

data = {"name": "Charlie", "age": "28", "active": 1}
res = validate_payload(data, UserSchema)
assert res["age"] == 28
assert isinstance(res["age"], int)
assert res["name"] == "Charlie"
print(f"Validated and coerced payload: {res}")

# -------------------------------------------- 3. Field Constraint Checking
def check_age_bounds(age):
    assert 0 <= age <= 120, "Age out of bounds"
    return True

assert check_age_bounds(25) is True
assert check_age_bounds(0) is True
print("Age boundary constraints verified.")

print()
print("All checks passed.")
