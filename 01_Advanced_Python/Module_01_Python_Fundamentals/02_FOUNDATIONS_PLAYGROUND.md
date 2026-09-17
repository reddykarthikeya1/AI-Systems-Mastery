# 🐣 Interactive Foundations Playground: Python Fundamentals & Data Model

> *"In Python, everything is an object, and every variable holds a reference."*

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
import copy
```

---

## 1. Reference Semantics and Object Identity

Variables in Python are pointers to memory addresses. Reassigning a name modifies the pointer, not the object in place.

```python
a = [1, 2, 3]
b = a
b.append(4)
assert a == [1, 2, 3, 4]
assert a is b
c = copy.deepcopy(a)
assert c == a
assert c is not a
print(f"Object identity verified: id(a)==id(b): {id(a)==id(b)}, id(a)==id(c): {id(a)==id(c)}")
```

---

## 2. Comprehensions and Filtering

Comprehensions evaluate expressions in a local scope without polluting enclosing namespaces.

```python
numbers = range(10)
evens_squared = [x**2 for x in numbers if x % 2 == 0]
assert evens_squared == [0, 4, 16, 36, 64]
assert len(evens_squared) == 5
print(f"Computed even squares: {evens_squared}")
```

---

## 3. Dictionary Invariants and Keys

Only hashable, immutable objects can serve as dictionary keys.

```python
lookup = {(1, 2): "coordinate", "title": "metadata"}
assert lookup[(1, 2)] == "coordinate"
assert "title" in lookup
assert len(lookup) == 2
print("Hashable tuple key accessed successfully.")
```

---
