# Troubleshooting & Production Edge Cases

### 1. RecursionLimitExceeded Error
- **Symptom**: Graph raises `RecursionLimitExceeded: Maximum supersteps 25 reached`.
- **Root Cause**: Conditional edge logic failed to evaluate termination condition properly, causing infinite node ping-pong.
- **Fix**: Inspect router return values and ensure state mutations progress monotonically towards the termination threshold.

### 2. State Mutation Side Effects (Shallow Copy Bugs)
- **Symptom**: Node B sees modifications made by Node A before Superstep $k$ concludes.
- **Root Cause**: Node A mutated a nested list or dict in-place without deep-copying.
- **Fix**: Freeze state or enforce `copy.deepcopy` when dispatching state to worker nodes.
