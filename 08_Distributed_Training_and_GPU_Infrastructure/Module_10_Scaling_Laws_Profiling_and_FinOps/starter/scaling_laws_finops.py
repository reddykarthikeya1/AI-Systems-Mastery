from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class MFUResult:
    mfu_percent: float
    effective_tflops: float
    total_peak_tflops: float
    is_healthy: bool


class MFUCalculator:
    @staticmethod
    def calculate_mfu(
        params_b: float,
        tokens_per_sec: float,
        num_gpus: int,
        peak_tflops_per_gpu: float,
        activation_recompute: bool = False,
    ) -> MFUResult:
        raise NotImplementedError("Implement calculate_mfu")


class ChinchillaScalingLaw:
    @staticmethod
    def compute_optimal_allocation(flop_budget: float) -> dict[str, float]:
        raise NotImplementedError("Implement compute_optimal_allocation")
