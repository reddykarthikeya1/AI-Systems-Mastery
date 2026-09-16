# Debug Lab: Module 18 — Distributed Systems Traps

## How to Run
```bash
python debug_lab/broken_distributed_pipeline.py
```

## Observed Symptoms
1. **Double debiting / Data corruption under redelivery**:
   When a message broker redelivers an unacknowledged task, Alice is debited twice ($200 instead of $100).
