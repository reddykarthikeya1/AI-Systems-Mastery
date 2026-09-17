"""Reference Solution — Problem 01: compute_attention_budget

Topic: Transformers
"""

from __future__ import annotations

def compute_attention_budget(seq_len: int, num_heads: int, head_dim: int, batch_size: int = 1) -> dict[str, int]:
    # Memory in bytes for KV cache (FP16: 2 bytes, K + V = 2)
    bytes_per_token = 2 * 2 * num_heads * head_dim
    kv_cache_bytes = batch_size * seq_len * bytes_per_token
    # Attention QK^T + AV FLOPs: 4 * b * h * s^2 * d
    flop_count = 4 * batch_size * num_heads * (seq_len ** 2) * head_dim
    return {"kv_cache_bytes": kv_cache_bytes, "attn_flops": flop_count}

