# Debug Lab: Module 23 — Strict Typing Traps

## How to Run
```bash
python debug_lab/broken_typed_sdk.py
```

## Observed Symptoms
1. **Type checker false-safety via `Any`**:
   `mypy` reports 0 errors because `Any` disables type analysis, but code crashes at runtime with `AttributeError`.
