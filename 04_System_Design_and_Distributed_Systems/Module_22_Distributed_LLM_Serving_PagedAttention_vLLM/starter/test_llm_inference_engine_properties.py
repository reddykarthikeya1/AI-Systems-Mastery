"""Property and performance assertions for Distributed LLM Serving & PagedAttention.

These complement the correctness tests in `test_llm_inference_engine.py`. A correctness test says
the operation does the right thing; these say the *claim the module makes about
it* is true - and they fail when it stops being true.

    pytest -m perf -v          # just the performance assertions
    pytest -m "not slow" -q    # skip the long ones
"""

from __future__ import annotations

import pytest
from llm_inference_engine import PagedAttentionBlockManager


def test_freeing_blocks_returns_them_to_the_pool() -> None:
    """Paged allocation is only a win if freed pages are genuinely reusable."""
    manager = PagedAttentionBlockManager(num_gpu_blocks=32, block_size=16)
    start = manager.num_free_blocks()

    manager.ensure_blocks_for_length("req-1", 100)
    assert manager.num_free_blocks() < start

    manager.free_blocks("req-1")
    assert manager.num_free_blocks() == start, "freed blocks were not reclaimed"


@pytest.mark.perf
def test_paged_allocation_wastes_less_than_one_block_per_request() -> None:
    """The claim PagedAttention makes: internal fragmentation is bounded by the
    block size, not by the longest sequence you might ever see.

    Naive contiguous pre-allocation reserves max_seq_len per request and wastes
    everything unused. Here the waste per request must stay under one block.
    """
    block_size = 16
    manager = PagedAttentionBlockManager(num_gpu_blocks=256, block_size=block_size)

    lengths = [10, 33, 47, 5, 100, 61]
    for i, length in enumerate(lengths):
        manager.ensure_blocks_for_length(f"req-{i}", length)

    used_blocks = 256 - manager.num_free_blocks()
    tokens = sum(lengths)
    waste = used_blocks * block_size - tokens

    assert waste < block_size * len(lengths), (
        f"wasted {waste} token slots across {len(lengths)} requests - "
        f"must stay under one block ({block_size}) each."
    )


def test_exhausting_the_pool_is_reported_rather_than_silently_overcommitted() -> None:
    """Overcommitting GPU memory is an OOM kill, not a slowdown."""
    manager = PagedAttentionBlockManager(num_gpu_blocks=4, block_size=16)
    outcomes = [manager.ensure_blocks_for_length(f"r{i}", 64) for i in range(6)]
    assert not all(outcomes), "allocated more blocks than the pool contains"


def test_memory_utilisation_is_reported_within_bounds() -> None:
    manager = PagedAttentionBlockManager(num_gpu_blocks=16, block_size=16)
    assert 0.0 <= manager.get_memory_utilization() <= 1.0
    manager.ensure_blocks_for_length("r", 128)
    assert 0.0 < manager.get_memory_utilization() <= 1.0


def test_longer_sequences_need_proportionally_more_blocks() -> None:
    manager = PagedAttentionBlockManager(num_gpu_blocks=256, block_size=16)
    before = manager.num_free_blocks()
    manager.ensure_blocks_for_length("short", 16)
    after_short = manager.num_free_blocks()
    manager.ensure_blocks_for_length("long", 160)
    after_long = manager.num_free_blocks()

    short_cost = before - after_short
    long_cost = after_short - after_long
    assert long_cost > short_cost
