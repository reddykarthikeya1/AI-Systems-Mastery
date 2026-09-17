# 🐣 Interactive Foundations Playground: Deep Object-Oriented Programming

> *"Python's data model allows objects to customize operator semantics through dunder methods."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
from dataclasses import dataclass
```

---

## 1. Custom Operator Overloading via Dunder Methods

Implementing `__repr__` and `__add__` enables seamless composition of domain value objects.

```python
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
```

---

## 2. Encapsulation with Properties

Properties allow programmatic validation without breaking attribute access syntax.

```python
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
```

---

## 3. Dataclasses for Clean Value Objects

Dataclasses automatically generate initialization, equality, and representation methods.

```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p1 = Point(1.5, 2.5)
p2 = Point(1.5, 2.5)
assert p1 == p2
assert hash(p1) == hash(p2)
print(f"Immutable dataclass point created: {p1}")
```

---
