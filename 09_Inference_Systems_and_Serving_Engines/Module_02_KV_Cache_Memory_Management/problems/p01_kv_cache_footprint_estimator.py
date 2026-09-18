"""Problem 01 — Kv Cache Footprint Estimator

Topic: 02 KV Cache Memory Management
Target: Production-grade implementation

Calculate exact byte size of FP16/FP8 KV cache for model architecture and token context.

Example:
    >>> kv_cache_footprint_estimator(32, 8, 128, 4096, 2)
    536870912

Hints:
    Hint 1: Every cached token stores both a Key vector and a Value vector
        per layer, so the per-token cost is doubled before anything else is
        multiplied in.
    Hint 2: This is pure arithmetic, no loop needed: compute
        `bytes_per_token = 2 * num_layers * num_kv_heads * head_dim *
        bytes_per_elem`, then multiply by `context_tokens` for the total.
    Hint 3: Use `num_kv_heads`, not a full query-head count — GQA/MQA models
        share fewer KV heads than query heads — and respect `bytes_per_elem`
        as given (2 for FP16, 1 for FP8) rather than hardcoding a dtype size.
"""

from __future__ import annotations


def kv_cache_footprint_estimator(num_layers: int, num_kv_heads: int, head_dim: int, context_tokens: int, bytes_per_elem: int = 2) -> int:
    """Byte footprint per token: 2 (K and V) * num_layers * num_kv_heads * head_dim * bytes_per_elem.
    Total bytes = footprint_per_token * context_tokens.
    """
    raise NotImplementedError("Implement kv_cache_footprint_estimator")
