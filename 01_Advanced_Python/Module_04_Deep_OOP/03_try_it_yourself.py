"""Beginner playground for Module 04 - Deep Object-Oriented Programming.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from dataclasses import dataclass

# -------------------------------------------- 1. Custom Operator Overloading via Dunder Methods
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

v1 = Vector2D(1, 2)
v2 = Vector2D(3, 4)
v3 = v1 + v2
assert v3 == Vector2D(4, 6)
assert (v3.x, v3.y) == (4, 6)
print(f"Vector addition: ({v1.x},{v1.y}) + ({v2.x},{v2.y}) = ({v3.x},{v3.y})")

# -------------------------------------------- 2. Encapsulation with Properties
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, val):
        if val < -273.15:
            raise ValueError("Below absolute zero!")
        self._celsius = val

t = Temperature(25)
assert t.celsius == 25
t.celsius = 30
assert t.celsius == 30
print(f"Validated property updated to: {t.celsius} C")

# -------------------------------------------- 3. Dataclasses for Clean Value Objects
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p1 = Point(1.5, 2.5)
p2 = Point(1.5, 2.5)
assert p1 == p2
assert hash(p1) == hash(p2)
print(f"Immutable dataclass point created: {p1}")

print()
print("All checks passed.")
