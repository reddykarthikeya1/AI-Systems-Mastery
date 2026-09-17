"""Beginner playground for Module 06 - Error Handling, Logging & Robustness.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import logging

# -------------------------------------------- 1. Custom Exception Hierarchies
class DomainError(Exception):
    pass

class ValidationFailure(DomainError):
    pass

def validate_age(age):
    if age < 0:
        raise ValidationFailure("Age cannot be negative")
    return True

assert validate_age(20) is True
try:
    validate_age(-5)
except ValidationFailure as exc:
    assert isinstance(exc, DomainError)
    print(f"Caught expected domain error: {exc}")

# -------------------------------------------- 2. Exception Chaining with 'from'
def parse_config(value):
    try:
        return int(value)
    except ValueError as err:
        raise DomainError("Configuration integer required") from err

try:
    parse_config("invalid")
except DomainError as err:
    assert isinstance(err.__cause__, ValueError)
    print(f"Exception chained from root cause: {type(err.__cause__).__name__}")

# -------------------------------------------- 3. Configuring Standard Logging
logger = logging.getLogger("module06_test")
logger.setLevel(logging.INFO)
assert logger.level == logging.INFO
assert logger.isEnabledFor(logging.INFO)
assert not logger.isEnabledFor(logging.DEBUG)
print("Logger configured with level INFO.")

print()
print("All checks passed.")
