"""Course 09 Quickstart: Interactive Inference Systems & KV-Cache Slicing Demo."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "Module_02_KV_Cache_Memory_Management" / "project_solution"))
from tp_kv_cache_allocator import CUDAGraphReplaySimulator, TensorParallelKVAllocator


def run_demo() -> None:
    print("=" * 70)
    print(" COURSE 09: AI INFERENCE SYSTEMS & SERVING ENGINES QUICKSTART")
    print("=" * 70)

    print("\n[1] Multi-GPU Tensor Parallel KV-Cache Slicing (LLaMA-3-70B):")
    # LLaMA-3-70B has 8 KV heads in Grouped-Query Attention (GQA), 80 layers, head_dim 128
    allocator = TensorParallelKVAllocator(total_kv_heads=8, head_dim=128, num_layers=80, tp_size=8)
    shards = allocator.allocate_sequence(seq_len=4096, dtype_bytes=2)

    total_bytes = sum(s.allocated_bytes for s in shards.values())
    print("     * Sequence Length: 4,096 tokens (FP16)")
    print(f"     * Total KV-Cache Across Cluster: {total_bytes / (1024**2):.2f} MB")
    print(f"     * Per-GPU Shard Memory: {shards[0].allocated_bytes / (1024**2):.2f} MB ({shards[0].num_kv_heads} head/GPU)")

    print("\n[2] CUDA Graph Execution Replay Acceleration:")
    graph = CUDAGraphReplaySimulator(max_batch_size=64)
    graph.capture_graph()
    overhead_us = graph.replay_step(active_batch=32)
    print("     * Static Decoding Batch Size: 32")
    print("     * Standard CPU Launch Latency: ~35.00 us")
    print(f"     * CUDA Graph Replay Latency:   ~{overhead_us:.2f} us (Zero-overhead kernel launch!)")

    print("\n" + "=" * 70)
    print(" QUICKSTART DEMO COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
