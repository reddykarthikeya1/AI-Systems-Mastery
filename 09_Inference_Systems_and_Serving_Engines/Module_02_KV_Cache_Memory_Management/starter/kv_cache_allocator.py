from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class KVCacheFootprint:
    bytes_per_token: int
    req_memory_mb: float
    max_concurrent_requests: int
    internal_frag_percent: float


class KVCacheMemoryCalculator:
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
        raise NotImplementedError("Implement calculate_footprint")
