# Diagnosis and Fix

## Root Cause
In standard transformer training without activation recomputation, each token requires $2N$ FLOPs for forward and $4N$ FLOPs for backward (total $6N$ FLOPs per token). Using $2N$ undercounts computational work and produces nonsensical MFU figures.

## Correct Implementation
```python
def calculate_mfu(num_params: int, tokens_per_sec: float, peak_tflops: float) -> float:
    flops_per_sec = 6.0 * num_params * tokens_per_sec
    return (flops_per_sec / (peak_tflops * 1e12)) * 100.0
```
