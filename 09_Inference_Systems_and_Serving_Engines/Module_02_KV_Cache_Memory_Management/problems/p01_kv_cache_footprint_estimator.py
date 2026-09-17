"""Problem 01 — Kv Cache Footprint Estimator

Topic: 02 KV Cache Memory Management
Target: Production-grade implementation

Calculate exact byte size of FP16/FP8 KV cache for model architecture and token context.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def kv_cache_footprint_estimator(num_layers: int, num_kv_heads: int, head_dim: int, context_tokens: int, bytes_per_elem: int = 2) -> int:
    """Byte footprint per token: 2 (K and V) * num_layers * num_kv_heads * head_dim * bytes_per_elem.
    Total bytes = footprint_per_token * context_tokens.
    """
    raise NotImplementedError("Implement kv_cache_footprint_estimator")
