# Debug Lab: Module 24 — Modern Data Engineering Traps

## How to Run
```bash
python debug_lab/broken_analytics.py
```

## Observed Symptoms
1. **InvalidSchemaOperationError**:
   Attempting numeric operations on dirty columns fails because dirty strings coerce the entire Arrow series to `String` (`Utf8`).
