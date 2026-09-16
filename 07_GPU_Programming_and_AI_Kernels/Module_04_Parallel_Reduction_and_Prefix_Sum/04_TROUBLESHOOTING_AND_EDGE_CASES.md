# Troubleshooting & Edge Cases: Parallel Reduction & Prefix Sum

## Production Traps & Silent Failure Modes

### 1. Missing Active Mask in `__shfl_down_sync`
- **Symptom**: Undefined behavior or deadlock on Volta, Hopper, or Blackwell GPUs.
- **Root Cause**: Passing `0xFFFFFFFF` mask when some threads in the warp are inactive due to boundary conditions.
- **Fix**: Always pass `__activemask()` when calling warp shuffles inside divergent branch sections:
  `val += __shfl_down_sync(__activemask(), val, offset);`
