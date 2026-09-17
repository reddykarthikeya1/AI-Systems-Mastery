"""Reference Solution — Problem 01: Kv Cache Footprint Estimator

Topic: 02 KV Cache Memory Management
"""

from __future__ import annotations


def kv_cache_footprint_estimator(num_layers: int, num_kv_heads: int, head_dim: int, context_tokens: int, bytes_per_elem: int = 2) -> int:
    bytes_per_token = 2 * num_layers * num_kv_heads * head_dim * bytes_per_elem
    return bytes_per_token * context_tokens
