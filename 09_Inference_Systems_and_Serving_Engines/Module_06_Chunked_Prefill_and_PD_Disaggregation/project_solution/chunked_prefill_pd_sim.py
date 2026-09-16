from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class ChunkScheduleResult:
    total_chunks: int
    step_latencies_ms: list[float]
    max_step_latency_ms: float
    total_prefill_time_ms: float


class ChunkedPrefillSimulator:
    """Simulates Sarathi-Serve Chunked Prefill execution and step latency bounding."""

    def __init__(self, chunk_size: int = 512, ms_per_token_prefill: float = 0.05):
        self.chunk_size = chunk_size
        self.ms_per_token = ms_per_token_prefill

    def schedule_prompt(self, prompt_tokens: int, decode_step_overhead_ms: float = 15.0) -> ChunkScheduleResult:
        remaining = prompt_tokens
        step_latencies = []

        while remaining > 0:
            current_chunk = min(remaining, self.chunk_size)
            prefill_time = current_chunk * self.ms_per_token
            step_latency = prefill_time + decode_step_overhead_ms
            step_latencies.append(round(step_latency, 2))
            remaining -= current_chunk

        return ChunkScheduleResult(
            total_chunks=len(step_latencies),
            step_latencies_ms=step_latencies,
            max_step_latency_ms=max(step_latencies),
            total_prefill_time_ms=round(sum(step_latencies) - (len(step_latencies) * decode_step_overhead_ms), 2),
        )
