"""Production reference implementation for Parallel Reduction and Scan Engine."""
from __future__ import annotations

import numpy as np


def warp_shuffle_down_reduce(vals: list[float]) -> float:
    """Simulate __shfl_down_sync tree reduction within a 32-thread warp.

    In hardware, 32 threads in a warp exchange register values directly using:
    for offset in [16, 8, 4, 2, 1]:
        val += __shfl_down_sync(0xffffffff, val, offset)
    Thread 0 holds the final sum.
    """
    if len(vals) != 32:
        raise ValueError("Warp reduction requires exactly 32 thread values.")

    regs = list(vals)
    for offset in [16, 8, 4, 2, 1]:
        new_regs = list(regs)
        for t in range(32):
            if t + offset < 32:
                new_regs[t] += regs[t + offset]
        regs = new_regs

    return float(regs[0])


def block_tree_reduce(arr: np.ndarray, block_size: int = 256) -> float:
    """Simulate block reduction using sequential addressing.

    Sequential addressing halves active threads each step (s = block_size // 2, ... 1),
    ensuring zero warp divergence until s < 32.
    """
    if arr.size == 0:
        return 0.0

    # Pad array to multiple of block_size
    n = arr.size
    pad_len = (block_size - (n % block_size)) % block_size
    padded = np.pad(arr, (0, pad_len), mode="constant", constant_values=0.0)

    # Reduce within each block
    num_blocks = padded.size // block_size
    block_sums = np.zeros(num_blocks, dtype=np.float64)

    for b in range(num_blocks):
        sdata = padded[b * block_size : (b + 1) * block_size].copy()
        s = block_size // 2
        while s > 0:
            sdata[:s] += sdata[s : 2 * s]
            s //= 2
        block_sums[b] = sdata[0]

    return float(np.sum(block_sums))


def blelloch_scan_exclusive(arr: np.ndarray) -> np.ndarray:
    """Compute exclusive parallel prefix sum (first element is 0).

    Blelloch algorithm operates on power-of-two arrays in two passes:
    1. Up-Sweep (reduce): computes tree sums.
    2. Down-Sweep (distribute): sets root to 0 and propagates sums down.
    """
    n = arr.size
    if n == 0:
        return np.array([], dtype=arr.dtype)

    # Next power of 2
    p2 = 1
    while p2 < n:
        p2 *= 2

    tree = np.zeros(p2, dtype=np.float64)
    tree[:n] = arr

    # 1. Up-Sweep
    step = 1
    while step < p2:
        for i in range(2 * step - 1, p2, 2 * step):
            tree[i] += tree[i - step]
        step *= 2

    # Set root to zero
    tree[p2 - 1] = 0.0

    # 2. Down-Sweep
    step = p2 // 2
    while step > 0:
        for i in range(2 * step - 1, p2, 2 * step):
            t = tree[i - step]
            tree[i - step] = tree[i]
            tree[i] += t
        step //= 2

    return tree[:n]


def blelloch_scan_inclusive(arr: np.ndarray) -> np.ndarray:
    """Compute inclusive parallel prefix sum.

    Inclusive scan = exclusive scan + original array.
    """
    if arr.size == 0:
        return np.array([], dtype=arr.dtype)

    exclusive = blelloch_scan_exclusive(arr)
    return exclusive + arr
