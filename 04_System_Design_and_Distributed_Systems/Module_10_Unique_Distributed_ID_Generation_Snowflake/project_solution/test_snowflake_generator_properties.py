"""Property and performance assertions for Distributed Unique ID Generation.

These complement the correctness tests in `test_snowflake_generator.py`. A correctness test says
the operation does the right thing; these say the *claim the module makes about
it* is true - and they fail when it stops being true.

    pytest -m perf -v          # just the performance assertions
    pytest -m "not slow" -q    # skip the long ones
"""

from __future__ import annotations

import concurrent.futures
import time

import pytest
from snowflake_generator import SnowflakeGenerator


@pytest.mark.concurrency
@pytest.mark.slow
def test_ids_stay_unique_under_concurrent_generation() -> None:
    """Coordination-free uniqueness is the entire promise. Hammer it."""
    gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)

    def batch() -> list[int]:
        return [gen.next_id() for _ in range(500)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        ids = [i for f in [pool.submit(batch) for _ in range(8)] for i in f.result()]

    assert len(ids) == 4000
    assert len(set(ids)) == 4000, f"{4000 - len(set(ids))} duplicate IDs under concurrency"


def test_ids_are_monotonically_increasing() -> None:
    """Sortable IDs give index locality for free - but only if they sort."""
    gen = SnowflakeGenerator(datacenter_id=1, worker_id=2)
    ids = [gen.next_id() for _ in range(2000)]
    assert ids == sorted(ids), "IDs are not monotonic; index locality is lost"


def test_different_workers_never_collide_in_the_same_millisecond() -> None:
    """The worker field is what removes the need for coordination."""
    a = SnowflakeGenerator(datacenter_id=1, worker_id=1)
    b = SnowflakeGenerator(datacenter_id=1, worker_id=2)
    ids = {a.next_id() for _ in range(500)} | {b.next_id() for _ in range(500)}
    assert len(ids) == 1000


def test_parse_round_trips_the_component_fields() -> None:
    gen = SnowflakeGenerator(datacenter_id=3, worker_id=9)
    parsed = gen.parse_id(gen.next_id())
    assert parsed.datacenter_id == 3
    assert parsed.worker_id == 9


@pytest.mark.perf
def test_generation_throughput_is_high_enough_to_be_useful() -> None:
    """An ID generator that cannot outrun your request rate is a bottleneck."""
    gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)
    n = 20_000
    start = time.perf_counter()
    for _ in range(n):
        gen.next_id()
    per_second = n / (time.perf_counter() - start)
    assert per_second > 50_000, f"only {per_second:,.0f} IDs/sec"


def test_invalid_worker_ids_are_rejected() -> None:
    """The field is a fixed bit width; an out-of-range id would silently wrap."""
    with pytest.raises((ValueError, AssertionError)):
        SnowflakeGenerator(datacenter_id=1, worker_id=10_000)
