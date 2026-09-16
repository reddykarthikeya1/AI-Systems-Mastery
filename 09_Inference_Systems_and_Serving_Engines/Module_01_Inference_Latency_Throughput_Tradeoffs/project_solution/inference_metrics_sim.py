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
    """Simulates LLM inference latency, throughput, and roofline regimes."""

    def __init__(
        self,
        params_b: float,
        gpu_hbm_bw_tb_s: float = 3.35,  # H100 default: 3.35 TB/s
        gpu_peak_tflops: float = 989.0,  # H100 BF16: 989 TFLOPs
    ):
        self.params_b = params_b
        self.weight_bytes = params_b * 1e9 * 2.0  # FP16/BF16
        self.hbm_bw_bytes_sec = gpu_hbm_bw_tb_s * 1e12
        self.peak_flops_sec = gpu_peak_tflops * 1e12

    def simulate_request(
        self,
        prompt_tokens: int,
        gen_tokens: int,
        batch_size: int = 1,
    ) -> ServingMetrics:
        # Phase 1: Prefill (Compute-Bound)
        # FLOPs = 2 * params * tokens
        prefill_flops = 2.0 * (self.params_b * 1e9) * prompt_tokens * batch_size
        prefill_compute_time = prefill_flops / self.peak_flops_sec
        # Memory transfer for weights in prefill
        prefill_mem_time = self.weight_bytes / self.hbm_bw_bytes_sec
        # Prefill execution time is dominated by max(compute, mem) + kernel overhead
        t_prefill_sec = max(prefill_compute_time, prefill_mem_time) + 0.002
        ttft_ms = t_prefill_sec * 1000.0

        # Phase 2: Decode (Memory-Bandwidth Bound for small batch sizes)
        # In decode, for each generated token, we stream all weights once for the batch
        decode_flops_per_tok = 2.0 * (self.params_b * 1e9) * batch_size
        decode_compute_time_tok = decode_flops_per_tok / self.peak_flops_sec
        decode_mem_time_tok = self.weight_bytes / self.hbm_bw_bytes_sec

        is_mem_bound = decode_mem_time_tok > decode_compute_time_tok
        t_step_sec = max(decode_compute_time_tok, decode_mem_time_tok) + 0.0005
        tpot_ms = t_step_sec * 1000.0

        total_decode_sec = t_step_sec * gen_tokens
        total_time_ms = (t_prefill_sec + total_decode_sec) * 1000.0

        total_tokens = (prompt_tokens + gen_tokens) * batch_size
        throughput = total_tokens / (t_prefill_sec + total_decode_sec)

        return ServingMetrics(
            ttft_ms=round(ttft_ms, 2),
            tpot_ms=round(tpot_ms, 2),
            total_time_ms=round(total_time_ms, 2),
            throughput_tok_per_sec=round(throughput, 2),
            is_memory_bound_decode=is_mem_bound,
        )
