# Troubleshooting & Production Edge Cases

### 1. Zero Combinations in Pass@k Calculation
- **Symptom**: `ValueError: n - c must be greater than or equal to k` or division by zero.
- **Root Cause**: Math combinations overflow or unhandled edge cases where $n < k$.
- **Fix**: Guard clauses: if $n - c < k$, return 1.0; if $n < k$, raise `ValueError("Sample count n must be >= k")`.

### 2. Sandbox Deadlocks on Unit Test Execution
- **Symptom**: Evaluation suite hangs on an infinite `while True:` loop in candidate code.
- **Root Cause**: Candidate code lacked execution timeout guards.
- **Fix**: Run unit tests in subprocesses bounded by a strict 1-second timeout.
