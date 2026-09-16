# Interactive Foundations Playground: C Extensions, FFI & Native Interop

> *"Python gives you developer velocity; C and Rust give you raw hardware speed."*

Welcome to the **Module 22 CPython Internals Rust PyO3 Extensions** Playground! Here we demystify advanced concepts into bite-sized, runnable mental models.

---

## 1. Core Concept in 30 Seconds

Python can call compiled machine code written in C, C++, or Rust using Foreign Function Interfaces (FFI). Python's standard library `ctypes` allows calling native C shared libraries directly without any external compiler!

---

## 2. Micro-Code Example (3-5 Lines)

```python
import ctypes

# Access C standard library math functions:
# On Windows: msvcrt; On Linux/macOS: libc
try:
    libc = ctypes.CDLL("msvcrt")  # Windows C runtime
except OSError:
    libc = ctypes.CDLL("libc.so.6")  # Linux C runtime

print("Native C puts call:")
libc.puts(b"Hello from raw C runtime via Python ctypes!")
```

### Line-by-Line Breakdown:
- `ctypes.CDLL(...)`: Loads a compiled dynamic shared library (`.dll`, `.so`, or `.dylib`) into Python's process.
- Native functions expect C data types (like `c_int`, `c_char_p`, or raw `b"bytes"`).
- **PyO3:** The modern Rust framework that lets you write blazingly fast compiled extensions for Python with zero memory unsafety.

---

## 3. Run the Interactive Playground

Execute the standalone, zero-dependency sandbox in your terminal:
```bash
python 03_try_it_yourself.py
```

---

## 4. Beginner Quick-Check Drills

### Drill 1: Quick Check
What is an FFI?

<details><summary><b>Show Answer</b></summary>

Foreign Function Interface: a mechanism by which a program in one language can call routines in another language.
</details>

---

### Drill 2: Quick Check
Why are PyO3 and Rust increasingly preferred over raw C extensions?

<details><summary><b>Show Answer</b></summary>

Rust provides memory safety, preventing segmentation faults and memory leaks common in C.
</details>

---
