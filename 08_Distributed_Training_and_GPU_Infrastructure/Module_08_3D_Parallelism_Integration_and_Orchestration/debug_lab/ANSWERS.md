# Diagnosis and Fix

## Root Cause
Megatron 3D coordinates must assign consecutive ranks to the lowest dimension (Tensor Parallelism) across high-speed NVLink intra-node, followed by Data Parallelism, and Pipeline Parallelism across inter-node InfiniBand.

## Correct Implementation
```python
def get_3d_coordinates(global_rank: int, dp_size: int, pp_size: int, tp_size: int):
    tp_id = global_rank % tp_size
    dp_id = (global_rank // tp_size) % dp_size
    pp_id = global_rank // (tp_size * dp_size)
    return (dp_id, pp_id, tp_id)
```
