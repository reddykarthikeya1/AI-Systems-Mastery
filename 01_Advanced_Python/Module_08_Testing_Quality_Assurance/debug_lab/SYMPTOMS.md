# Debug Lab: Module 08 — Testing Traps

## How to Run
```bash
python debug_lab/broken_ledger.py
```

## Observed Symptoms
1. **False-positive passing test due to tuple assertion**:
   `assert (99 == 100, "Error")` passes without raising `AssertionError` because a non-empty tuple is always truthy.
2. **Order dependence and flaky test runs**:
   Running tests under `pytest-randomly` causes `test_step_two_assumes_step_one_ran` to fail intermittently.
3. **Fragile floating-point test failure**:
   `assert 0.1 + 0.2 == 0.3` fails with `AssertionError: assert 0.30000000000000004 == 0.3`.
