"""Production reference implementation for GPU Microarchitecture Simulator."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RooflineResult:
    arithmetic_intensity: float
    achieved_tflops: float
    bound_type: str  # "memory_bound" or "compute_bound"


def compute_warp_divergence(predicates: list[bool]) -> tuple[int, list[int]]:
    """Simulate SIMT execution of 32 threads with given boolean predicates.

    In NVIDIA SIMT architecture, a warp consists of 32 threads. When threads
    within the same warp diverge on a conditional branch (e.g. some evaluate True,
    others False), execution is serialized:
    - Pass 1 executes the True path with threads where predicate is True enabled.
    - Pass 2 executes the False path with threads where predicate is False enabled.
    If all 32 threads evaluate to the same branch (all True or all False),
    there is only 1 pass with no divergence penalty.

    Returns:
        tuple of (number_of_passes, list_of_active_masks_per_pass).
    """
    if len(predicates) != 32:
        raise ValueError("A warp must contain exactly 32 thread predicates.")

    true_count = sum(1 for p in predicates if p)
    false_count = 32 - true_count

    if true_count == 32:
        # Uniform True path
        return 1, [0xFFFFFFFF]
    if false_count == 32:
        # Uniform False path
        return 1, [0xFFFFFFFF]

    # Divergent warp: requires 2 serialized execution passes
    mask_true = 0
    mask_false = 0
    for idx, p in enumerate(predicates):
        if p:
            mask_true |= (1 << idx)
        else:
            mask_false |= (1 << idx)

    return 2, [mask_true, mask_false]


def calculate_arithmetic_intensity(flops: int, memory_bytes: int) -> float:
    """Calculate arithmetic intensity in FLOPs per Byte.

    Arithmetic Intensity = Operations / Memory Traffic (Bytes).
    """
    if memory_bytes <= 0:
        raise ValueError("Memory bytes must be strictly positive.")
    return float(flops) / float(memory_bytes)


def evaluate_roofline(
    peak_tflops: float, peak_bandwidth_gbs: float, arithmetic_intensity: float
) -> RooflineResult:
    """Evaluate performance bound using the Roofline model.

    Peak attainable performance P = min(P_peak, I * B_peak).
    Ridge point I_ridge = P_peak / B_peak.
    - If I < I_ridge: Kernel is Memory-Bound (limited by memory bandwidth).
    - If I >= I_ridge: Kernel is Compute-Bound (limited by ALU/Tensor Core peak).
    """
    bandwidth_tflops_limit = (arithmetic_intensity * peak_bandwidth_gbs) / 1000.0
    achieved = min(peak_tflops, bandwidth_tflops_limit)

    ridge_point = (peak_tflops * 1000.0) / peak_bandwidth_gbs
    bound_type = "memory_bound" if arithmetic_intensity < ridge_point else "compute_bound"

    return RooflineResult(
        arithmetic_intensity=arithmetic_intensity,
        achieved_tflops=achieved,
        bound_type=bound_type,
    )


def calculate_sm_occupancy(
    threads_per_block: int,
    regs_per_thread: int,
    shared_mem_per_block_bytes: int,
    max_regs_per_sm: int = 65536,
    max_shared_mem_per_sm: int = 102400,
    max_warps_per_sm: int = 64,
) -> float:
    """Calculate SM theoretical occupancy (ratio of active warps to max warps).

    Hardware limits:
    - Thread limit (warps per block = ceil(threads_per_block / 32))
    - Register limit (regs per warp * warps per block)
    - Shared memory limit (shared memory per block)
    """
    if threads_per_block <= 0 or regs_per_thread < 0:
        raise ValueError("Invalid block parameters.")

    warps_per_block = (threads_per_block + 31) // 32
    regs_per_block = threads_per_block * regs_per_thread

    # Limit by registers
    blocks_by_regs = max_regs_per_sm // regs_per_block if regs_per_block > 0 else 32

    # Limit by shared memory
    blocks_by_smem = (
        max_shared_mem_per_sm // shared_mem_per_block_bytes
        if shared_mem_per_block_bytes > 0
        else 32
    )

    # Max blocks per SM on modern architectures is typically 32
    active_blocks = max(0, min(32, blocks_by_regs, blocks_by_smem))
    active_warps = min(max_warps_per_sm, active_blocks * warps_per_block)

    return float(active_warps) / float(max_warps_per_sm)
