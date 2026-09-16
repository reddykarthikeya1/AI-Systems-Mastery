# Troubleshooting & Edge Cases: Collective Communications

## Production Traps & Silent Failure Modes

### 1. NCCL Ring Deadlock from Unordered Barrier Calls
- **Symptom**: All GPUs hang at 100% compute with 0% memory throughput indefinitely.
- **Root Cause**: Rank 0 issues an AllReduce on Group A, while Rank 1 issues an AllReduce on Group B in different order.
  - NCCL's internal proxy thread locks the ring waiting for matching sequence IDs, causing a circular deadlock!
- **Fix**: Guarantee identical collective execution ordering across all ranks.
