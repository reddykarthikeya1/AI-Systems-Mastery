from __future__ import annotations

from scaling_laws_finops import ChinchillaScalingLaw, MFUCalculator


def test_mfu_calculation_h100():
    # 70B model, 1024 GPUs, 989 peak TFLOPs, 420k tokens/sec
    res = MFUCalculator.calculate_mfu(
        params_b=70.0,
        tokens_per_sec=420_000,
        num_gpus=1024,
        peak_tflops_per_gpu=989.0,
        activation_recompute=False,
    )
    # Expected ~17.4% MFU
    assert 17.0 <= res.mfu_percent <= 18.0
    assert res.is_healthy is False


def test_mfu_healthy_run():
    # 70B model, 1024 GPUs, 989 peak TFLOPs, 1.1M tokens/sec
    res = MFUCalculator.calculate_mfu(
        params_b=70.0,
        tokens_per_sec=1_100_000,
        num_gpus=1024,
        peak_tflops_per_gpu=989.0,
        activation_recompute=False,
    )
    assert res.mfu_percent > 45.0
    assert res.is_healthy is True


def test_chinchilla_scaling_law_ratio():
    budget = 1e24  # 10^24 FLOPs
    alloc = ChinchillaScalingLaw.compute_optimal_allocation(budget)

    # Token to parameter ratio should be approximately 2.7 to 3.0 in raw proportionality
    assert alloc["optimal_params_b"] > 0
    assert alloc["optimal_tokens_b"] > 0
    assert alloc["token_to_param_ratio"] > 2.0
