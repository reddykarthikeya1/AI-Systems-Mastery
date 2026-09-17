"""Unit tests for Coalescing and Bank Conflict Simulator."""
from __future__ import annotations

import pytest
from coalescing_and_bank_conflict_sim import (
    detect_shared_memory_bank_conflicts,
    simulate_2d_shared_mem_access,
    simulate_global_memory_access,
)


def test_coalesced_vs_strided_global_access() -> None:
    # 32 contiguous floats (0, 4, 8, ... 124) -> 1 transaction of 128 bytes, 100% efficient
    contiguous = [i * 4 for i in range(32)]
    txs, eff = simulate_global_memory_access(contiguous, cache_line_size=128)
    assert txs == 1
    assert pytest.approx(eff, rel=1e-5) == 1.0

    # Stride-32 floats -> 32 distinct 128-byte cache lines, ~3.125% efficient
    strided = [i * 32 * 4 for i in range(32)]
    txs_strided, eff_strided = simulate_global_memory_access(strided, cache_line_size=128)
    assert txs_strided == 32
    assert pytest.approx(eff_strided, rel=1e-5) == 1.0 / 32.0


def test_shared_memory_bank_conflict_and_broadcast() -> None:
    # 32 threads accessing 32 consecutive 4-byte words -> Bank 0 to 31 -> 1-way (no conflict)
    conflict_free = [i * 4 for i in range(32)]
    conflict_factor, _ = detect_shared_memory_bank_conflicts(conflict_free)
    assert conflict_factor == 1

    # Broadcast: All 32 threads access address 0 -> Broadcast (1-way, no conflict)
    broadcast = [0] * 32
    conflict_factor_bc, _ = detect_shared_memory_bank_conflicts(broadcast)
    assert conflict_factor_bc == 1

    # 32-way conflict: 32 threads accessing different addresses on the same bank
    # e.g., thread i reads (i * 32 * 4) -> all map to bank 0!
    worst_conflict = [i * 32 * 4 for i in range(32)]
    conflict_factor_worst, _ = detect_shared_memory_bank_conflicts(worst_conflict)
    assert conflict_factor_worst == 32


def test_shared_memory_padding_trick() -> None:
    # Without padding: tile[32][32] -> column access has stride 32 -> 32-way bank conflict!
    conflict_unpadded = simulate_2d_shared_mem_access(rows=32, cols=32, stride_cols=32)
    assert conflict_unpadded == 32

    # With padding: tile[32][33] -> column access has stride 33 -> 1-way (0 bank conflicts!)
    conflict_padded = simulate_2d_shared_mem_access(rows=32, cols=32, stride_cols=33)
    assert conflict_padded == 1
