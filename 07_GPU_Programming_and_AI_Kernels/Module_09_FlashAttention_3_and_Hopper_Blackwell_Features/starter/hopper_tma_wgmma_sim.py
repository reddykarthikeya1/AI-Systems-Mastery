"""Starter template for Hopper TMA and WGMMA Simulator."""
from __future__ import annotations

import numpy as np


class HopperTMASimulator:
    """Simulate Hopper Tensor Memory Accelerator (TMA) asynchronous copy."""

    def __init__(self, sram_capacity_kb: int = 228) -> None:
        raise NotImplementedError("Implement HopperTMASimulator.__init__")

    def issue_async_load(self, global_tensor: np.ndarray, tile_coords: tuple[int, int], tile_shape: tuple[int, int]) -> int:
        """Issue async TMA load without tying up SM registers. Returns transaction bytes."""
        raise NotImplementedError("Implement HopperTMASimulator.issue_async_load")


def simulate_ping_pong_gemm_pipeline(
    m: int, n: int, k: int, tile_k: int = 64
) -> dict[str, float]:
    """Simulate overlap efficiency of ping-pong TMA loading and WGMMA compute."""
    raise NotImplementedError("Implement simulate_ping_pong_gemm_pipeline")
