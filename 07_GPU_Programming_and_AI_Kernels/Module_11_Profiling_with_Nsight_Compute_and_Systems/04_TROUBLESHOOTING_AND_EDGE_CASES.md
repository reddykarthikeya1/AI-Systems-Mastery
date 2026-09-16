# Troubleshooting & Edge Cases: Profiling with NCU & NSYS

## Production Traps & Silent Failure Modes

### 1. Profiler Overhead Distorting Latencies
- **Symptom**: Kernel runs $20\times$ slower under Nsight Compute than in production.
- **Root Cause**: NCU replays kernel passes multiple times to collect hardware performance counters (Kernel Replay mode).
- **Fix**: Use `--replay-mode application` or filter profiling to specific kernel launches using `cudaProfilerStart()` and `cudaProfilerStop()`.
