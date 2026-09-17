"""Unit tests for Twitter Snowflake Distributed ID Generator."""

from __future__ import annotations

import concurrent.futures

import pytest
from snowflake_generator import (
    ClockMovedBackwardsError,
    SnowflakeGenerator,
)


def test_snowflake_id_monotonicity() -> None:
    gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)
    ids = [gen.next_id() for _ in range(100)]

    # Strictly increasing order
    for i in range(len(ids) - 1):
        assert ids[i] < ids[i + 1]


def test_snowflake_bit_packing_and_parsing() -> None:
    gen = SnowflakeGenerator(datacenter_id=7, worker_id=15)
    raw_id = gen.next_id()

    parsed = gen.parse_id(raw_id)
    assert parsed.id == raw_id
    assert parsed.datacenter_id == 7
    assert parsed.worker_id == 15
    assert parsed.sequence >= 0
    assert parsed.timestamp_ms > gen.epoch


def test_concurrent_id_uniqueness_across_threads() -> None:
    gen = SnowflakeGenerator(datacenter_id=2, worker_id=4)
    total_ids = 5000

    def generate_batch(count: int) -> list[int]:
        return [gen.next_id() for _ in range(count)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(generate_batch, 625) for _ in range(8)]
        all_ids = []
        for f in concurrent.futures.as_completed(futures):
            all_ids.extend(f.result())

    # Every single ID generated must be strictly unique!
    assert len(all_ids) == total_ids
    assert len(set(all_ids)) == total_ids


def test_clock_backwards_movement_raises_exception() -> None:
    gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)
    gen.next_id()

    # Artificially set _last_timestamp into the future to simulate NTP clock rollback
    gen._last_timestamp = gen._current_timestamp_ms() + 5000

    with pytest.raises(ClockMovedBackwardsError, match="Clock moved backwards"):
        gen.next_id()


def test_invalid_worker_or_datacenter_bounds() -> None:
    with pytest.raises(ValueError, match="datacenter_id must be between 0 and 31"):
        SnowflakeGenerator(datacenter_id=32, worker_id=1)

    with pytest.raises(ValueError, match="worker_id must be between 0 and 31"):
        SnowflakeGenerator(datacenter_id=1, worker_id=-1)
