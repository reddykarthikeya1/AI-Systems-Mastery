# Diagnosis and Fix

## Root Cause
In `ring_shift`, `(rank - step)` was not wrapped with modulo `world_size`, causing negative indices or IndexError when stepping around the ring.

## Correct Implementation
```python
def ring_shift(kv_blocks: list[int], step: int, rank: int, world_size: int) -> int:
    source_rank = (rank - step) % world_size
    return kv_blocks[source_rank]
```
