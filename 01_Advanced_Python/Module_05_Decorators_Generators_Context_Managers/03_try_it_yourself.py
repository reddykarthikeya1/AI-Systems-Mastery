"""Beginner playground for Module 05 - Decorators, Generators & Context Managers.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from contextlib import contextmanager
import functools

# -------------------------------------------- 1. Function Decorators Preserving Metadata
call_log = []
def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        call_log.append(func.__name__)
        return func(*args, **kwargs)
    return wrapper

@trace
def greet(name):
    """Greeting function docstring."""
    return f"Hello, {name}!"

res = greet("Pythonista")
assert res == "Hello, Pythonista!"
assert greet.__name__ == "greet"
assert call_log == ["greet"]
print(f"Decorated function executed: {res}")

# -------------------------------------------- 2. Stateful Generators with Yield
def fibonacci(limit):
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1

fibs = list(fibonacci(7))
assert fibs == [0, 1, 1, 2, 3, 5, 8]
assert len(fibs) == 7
print(f"Generated first 7 Fibonacci numbers: {fibs}")

# -------------------------------------------- 3. Deterministic Resource Management
cleanup_done = False
@contextmanager
def temporary_resource():
    global cleanup_done
    try:
        yield "resource_handle"
    finally:
        cleanup_done = True

with temporary_resource() as handle:
    assert handle == "resource_handle"
    assert not cleanup_done

assert cleanup_done
print("Context manager cleanup executed deterministically.")

print()
print("All checks passed.")
