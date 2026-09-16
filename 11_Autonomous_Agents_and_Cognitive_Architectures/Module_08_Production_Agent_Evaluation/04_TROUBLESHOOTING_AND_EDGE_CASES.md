# Troubleshooting & Production Edge Cases

### 1. Flaky Benchmark Tests Due to Non-Deterministic Environment State
- **Symptom**: The same agent achieves 80% pass rate on Run 1, but 65% on Run 2.
- **Root Cause**: Tests leave leftover files or database rows in the execution sandbox.
- **Fix**: Re-instantiate a clean filesystem container for every individual benchmark task.

### 2. Gaming the Metric via Early Abandonment
- **Symptom**: An agent shows 100% Step Efficiency by quitting immediately on complex tasks.
- **Root Cause**: Step efficiency was calculated without conditioning on task success.
- **Fix**: Only compute Step Efficiency on tasks where `task_success == True`.
