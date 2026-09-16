"""Production reference implementation for Coalescing and Bank Conflict Simulator."""
from __future__ import annotations

from collections import defaultdict


def simulate_global_memory_access(
    thread_addresses: list[int], cache_line_size: int = 128
) -> tuple[int, float]:
    """Simulate global memory transactions and compute bus efficiency.

    NVIDIA GPU memory controllers fetch memory in aligned cache lines (typically 128B).
    When threads in a warp issue memory addresses:
    - We calculate the unique aligned cache line tags: address // cache_line_size.
    - Each unique cache line requires 1 hardware memory transaction.
    - Bus efficiency = (Total bytes used by threads) / (Total bytes fetched from DRAM).

    Returns:
        tuple of (number_of_transactions, bus_efficiency_ratio).
    """
    if not thread_addresses:
        return 0, 1.0

    # 4 bytes per float address
    bytes_requested = len(thread_addresses) * 4
    unique_cache_lines = set(addr // cache_line_size for addr in thread_addresses)
    num_transactions = len(unique_cache_lines)

    bytes_transferred = num_transactions * cache_line_size
    efficiency = float(bytes_requested) / float(bytes_transferred) if bytes_transferred > 0 else 0.0

    return num_transactions, efficiency


def detect_shared_memory_bank_conflicts(
    thread_byte_addresses: list[int], num_banks: int = 32, word_size: int = 4
) -> tuple[int, dict[int, list[int]]]:
    """Detect shared memory bank conflicts across 32 threads in a warp.

    Shared memory is divided into 32 banks of 4-byte words.
    Bank index = (byte_address // word_size) % num_banks.
    - If multiple threads access the same bank with different addresses: Bank Conflict!
      The hardware serializes the requests (k-way conflict).
    - If multiple threads access the exact same byte address: Broadcast! (0 conflict).

    Returns:
        tuple of (max_serialization_factor, bank_to_threads_map).
    """
    if len(thread_byte_addresses) != 32:
        raise ValueError("Must provide exactly 32 thread memory addresses for warp analysis.")

    bank_to_unique_addrs: dict[int, set[int]] = defaultdict(set)
    bank_to_threads: dict[int, list[int]] = defaultdict(list)

    for thread_id, addr in enumerate(thread_byte_addresses):
        word_idx = addr // word_size
        bank_id = word_idx % num_banks
        bank_to_unique_addrs[bank_id].add(addr)
        bank_to_threads[bank_id].append(thread_id)

    # Serialization factor is the maximum number of distinct addresses hitting any single bank
    max_conflict = max(len(addrs) for addrs in bank_to_unique_addrs.values()) if bank_to_unique_addrs else 1
    return max_conflict, dict(bank_to_threads)


def simulate_2d_shared_mem_access(
    rows: int, cols: int, stride_cols: int, word_size: int = 4
) -> int:
    """Calculate max bank conflict when reading a column in a 2D shared tile.

    In a 2D array tile[rows][stride_cols], reading a column across 32 threads:
    Thread i reads address = (i * stride_cols + target_col) * word_size.
    Returns the serialization factor (1 = conflict-free, 32 = full conflict).
    """
    addrs = [(i * stride_cols + 0) * word_size for i in range(min(32, rows))]
    if len(addrs) < 32:
        addrs.extend([0] * (32 - len(addrs)))

    max_conflict, _ = detect_shared_memory_bank_conflicts(addrs, num_banks=32, word_size=word_size)
    return max_conflict
