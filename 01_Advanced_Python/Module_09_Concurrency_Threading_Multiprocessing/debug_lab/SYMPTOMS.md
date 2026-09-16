# Debug Lab: Module 09 — Threading & Multiprocessing Traps

## How to Run
```bash
python debug_lab/broken_pipeline.py
```

## Observed Symptoms
1. **Non-deterministic race condition counter loss**:
   Final counter value is 20,000–50,000 instead of the expected 100,000 due to lost updates.
2. **Permanent process hang (Deadlock)**:
   Thread 1 holds `lock_a` waiting for `lock_b`; Thread 2 holds `lock_b` waiting for `lock_a`.
3. **Corrupted or truncated output files from daemon threads**:
   Daemon threads are forcibly terminated when the main thread finishes, leaving buffers unflushed.
