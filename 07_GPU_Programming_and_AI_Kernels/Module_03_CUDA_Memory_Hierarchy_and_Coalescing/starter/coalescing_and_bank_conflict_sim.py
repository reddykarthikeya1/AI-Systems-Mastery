"""Starter template for Coalescing and Bank Conflict Simulator."""
from __future__ import annotations


def simulate_global_memory_access(
    thread_addresses: list[int], cache_line_size: int = 128
) -> tuple[int, float]:
    """Simulate global memory transactions and compute bus efficiency.

    Returns:
        tuple of (number_of_transactions, bus_efficiency_ratio).
    """
    raise NotImplementedError("Implement simulate_global_memory_access")


def detect_shared_memory_bank_conflicts(
    thread_byte_addresses: list[int], num_banks: int = 32, word_size: int = 4
) -> tuple[int, dict[int, list[int]]]:
    """Detect shared memory bank conflicts across 32 threads in a warp.

    Returns:
        tuple of (max_serialization_factor, bank_access_distribution).
    """
    raise NotImplementedError("Implement detect_shared_memory_bank_conflicts")


def simulate_2d_shared_mem_access(
    rows: int, cols: int, stride_cols: int, word_size: int = 4
) -> int:
    """Calculate max bank conflict when reading a column in a 2D shared tile."""
    raise NotImplementedError("Implement simulate_2d_shared_mem_access")
