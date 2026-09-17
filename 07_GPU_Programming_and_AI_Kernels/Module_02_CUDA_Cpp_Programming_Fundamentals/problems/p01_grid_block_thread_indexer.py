"""Problem 01 — Grid Block Thread Indexer

Topic: 02 CUDA Cpp Programming Fundamentals
Target: Production-grade implementation

Compute 1D global memory offset from CUDA blockIdx, blockDim, and threadIdx.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def grid_block_thread_indexer(block_idx: int, block_dim: int, thread_idx: int) -> int:
    """CUDA 1D global index: i = block_idx * block_dim + thread_idx."""
    raise NotImplementedError("Implement grid_block_thread_indexer")
