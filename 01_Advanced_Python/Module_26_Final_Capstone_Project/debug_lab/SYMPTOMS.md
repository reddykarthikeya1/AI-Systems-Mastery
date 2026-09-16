# Debug Lab: Module 26 — Master Capstone Integration Traps

## How to Run
```bash
python debug_lab/broken_capstone.py
```

## Observed Symptoms
1. **Cross-subsystem silent failure / KeyError**:
   Background task fails with `KeyError: 'target_format'` because the API endpoint produced a payload using an older parameter name (`format`).
