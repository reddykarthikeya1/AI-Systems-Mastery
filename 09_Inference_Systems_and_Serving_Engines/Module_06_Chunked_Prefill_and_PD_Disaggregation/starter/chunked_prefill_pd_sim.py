from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class ChunkScheduleResult:
    total_chunks: int
    step_latencies_ms: list[float]
    max_step_latency_ms: float
    total_prefill_time_ms: float


class ChunkedPrefillSimulator:
    def __init__(self, chunk_size: int = 512, ms_per_token_prefill: float = 0.05):
        raise NotImplementedError("Implement ChunkedPrefillSimulator")

    def schedule_prompt(self, prompt_tokens: int, decode_step_overhead_ms: float = 15.0) -> ChunkScheduleResult:
        raise NotImplementedError("Implement schedule_prompt")
