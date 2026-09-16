from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class KVCacheFootprint:
    bytes_per_token: int
    req_memory_mb: float
    max_concurrent_requests: int
    internal_frag_percent: float


class KVCacheMemoryCalculator:
    """Calculates KV-cache memory requirements and fragmentation metrics."""

    @staticmethod
    def calculate_footprint(
        layers: int,
        kv_heads: int,
        head_dim: int,
        seq_len: int,
        available_vram_gb: float,
        precision_bytes: int = 2,
        static_reserved_len: int | None = None,
    ) -> KVCacheFootprint:
        # Key + Value = 2 tensors
        bytes_per_tok = 2 * precision_bytes * layers * kv_heads * head_dim
        req_bytes = bytes_per_tok * seq_len
        req_mb = req_bytes / (1024**2)

        available_bytes = available_vram_gb * (1024**3)
        max_concurrent = int(available_bytes // req_bytes)

        if static_reserved_len and static_reserved_len > seq_len:
            wasted_tokens = static_reserved_len - seq_len
            frag = (wasted_tokens / static_reserved_len) * 100.0
        else:
            frag = 0.0

        return KVCacheFootprint(
            bytes_per_token=bytes_per_tok,
            req_memory_mb=round(req_mb, 2),
            max_concurrent_requests=max_concurrent,
            internal_frag_percent=round(frag, 2),
        )
