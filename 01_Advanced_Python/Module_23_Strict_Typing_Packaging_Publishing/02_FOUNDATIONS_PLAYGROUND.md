# Interactive Foundations Playground: Strict Typing & Modern Packaging

> *"Types are machine-checked documentation that catch bugs before production."*

Welcome to the **Module 23 Strict Typing Packaging Publishing** Playground! Here we demystify advanced concepts into bite-sized, runnable mental models.

---

## 1. Core Concept in 30 Seconds

Modern Python uses type hints (`typing`) to eliminate runtime bugs during development. Packaging with `pyproject.toml` packages your code into distributable `.whl` (Wheel) archives ready for `pip install`.

---

## 2. Micro-Code Example (3-5 Lines)

```python
from typing import TypeVar, Sequence

T = TypeVar("T")

def get_first_element(items: Sequence[T]) -> T | None:
    if items:
        return items[0]
    return None

print(get_first_element([10, 20, 30]))     # 10 (typed as int)
print(get_first_element(["a", "b", "c"]))  # "a" (typed as str)
```

### Line-by-Line Breakdown:
- `TypeVar("T")`: A generic placeholder that binds to whatever type is passed in.
- `Sequence[T]`: Accepts any ordered sequence (lists, tuples, strings).
- `T | None`: Modern Python 3.10+ union syntax (replaces `Optional[T]`).
- `pyproject.toml`: The PEP 621 standard file defining metadata, dependencies, and build tools.

---

## 3. Run the Interactive Playground

Execute the standalone, zero-dependency sandbox in your terminal:
```bash
python 03_try_it_yourself.py
```

---

## 4. Beginner Quick-Check Drills

### Drill 1: Quick Check
What tool checks Python type annotations without executing the code?

<details><summary><b>Show Answer</b></summary>

Static type checkers like `mypy` or `pyright`.
</details>

---

### Drill 2: Quick Check
What is the standard configuration file for modern Python packages?

<details><summary><b>Show Answer</b></summary>

`pyproject.toml`.
</details>

---
