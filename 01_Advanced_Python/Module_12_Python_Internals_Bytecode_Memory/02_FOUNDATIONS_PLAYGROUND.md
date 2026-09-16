# Interactive Foundations Playground: CPython Internals, Bytecode & Memory

> *"Python compiles your English text into bytecode instructions that a virtual machine executes."*

Welcome to the **Module 12 Python Internals Bytecode Memory** Playground! Here we demystify advanced concepts into bite-sized, runnable mental models.

---

## 1. Core Concept in 30 Seconds

Before executing Python code, the CPython compiler translates text into bytecode instructions. You can disassemble any function using `dis.dis()` and track memory addresses and reference counts using `id()` and `sys.getrefcount()`.

---

## 2. Micro-Code Example (3-5 Lines)

```python
import dis
import sys

def calculate(x):
    return x * 2 + 1

# Peek inside the compiled bytecode:
dis.dis(calculate)

# Check memory address:
data = [10, 20]
print("Memory Address:", hex(id(data)))
print("Active References:", sys.getrefcount(data))
```

### Line-by-Line Breakdown:
- `dis.dis()`: Disassembles a Python function or code block into assembly-like bytecode instructions.
- `LOAD_FAST`: Pushes a local variable onto CPython's evaluation stack.
- `BINARY_OP`: Pops operands, computes the operation, and pushes the result.
- `id()`: Returns the actual memory address integer of an object in RAM.
- `sys.getrefcount()`: Returns the number of active references pointing to this memory location.

---

## 3. Run the Interactive Playground

Execute the standalone, zero-dependency sandbox in your terminal:
```bash
python 03_try_it_yourself.py
```

---

## 4. Beginner Quick-Check Drills

### Drill 1: Quick Check
Why does `sys.getrefcount(x)` return 2 when you only created one variable?

<details><summary><b>Show Answer</b></summary>

The function call itself receives `x` as a parameter, temporarily incrementing the reference count by 1!
</details>

---

### Drill 2: Quick Check
Where are precompiled bytecode files stored on your machine?

<details><summary><b>Show Answer</b></summary>

In `__pycache__/` subdirectories as `.pyc` files.
</details>

---
