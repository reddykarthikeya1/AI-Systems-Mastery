# Troubleshooting & Edge Cases: CUDA C++ Fundamentals

## Production Traps & Silent Failure Modes

### 1. Asynchronous Error Masking
- **Symptom**: Kernel launches exit with code 0, but subsequent memory operations crash with `cudaErrorIllegalAddress`.
- **Root Cause**: Kernel launches in CUDA are **asynchronous**. The CPU returns immediately before the GPU encounters an illegal memory access or segmentation fault.
- **Fix**: Wrap kernel launches with synchronization during debugging:
```cpp
kernel<<<grid, block>>>(...);
cudaError_t err = cudaGetLastError();
if (err != cudaSuccess) {
    printf("Kernel launch failed: %s\n", cudaGetErrorString(err));
}
cudaDeviceSynchronize();
```

### 2. Array Out-of-Bounds Memory Corruption
- **Symptom**: Random NaNs or corrupted weights in deep neural network layers.
- **Root Cause**: Forgetting the boundary check `if (idx < n)` when input array size $N$ is not an exact multiple of `blockDim.x`.
- **Fix**: Always enforce boundary checks or use grid-stride loops.
