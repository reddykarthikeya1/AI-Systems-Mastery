"""Unit tests for Tensor-Parallel KV Allocator and CUDA Graph Simulator."""

from __future__ import annotations

import pytest
from tp_kv_cache_allocator import CUDAGraphReplaySimulator, TensorParallelKVAllocator


def test_tp_kv_slicing():
    allocator = TensorParallelKVAllocator(total_kv_heads=8, head_dim=128, num_layers=80, tp_size=8)
    shards = allocator.allocate_sequence(seq_len=2048, dtype_bytes=2)

    assert len(shards) == 8
    assert shards[0].num_kv_heads == 1
    assert shards[0].allocated_bytes == shards[7].allocated_bytes


def test_cuda_graph_replay():
    graph = CUDAGraphReplaySimulator(max_batch_size=32)
    with pytest.raises(RuntimeError):
        graph.replay_step(16)

    graph.capture_graph()
    overhead_us = graph.replay_step(16)
    assert overhead_us < 5.0
