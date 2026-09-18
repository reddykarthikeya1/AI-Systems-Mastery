"""Problem 01 — Grid Block Thread Indexer

Topic: 02 CUDA Cpp Programming Fundamentals
Target: Production-grade implementation

Compute 1D global memory offset from CUDA blockIdx, blockDim, and threadIdx.

Example:
    >>> grid_block_thread_indexer(2, 256, 10)
    522

Hints:
    Hint 1: A thread's global position is just its block's starting offset
        in the grid plus its own local position inside that block.
    Hint 2: Multiply `block_idx` by `block_dim` to get the block's starting
        offset, then add `thread_idx`.
    Hint 3: This is a single multiply-add with no clamping or wraparound —
        `thread_idx` is assumed to already lie within `[0, block_dim)`, so
        there is no edge case to special-case here.
"""

from __future__ import annotations


def grid_block_thread_indexer(block_idx: int, block_dim: int, thread_idx: int) -> int:
    """CUDA 1D global index: i = block_idx * block_dim + thread_idx."""
    raise NotImplementedError("Implement grid_block_thread_indexer")
