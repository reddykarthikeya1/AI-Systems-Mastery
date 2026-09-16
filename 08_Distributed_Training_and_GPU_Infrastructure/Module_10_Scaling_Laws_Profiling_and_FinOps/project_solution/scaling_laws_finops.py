from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class MFUResult:
    mfu_percent: float
    effective_tflops: float
    total_peak_tflops: float
    is_healthy: bool


class MFUCalculator:
    """Calculates exact Model FLOPs Utilization (MFU) for distributed training clusters."""

    @staticmethod
    def calculate_mfu(
        params_b: float,
        tokens_per_sec: float,
        num_gpus: int,
        peak_tflops_per_gpu: float,
        activation_recompute: bool = False,
    ) -> MFUResult:
        phi = params_b * 1e9
        # 6 * phi for standard forward+backward, 8 * phi if recomputing activations
        factor = 8.0 if activation_recompute else 6.0

        achieved_flops = factor * phi * tokens_per_sec
        achieved_tflops = achieved_flops / 1e12

        total_peak_tflops = num_gpus * peak_tflops_per_gpu
        mfu = (achieved_tflops / total_peak_tflops) * 100.0

        return MFUResult(
            mfu_percent=round(mfu, 2),
            effective_tflops=round(achieved_tflops, 2),
            total_peak_tflops=round(total_peak_tflops, 2),
            is_healthy=mfu >= 35.0,
        )


class ChinchillaScalingLaw:
    """Computes compute-optimal parameter and token allocations (Hoffmann et al., 2022)."""

    @staticmethod
    def compute_optimal_allocation(flop_budget: float) -> dict[str, float]:
        # C = 6 * N * D
        # N* proportional to C^0.45, D* proportional to C^0.55
        # Calibrated constants: N_opt ~ 0.6 * sqrt(C / 6), D_opt ~ 1.66 * sqrt(C / 6)
        c_norm = flop_budget / 6.0
        n_opt = 0.6 * (c_norm**0.5)
        d_opt = 1.66 * (c_norm**0.5)

        return {
            "flop_budget": flop_budget,
            "optimal_params_b": round(n_opt / 1e9, 2),
            "optimal_tokens_b": round(d_opt / 1e9, 2),
            "token_to_param_ratio": round(d_opt / n_opt, 2),
        }
