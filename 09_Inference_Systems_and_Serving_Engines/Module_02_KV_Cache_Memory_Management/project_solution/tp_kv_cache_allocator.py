"""Multi-GPU Tensor-Parallel KV-Cache Allocator and CUDA Graph Capture Simulator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class TPKVCacheShard:
    rank: int
    num_kv_heads: int
    head_dim: int
    allocated_bytes: int


class TensorParallelKVAllocator:
    """Manages KV-Cache memory distribution across Tensor Parallel (TP) GPU ranks."""

    def __init__(self, total_kv_heads: int, head_dim: int, num_layers: int, tp_size: int = 8) -> None:
        assert total_kv_heads % tp_size == 0, f"KV heads ({total_kv_heads}) must divide tp_size ({tp_size})"
        self.tp_size = tp_size
        self.total_kv_heads = total_kv_heads
        self.heads_per_rank = total_kv_heads // tp_size
        self.head_dim = head_dim
        self.num_layers = num_layers

    def allocate_sequence(self, seq_len: int, dtype_bytes: int = 2) -> Dict[int, TPKVCacheShard]:
        """Calculates per-GPU shard allocation for a sequence (K and V tensors)."""
        bytes_per_gpu = 2 * self.num_layers * self.heads_per_rank * seq_len * self.head_dim * dtype_bytes

        shards = {}
        for rank in range(self.tp_size):
            shards[rank] = TPKVCacheShard(
                rank=rank,
                num_kv_heads=self.heads_per_rank,
                head_dim=self.head_dim,
                allocated_bytes=bytes_per_gpu,
            )
        return shards


class CUDAGraphReplaySimulator:
    """Simulates CUDA Graph capture and zero-overhead memory replay during decoding."""

    def __init__(self, max_batch_size: int) -> None:
        self.max_batch_size = max_batch_size
        self.is_captured = False
        self.static_buffer_slots: List[int] = []

    def capture_graph(self) -> None:
        self.static_buffer_slots = [0] * self.max_batch_size
        self.is_captured = True

    def replay_step(self, active_batch: int) -> float:
        """Simulates decoding step; returns execution overhead in microseconds."""
        if not self.is_captured:
            raise RuntimeError("Cannot replay uncaptured CUDA Graph.")
        if active_batch > self.max_batch_size:
            raise ValueError("Batch exceeds captured graph capacity.")
        return 3.5
