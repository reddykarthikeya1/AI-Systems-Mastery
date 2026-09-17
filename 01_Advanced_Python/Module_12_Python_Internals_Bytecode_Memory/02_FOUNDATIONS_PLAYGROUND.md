# 🐣 Interactive Foundations Playground: Python Internals: Bytecode & Memory

> *"Understanding CPython bytecode and garbage collection unlocks extreme performance tuning."*

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
import dis
import gc
import sys
```

---

## 1. Disassembling Bytecode Opcodes

The `dis` module compiles Python functions into readable CPython virtual machine instructions.

```python
def add(a, b):
    return a + b

instructions = list(dis.get_instructions(add))
opnames = [instr.opname for instr in instructions]
assert any("LOAD_FAST" in name for name in opnames)
assert any("BINARY_OP" in name or "BINARY_ADD" in name for name in opnames)
assert "RETURN_VALUE" in opnames
print(f"CPython bytecode instructions for add(): {opnames}")
```

---

## 2. Object Memory Overhead with sys.getsizeof

Every Python object incurs memory overhead for reference counts and type pointers.

```python
size_empty_int = sys.getsizeof(0)
size_large_int = sys.getsizeof(2**64)
assert size_empty_int >= 24
assert size_large_int > size_empty_int
print(f"Memory size of 0: {size_empty_int} bytes, large int: {size_large_int} bytes")
```

---

## 3. Garbage Collector Cycle Tracking

CPython uses reference counting supplemented by a generational cyclic garbage collector.

```python
gc_enabled = gc.isenabled()
assert gc_enabled is True
thresholds = gc.get_threshold()
assert len(thresholds) == 3
print(f"GC active with generational thresholds: {thresholds}")
```

---
