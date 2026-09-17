from __future__ import annotations

from inference_metrics_sim import InferencePerformanceSimulator


def test_decode_is_memory_bound_for_batch_1():
    # 70B model on single H100
    sim = InferencePerformanceSimulator(params_b=70.0, gpu_hbm_bw_tb_s=3.35, gpu_peak_tflops=989.0)
    res = sim.simulate_request(prompt_tokens=512, gen_tokens=64, batch_size=1)

    # Decode must be memory-bound at batch size 1
    assert res.is_memory_bound_decode is True
    # TPOT must be at least weight streaming time: 140GB / 3350 GB/s = ~41.8ms
    assert res.tpot_ms >= 40.0


def test_throughput_increases_with_batch_size():
    sim = InferencePerformanceSimulator(params_b=8.0, gpu_hbm_bw_tb_s=3.35, gpu_peak_tflops=989.0)
    res_b1 = sim.simulate_request(prompt_tokens=256, gen_tokens=64, batch_size=1)
    res_b8 = sim.simulate_request(prompt_tokens=256, gen_tokens=64, batch_size=8)

    # Batch 8 throughput should be substantially higher than Batch 1
    assert res_b8.throughput_tok_per_sec > (res_b1.throughput_tok_per_sec * 3.0)
