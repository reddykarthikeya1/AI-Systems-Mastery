"""Production reference implementation for Hopper TMA and WGMMA Simulator."""
from __future__ import annotations

import numpy as np


class HopperTMASimulator:
    """Simulate Hopper Tensor Memory Accelerator (TMA) asynchronous copy.

    TMA executes multi-dimensional tensor transfers between HBM and Shared Memory
    without consuming thread registers or instruction issue slots.
    """

    def __init__(self, sram_capacity_kb: int = 228) -> None:
        self.capacity_bytes = sram_capacity_kb * 1024
        self.allocated_bytes = 0
        self.total_transactions_bytes = 0

    def issue_async_load(
        self,
        global_tensor: np.ndarray,
        tile_coords: tuple[int, int],
        tile_shape: tuple[int, int],
    ) -> int:
        """Issue async TMA load of a 2D tile.

        Returns the number of bytes transferred asynchronously.
        """
        r_start, c_start = tile_coords
        th, tw = tile_shape

        tile = global_tensor[r_start : r_start + th, c_start : c_start + tw]
        tile_bytes = tile.nbytes

        if self.allocated_bytes + tile_bytes > self.capacity_bytes:
            raise MemoryError("SRAM capacity exceeded.")

        self.allocated_bytes += tile_bytes
        self.total_transactions_bytes += tile_bytes
        return tile_bytes

    def release_tile(self, tile_bytes: int) -> None:
        """Release shared memory allocation after compute consumption."""
        self.allocated_bytes = max(0, self.allocated_bytes - tile_bytes)


def simulate_ping_pong_gemm_pipeline(
    m: int, n: int, k: int, tile_k: int = 64
) -> dict[str, float]:
    """Simulate overlap efficiency of ping-pong TMA loading and WGMMA compute.

    In a 2-stage ping-pong pipeline:
    - Stage A: Warpgroup 0 computes WGMMA on Buffer 0.
    - Stage B: TMA asynchronously fills Buffer 1.
    If compute_time >= transfer_time, memory latency is 100% hidden.
    """
    num_phases = (k + tile_k - 1) // tile_k

    # Estimated times in arbitrary microsecond units
    # Transfer time = bytes / bandwidth
    tile_bytes = (m * tile_k + tile_k * n) * 2  # FP16 = 2 bytes
    tma_transfer_time_us = tile_bytes / 3000.0  # ~3 TB/s HBM3
    wgmma_compute_time_us = (2.0 * m * n * tile_k) / (1000.0 * 1000.0)  # ~1 PFLOPs FP8/FP16 tensor core

    sequential_time = num_phases * (tma_transfer_time_us + wgmma_compute_time_us)
    # Pipelined time = first load + phases * max(compute, transfer)
    pipelined_time = tma_transfer_time_us + num_phases * max(tma_transfer_time_us, wgmma_compute_time_us)

    overlap_efficiency = sequential_time / pipelined_time if pipelined_time > 0 else 1.0

    return {
        "num_phases": float(num_phases),
        "sequential_time_us": sequential_time,
        "pipelined_time_us": pipelined_time,
        "speedup_factor": overlap_efficiency,
        "latency_hidden": float(wgmma_compute_time_us >= tma_transfer_time_us),
    }
