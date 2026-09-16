# Troubleshooting & Edge Cases: GPU Microarchitecture

## Production Traps & Silent Failure Modes

### 1. Warp Divergence Serialization
- **Symptom**: Kernel executes at 50% or 25% of expected throughput with high active warp counts in Nsight Compute.
- **Root Cause**: Conditionals inside thread blocks depending on `threadIdx.x % 2` or `threadIdx.x % 4`.
- **Diagnosis**: Check `smsp__warp_execution_efficiency.pct` in NCU. If it is below 80%, intra-warp branching is serializing execution.
- **Fix**: Reorganize data or thread assignments so that branching evaluates uniformly across all 32 threads in a warp (`threadIdx.x / 32`).

### 2. Tail Latency & Grid Wavefront Tail Effect
- **Symptom**: The last 5% of a kernel run takes 40% of the execution time.
- **Root Cause**: The number of thread blocks in the grid is not a multiple of the number of SMs.
  - For example, launching 133 blocks on an H100 with 132 SMs:
  - Wave 1: 132 blocks execute concurrently across 132 SMs.
  - Wave 2: 1 single block executes on 1 SM while 131 SMs sit completely idle!
- **Fix**: Quantize grid dimensions to multiples of SM count, or use grid-stride loops to allow a fixed number of blocks to cooperatively process work.
