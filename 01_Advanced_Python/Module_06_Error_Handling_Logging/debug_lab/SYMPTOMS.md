# Debug Lab: Module 06 — Error Handling & Logging Traps

## How to Run
```bash
python debug_lab/broken_checkout.py
```

## Observed Symptoms
1. **Log message duplication**:
   Each log statement prints 1 time, then 2 times, then 3 times progressively.
2. **Unstoppable script / swallowed system signals**:
   Bare `except:` blocks prevent `Ctrl+C` (`KeyboardInterrupt`) from cleanly terminating the process.
3. **Lost root cause in traceback**:
   `e.__cause__` is `None`, hiding whether the transaction failed due to network, database, or validation.
