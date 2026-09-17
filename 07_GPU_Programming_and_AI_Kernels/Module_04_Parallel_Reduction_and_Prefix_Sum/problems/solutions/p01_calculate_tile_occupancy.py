"""Reference Solution — Problem 01: calculate_tile_occupancy

Topic: Parallel Reduction and Prefix Sum
"""

from __future__ import annotations

def calculate_tile_occupancy(threads_per_block: int, shared_mem_bytes: int, max_sm_threads: int = 2048, max_sm_shared_mem: int = 102400) -> dict[str, float | int]:
    if threads_per_block <= 0 or threads_per_block > 1024 or threads_per_block % 32 != 0:
        return {"active_blocks": 0, "active_warps": 0, "occupancy_percent": 0.0}
    max_blocks_by_threads = max_sm_threads // threads_per_block
    max_blocks_by_shmem = max_sm_shared_mem // shared_mem_bytes if shared_mem_bytes > 0 else 32
    active_blocks = min(max_blocks_by_threads, max_blocks_by_shmem, 32)
    active_warps = active_blocks * (threads_per_block // 32)
    max_warps = max_sm_threads // 32
    occupancy = round((active_warps / max_warps) * 100.0, 2)
    return {"active_blocks": active_blocks, "active_warps": active_warps, "occupancy_percent": occupancy}

