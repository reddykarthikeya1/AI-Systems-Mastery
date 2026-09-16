# Debug Lab: Module 05 — Decorator, Generator & Context Manager Traps

## How to Run
```bash
python debug_lab/broken_log_analyzer.py
```

## Observed Symptoms
1. **Introspection and docstring loss**:
   `parse_access_log.__name__` returns `'wrapper'` instead of `'parse_access_log'`.
2. **Generator produces empty results on second pass**:
   Processing the stream a second time returns 0 items without warning.
3. **Critical exceptions silently swallowed**:
   A fatal `KeyError` inside a database block is swallowed, masking critical data corruption.
