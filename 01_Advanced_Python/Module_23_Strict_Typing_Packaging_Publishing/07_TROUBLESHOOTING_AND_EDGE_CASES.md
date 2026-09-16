# Module 23: Troubleshooting, Typing Traps & Packaging Pitfalls

This reference guide details common Mypy type-checking errors and library distribution bugs.

---

## 1. The Missing `py.typed` Marker Trap

### The Bug
You write a library with 100% complete type annotations, package it, and install it in another project. When users run `mypy`, Mypy ignores all your types and reports `Skipping analyzing "my_library": module is installed, but missing library stubs or py.typed marker`.

### The Fix
Include an empty file named `py.typed` inside your package source folder:
```bash
touch src/my_library/py.typed
```
And ensure your build backend packages it in wheels.

---

## 2. Circular Type Imports with `TYPE_CHECKING`

### The Bug
Class A imports Class B for type hints; Class B imports Class A. Running Python raises `ImportError: cannot import name ... from partially initialized module`.

### The Fix
Use `typing.TYPE_CHECKING` and `from __future__ import annotations`:
```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from other_module import ClassB # Executed ONLY during static analysis!
```
