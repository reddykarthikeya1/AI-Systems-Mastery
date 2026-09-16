# Debug Lab: Module 01 — Fundamentals Traps

## How to Run
```bash
python debug_lab/broken_calculator.py
```

## Observed Symptoms
1. **Financial balance verification returns `False`**:
   `0.1 + 0.2 == 0.3` evaluates to `False`, causing balanced transactions to be rejected.
2. **Account identity comparison fails unpredictably**:
   `calculate_tier_bonus(100, 100)` returns `True`, but `calculate_tier_bonus(1000, 1000)` returns `False`!
3. **Missing payment installment**:
   Generating a 12-month installment schedule only returns 11 entries; the loan under-collects by an entire month.
