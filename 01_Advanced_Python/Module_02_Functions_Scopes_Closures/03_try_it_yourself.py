"""Beginner playground for Module 02 - Functions, Scopes & Closures.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import functools

# -------------------------------------------- 1. Lexical Scoping and the LEGB Rule
x = "global"
def outer():
    x = "enclosing"
    def inner():
        return x
    return inner()

assert outer() == "enclosing"
assert x == "global"
print(f"LEGB resolution: outer returned '{outer()}'")

# -------------------------------------------- 2. State Retention in Closures
def make_counter(start=0):
    count = start
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

c = make_counter(10)
assert c() == 11
assert c() == 12
assert c() == 13
print("Closure state persisted across function invocations.")

# -------------------------------------------- 3. Partial Application with functools
def power(base, exponent):
    return base ** exponent

square = functools.partial(power, exponent=2)
assert square(5) == 25
assert square(9) == 81
print("Partial function frozen exponent=2 successfully.")

print()
print("All checks passed.")
