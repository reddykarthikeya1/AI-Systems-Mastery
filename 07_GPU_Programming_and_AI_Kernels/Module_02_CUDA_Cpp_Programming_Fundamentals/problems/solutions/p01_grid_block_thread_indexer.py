"""Reference Solution — Problem 01: Grid Block Thread Indexer

Topic: 02 CUDA Cpp Programming Fundamentals
"""

from __future__ import annotations


def grid_block_thread_indexer(block_idx: int, block_dim: int, thread_idx: int) -> int:
    return block_idx * block_dim + thread_idx
