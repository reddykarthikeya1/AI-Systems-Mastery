from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class ServingMetrics:
    ttft_ms: float
    tpot_ms: float
    total_time_ms: float
    throughput_tok_per_sec: float
    is_memory_bound_decode: bool


class InferencePerformanceSimulator:
    def __init__(
        self,
        params_b: float,
        gpu_hbm_bw_tb_s: float = 3.35,
        gpu_peak_tflops: float = 989.0,
    ):
        raise NotImplementedError("Implement InferencePerformanceSimulator")

    def simulate_request(
        self,
        prompt_tokens: int,
        gen_tokens: int,
        batch_size: int = 1,
    ) -> ServingMetrics:
        raise NotImplementedError("Implement simulate_request")
