# Troubleshooting & Edge Cases: Tiled GEMM

## Production Traps & Silent Failure Modes

### 1. Missing Barrier Before Overwriting Shared Memory
- **Symptom**: Intermittent numerical inaccuracies or race conditions in matrix outputs.
- **Root Cause**: Having a `__syncthreads()` after loading shared memory, but forgetting the second `__syncthreads()` after the compute loop.
  - Fast threads from iteration $k+1$ start loading new data into `sA` while slow threads from iteration $k$ are still computing on the old data!
- **Fix**: Always include two barriers per iteration:
  `__syncthreads(); // Wait for load`
  `compute(...);`
  `__syncthreads(); // Wait for compute before next load`
