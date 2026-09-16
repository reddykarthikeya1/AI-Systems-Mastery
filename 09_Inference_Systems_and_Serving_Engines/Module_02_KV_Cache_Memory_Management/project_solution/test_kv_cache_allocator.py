from __future__ import annotations

from kv_cache_allocator import KVCacheMemoryCalculator


def test_llama3_8b_kv_cache_calculation():
    # Llama 3 8B: 32 layers, 8 KV heads, 128 head_dim, FP16 (2 bytes)
    res = KVCacheMemoryCalculator.calculate_footprint(
        layers=32,
        kv_heads=8,
        head_dim=128,
        seq_len=4096,
        available_vram_gb=20.0,
        precision_bytes=2,
    )
    # Expected bytes per token: 2 * 2 * 32 * 8 * 128 = 131,072 bytes (128 KB)
    assert res.bytes_per_token == 131072
    # 4096 tokens * 128 KB = 512 MB
    assert abs(res.req_memory_mb - 512.0) < 1.0
    # 20 GB / 512 MB = ~40 concurrent requests
    assert res.max_concurrent_requests == 40


def test_static_reservation_internal_fragmentation():
    # Request uses 500 tokens but system reserves static 2048 tokens
    res = KVCacheMemoryCalculator.calculate_footprint(
        layers=32,
        kv_heads=8,
        head_dim=128,
        seq_len=500,
        available_vram_gb=10.0,
        static_reserved_len=2048,
    )
    # (2048 - 500) / 2048 = 75.58% fragmentation
    assert res.internal_frag_percent > 75.0
