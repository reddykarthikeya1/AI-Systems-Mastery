# Debug Lab: Module 15 — Async SQLAlchemy Traps

## How to Run
```bash
python debug_lab/broken_inventory_db.py
```

## Observed Symptoms
1. **Silent data loss (Changes not persisted)**:
   Added entities disappear completely in subsequent sessions because `await session.commit()` was never called.
