# Debug Lab: Module 12 — Python Internals Traps

## How to Run
```bash
python debug_lab/broken_internals.py
```

## Observed Symptoms
1. **Memory leak from cyclic references**:
   Objects `Node("A")` and `Node("B")` are never finalized (`__del__` is never invoked) because their reference counts never drop to zero.
2. **Misleading memory measurements**:
   `sys.getsizeof()` reports virtually identical byte counts for a list containing 3 integers vs a list containing three 10,000-character strings.
