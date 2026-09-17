"""Beginner playground for Module 12 - Python Internals: Bytecode & Memory.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import dis
import gc
import sys

# -------------------------------------------- 1. Disassembling Bytecode Opcodes
def add(a, b):
    return a + b

instructions = list(dis.get_instructions(add))
opnames = [instr.opname for instr in instructions]
assert any("LOAD_FAST" in name for name in opnames)
assert any("BINARY_OP" in name or "BINARY_ADD" in name for name in opnames)
assert "RETURN_VALUE" in opnames
print(f"CPython bytecode instructions for add(): {opnames}")

# -------------------------------------------- 2. Object Memory Overhead with sys.getsizeof
size_empty_int = sys.getsizeof(0)
size_large_int = sys.getsizeof(2**64)
assert size_empty_int >= 24
assert size_large_int > size_empty_int
print(f"Memory size of 0: {size_empty_int} bytes, large int: {size_large_int} bytes")

# -------------------------------------------- 3. Garbage Collector Cycle Tracking
gc_enabled = gc.isenabled()
assert gc_enabled is True
thresholds = gc.get_threshold()
assert len(thresholds) == 3
print(f"GC active with generational thresholds: {thresholds}")

print()
print("All checks passed.")
