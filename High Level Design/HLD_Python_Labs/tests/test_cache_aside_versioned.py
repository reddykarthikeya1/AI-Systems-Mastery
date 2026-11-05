"""Tests for Versioned Cache-Aside, Generation Fence, and Dogpile SingleFlight (Chapter 03)."""
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import pytest
from ch03_caching.cache_aside_versioned import (
    VersionedCacheAside,
    SingleFlight,
    SimulatedDatabase,
)


def test_cache_aside_basic_flow():
    db = SimulatedDatabase()
    db.write("user:1", {"name": "Alice"})

    cache = VersionedCacheAside(db)

    # First access: cache miss -> DB read
    val = cache.get("user:1")
    assert val == {"name": "Alice"}
    assert cache.cache_misses == 1
    assert cache.cache_hits == 0

    # Second access: cache hit
    val2 = cache.get("user:1")
    assert val2 == {"name": "Alice"}
    assert cache.cache_hits == 1
    assert db.read_count == 1  # No extra DB hit


def test_stale_fill_race_prevention():
    """Simulates:

    1. Reader 1 reads version 1 from DB.
    2. Writer updates DB to version 2 and updates cache.
    3. Reader 1 attempts to write version 1 into cache.
    Expected: Lua version check rejects Reader 1's stale write!
    """
    db = SimulatedDatabase()
    db.write("prod:42", {"price": 100})  # version 1

    cache = VersionedCacheAside(db)

    # 1. Reader 1 reads DB at v1
    data_v1, ver_1 = db.read("prod:42")
    assert ver_1 == 1

    # 2. Writer updates DB to v2 and updates cache
    cache.update("prod:42", {"price": 150})  # version 2
    assert cache.get("prod:42") == {"price": 150}

    # 3. Reader 1 (delayed) attempts to put v1 into cache
    accepted = cache.put_cache("record:prod:42", data_v1, version=ver_1)
    # Stale fill with version 1 < watermark 2 is rejected
    assert accepted is False
    assert cache.stale_fill_rejections == 1

    # Cache must still hold the newer version 2 data!
    current = cache.get("prod:42")
    assert current == {"price": 150}


def test_stale_fill_rejected_after_invalidation_regression():
    """EXACT REGRESSION TEST:

    Reader A captures generation and reads v1 from DB
    -> Writer B commits v2 to DB
    -> Writer B invalidates cache (watermark=2)
    -> Reader A attempts to fill cache with v1 and captured gen
    -> Verify Stale fill is REJECTED and cache remains empty or updated to v2!
    """
    db = SimulatedDatabase()
    db.write("item:99", {"desc": "Original v1"})  # DB version 1

    cache = VersionedCacheAside(db)

    # 1. Reader A captures generation fence before reading DB
    reader_a_gen = cache.get_generation("item:99")
    reader_a_data, reader_a_version = db.read("item:99")
    assert reader_a_data == {"desc": "Original v1"}
    assert reader_a_version == 1

    # 2. Writer B commits v2 to DB
    writer_b_version = db.write("item:99", {"desc": "Updated v2"})
    assert writer_b_version == 2

    # 3. Writer B invalidates cache with watermark=2
    # Invalidation removes data key, advances generation fence, and preserves/advances watermark=2
    cache.invalidate("item:99", watermark=writer_b_version)
    assert cache.get_watermark("item:99") == 2
    assert cache.get_generation("item:99") == 1
    assert cache._read_cache("item:99") is None

    # 4. Reader A (delayed) attempts to fill cache with v1 and captured gen
    accepted = cache.put_cache("item:99", reader_a_data, version=reader_a_version, captured_gen=reader_a_gen)

    # 5. Verify stale fill is REJECTED!
    assert accepted is False
    assert cache.stale_fill_rejections == 1

    # Data key must NOT contain stale v1 data (cache is empty or reflects v2)
    assert cache._read_cache("item:99") is None

    # Subsequent read through cache fetches fresh v2 from DB and populates cache
    current_val = cache.get("item:99")
    assert current_val == {"desc": "Updated v2"}
    assert cache.get_watermark("item:99") == 2


def test_cold_cache_invalidation_race_prevention():
    """REGRESSION TEST: Prevention of cold-cache invalidation race via generation fence.

    Scenario:
    1. Cold cache: data empty, watermark=0, gen=0.
    2. Reader A begins: captures gen=0, reads DB v1 (delayed before writing to cache).
    3. Writer updates DB to v2 and calls cache.invalidate("rec1")
       - increments gen to 1, deletes data, does NOT invent fake DB versions.
    4. Reader A attempts to fill cache with v1 and its captured gen=0.
    5. Assert fill is REJECTED (accepted=False), stale_fill_rejections=1, cache does NOT contain stale v1.
    6. Subsequent reader reads fresh v2 from DB and successfully fills cache.
    """
    db = SimulatedDatabase()
    db.write("rec1", {"payload": "version_1"})  # DB version 1

    cache = VersionedCacheAside(db)
    assert cache.get_watermark("rec1") == 0
    assert cache.get_generation("rec1") == 0

    # 1. Reader A captures generation fence before querying DB
    captured_gen_a = cache.get_generation("rec1")
    assert captured_gen_a == 0

    # Reader A reads DB v1
    data_v1, ver_1 = db.read("rec1")
    assert ver_1 == 1

    # 2. Writer updates DB to v2 and calls cache.invalidate("rec1")
    db.write("rec1", {"payload": "version_2"})
    cache.invalidate("rec1")
    assert cache.get_generation("rec1") == 1
    assert cache._read_cache("rec1") is None

    # 3. Delayed Reader A attempts to fill cache with v1 and captured gen=0
    accepted = cache.put_cache("rec1", data_v1, version=ver_1, captured_gen=captured_gen_a)

    # 4. Assert fill is REJECTED and stale fill counted
    assert accepted is False
    assert cache.stale_fill_rejections == 1
    assert cache._read_cache("rec1") is None

    # 5. Subsequent reader fetches fresh v2 through cache.get()
    fresh_val = cache.get("rec1")
    assert fresh_val == {"payload": "version_2"}
    assert cache.get_watermark("rec1") == 2
    assert cache._read_cache("rec1") is not None
    assert cache._read_cache("rec1").value == {"payload": "version_2"}


def test_default_invalidation_without_version_advances_generation_fence():
    """REGRESSION TEST: Default invalidation without version advances generation fence.

    1. Cache is populated at v1 (watermark=1, gen=0).
    2. Reader A captures generation fence (gen=0) and reads v1 data.
    3. Writer invalidates cache without providing a watermark (watermark=None).
       - Invalidation MUST increment the generation fence to gen=1!
       - Invalidation MUST NOT invent fake database versions (watermark remains 1).
    4. Reader A (delayed) attempts to put v1 into cache with captured gen=0.
    5. Reader A's fill is strictly REJECTED because captured_gen (0) != current_gen (1)!
    """
    db = SimulatedDatabase()
    db.write("item:default_inv", {"val": "version_1"})  # DB version 1

    cache = VersionedCacheAside(db)

    # Reader initial fill
    val = cache.get("item:default_inv")
    assert val == {"val": "version_1"}
    assert cache.get_watermark("item:default_inv") == 1
    assert cache.get_generation("item:default_inv") == 0

    # Reader A captures generation and reads v1 data
    reader_a_gen = cache.get_generation("item:default_inv")
    reader_a_data, reader_a_version = db.read("item:default_inv")
    assert reader_a_version == 1

    # Writer invalidates WITHOUT specifying version
    cache.invalidate("item:default_inv", watermark=None)

    # Generation fence must have auto-advanced from 0 to 1
    assert cache.get_generation("item:default_inv") == 1
    # Watermark does NOT invent database versions
    assert cache.get_watermark("item:default_inv") == 1
    assert cache._read_cache("item:default_inv") is None

    # Reader A attempts to fill with stale v1
    accepted = cache.put_cache("item:default_inv", reader_a_data, version=reader_a_version, captured_gen=reader_a_gen)
    assert accepted is False
    assert cache.stale_fill_rejections == 1
    assert cache._read_cache("item:default_inv") is None


def test_singleflight_dogpile_prevention():
    db = SimulatedDatabase()
    db.write("hot:item", {"stock": 50})

    sf = SingleFlight()
    call_count = 0

    def slow_db_read():
        nonlocal call_count
        call_count += 1
        time.sleep(0.05)
        return "heavy_data"

    # Synchronize all threads with a barrier so they call sf.do simultaneously
    barrier = threading.Barrier(10)

    def worker():
        barrier.wait()
        return sf.do("hot:item", slow_db_read)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker) for _ in range(10)]
        results = [f.result() for f in futures]

    assert all(r == "heavy_data" for r in results)
    # Crucial: Exactly 1 execution occurred, all other 9 threads waited on the coalesced result!
    assert call_count == 1


def test_singleflight_exception_propagation():
    """Verify that if the leader raises an exception, all waiting callers receive the exception."""
    sf = SingleFlight()

    def failing_fn():
        time.sleep(0.03)
        raise RuntimeError("DB connection dropped")

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(sf.do, "fail:key", failing_fn) for _ in range(5)]
        exceptions = []
        for f in futures:
            try:
                f.result()
            except RuntimeError as e:
                exceptions.append(str(e))

    assert len(exceptions) == 5
    assert all("DB connection dropped" in msg for msg in exceptions)


def test_singleflight_waiter_timeout():
    """Verify that a waiter times out if the leader takes longer than the timeout."""
    sf = SingleFlight()
    started = False

    def very_slow_fn():
        nonlocal started
        started = True
        time.sleep(0.2)
        return "done"

    with ThreadPoolExecutor(max_workers=2) as executor:
        # Leader starts slow task
        leader_fut = executor.submit(sf.do, "slow:key", very_slow_fn)
        # Give leader time to register in-flight
        while not started:
            time.sleep(0.005)

        # Waiter joins with a tiny timeout
        waiter_fut = executor.submit(sf.do, "slow:key", very_slow_fn, timeout=0.02)

        with pytest.raises(TimeoutError):
            waiter_fut.result()

        # Leader should still complete successfully
        assert leader_fut.result() == "done"
