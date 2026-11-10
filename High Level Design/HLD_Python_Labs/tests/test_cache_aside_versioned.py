"""Tests for Versioned Cache-Aside, Generation Fence, and Dogpile SingleFlight (Chapter 03)."""
from __future__ import annotations
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Optional
import pytest
from ch03_caching.cache_aside_versioned import (
    VersionedCacheAside,
    SingleFlight,
    SimulatedDatabase,
    LUA_VERSIONED_SET,
    LUA_INVALIDATE,
)

# Optional Redis / FakeRedis availability detection for live integration testing
REDIS_AVAILABLE = False
_redis_client_factory: Optional[Callable[[], any]] = None
_redis_skip_reason = "Neither running Redis server on localhost:6379 nor fakeredis available"

try:
    import redis
    _probe = redis.Redis(host="localhost", port=6379, socket_connect_timeout=0.5)
    _probe.ping()
    REDIS_AVAILABLE = True
    _redis_client_factory = lambda: redis.Redis(host="localhost", port=6379, decode_responses=True)
except Exception:
    try:
        import fakeredis
        _fr = fakeredis.FakeRedis(decode_responses=True)
        _fr.ping()
        REDIS_AVAILABLE = True
        _redis_client_factory = lambda: fakeredis.FakeRedis(decode_responses=True)
    except Exception as _e:
        REDIS_AVAILABLE = False
        _redis_skip_reason = f"Live Redis and fakeredis unavailable: {_e}"


# =============================================================================
# IN-MEMORY SIMULATOR TESTS (Zero-DevOps Learner Path)
# =============================================================================

def test_cache_aside_basic_flow():
    """IN-MEMORY SIMULATOR TEST: Verifies basic cache-aside miss/hit workflow."""
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
    """IN-MEMORY SIMULATOR TEST: Simulates stale fill rejection with monotonic watermark.

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
    """IN-MEMORY SIMULATOR TEST: EXACT REGRESSION TEST:

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
    """IN-MEMORY SIMULATOR TEST: Prevention of cold-cache invalidation race via generation fence.

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
    """IN-MEMORY SIMULATOR TEST: Default invalidation without version advances generation fence.

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
    """IN-MEMORY SIMULATOR TEST: Verifies SingleFlight coalesces concurrent identical requests."""
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
    """IN-MEMORY SIMULATOR TEST: Verifies leader exception propagates to all waiting callers."""
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
    """IN-MEMORY SIMULATOR TEST: Verifies a waiter times out if the leader exceeds timeout."""
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


def test_stale_fill_rejected_after_data_expiration_regression():
    """IN-MEMORY SIMULATOR TEST: Regression test: verifies that invalidation metadata
    (generation fence and watermark) persists across data-key expiration, preventing
    arbitrarily delayed readers from resurrecting stale data after the data TTL expires."""
    db = SimulatedDatabase()
    db.write("prod:42", {"price": 100})  # Version 1

    cache = VersionedCacheAside(db=db)

    # Reader A starts reading prod:42, captures generation fence (gen = 0) and gets version 1
    reader_a_gen = cache.get_generation("prod:42")
    assert reader_a_gen == 0
    val_v1, ver_1 = db.read("prod:42")
    assert ver_1 == 1

    # Writer updates DB to version 2 (price: 150) and invalidates cache with watermark 2
    cache.update("prod:42", {"price": 150}, ttl_seconds=0.05)
    # Invalidation advanced generation fence to 1 and watermark to 2
    assert cache.get_generation("prod:42") == 1
    assert cache.get_watermark("prod:42") == 2

    # Allow data key TTL to expire (0.12s sleep to safely clear Windows 15.6ms timer granularity)
    time.sleep(0.12)

    # Data key has expired from cache
    assert cache._read_cache("prod:42") is None

    # Crucial assertion: Fencing metadata MUST NOT have expired!
    assert cache.get_generation("prod:42") == 1
    assert cache.get_watermark("prod:42") == 2

    # Delayed Reader A now attempts to fill the cache with stale Version 1 and obsolete gen 0
    accepted = cache.put_cache("record:prod:42", val_v1, ver_1, captured_gen=reader_a_gen, ttl_seconds=300.0)
    assert accepted is False, "Delayed stale fill must be strictly rejected even after data key expiration!"
    assert cache.stale_fill_rejections == 1

    # Fresh reader retrieves authoritative Version 2 from DB and successfully populates cache
    fresh_val = cache.get("prod:42")
    assert fresh_val == {"price": 150}
    assert cache.get_watermark("prod:42") == 2


def test_simulated_memory_pressure_eviction_recreates_race_window():
    """IN-MEMORY SIMULATOR TEST: Demonstrates memory pressure eviction vs metadata retention.

    This test explicitly contrasts two operational realities:
    ----------------------------------------------------------
    Scenario A (Metadata Retained - volatile-lru / no memory pressure):
      - Data key is expired/evicted, but metadata keys ({entity}:gen and {entity}:v_watermark) remain.
      - A delayed reader attempting to populate stale data with an old generation fence is REJECTED.
      - The cache remains uncontaminated.

    Scenario B (Metadata Evicted - allkeys-lru memory pressure):
      - Memory pressure evicts both data AND metadata keys ({entity}:gen and {entity}:v_watermark).
      - Default missing value in Redis GET / dict.get evaluates to 0.
      - When a delayed reader arrives with captured_gen=0 and version=1:
        * captured_gen (0) == current_gen (0) evaluates to TRUE!
        * incoming_ver (1) >= current_watermark (0) evaluates to TRUE!
      - The stale fill is erroneously ACCEPTED! Stale data resurrects into the cache!

    Architectural Conclusion:
      PERSIST prevents normal TTL-based expiration, but does NOT make keys immune
      to allkeys-lru / allkeys-lfu memory eviction. Absolute fencing safety under allkeys-*
      requires either volatile-lru configuration or explicit lease tokens.
    """
    db = SimulatedDatabase()

    # -------------------------------------------------------------------------
    # Scenario A: Metadata Retained (volatile-lru or unpressured cache)
    # -------------------------------------------------------------------------
    db.write("item:retained", {"price": 100})  # Version 1 in DB
    cache_a = VersionedCacheAside(db=db)

    # Reader 1 reads DB v1, captures gen 0
    gen_reader_1 = cache_a.get_generation("item:retained")
    assert gen_reader_1 == 0
    data_v1, ver_1 = db.read("item:retained")

    # Writer updates DB to v2 and invalidates cache (gen -> 1, watermark -> 2)
    db.write("item:retained", {"price": 200})
    cache_a.invalidate("item:retained", watermark=2)
    assert cache_a.get_generation("item:retained") == 1
    assert cache_a.get_watermark("item:retained") == 2

    # Simulate data-only eviction (volatile-lru: only keys with TTL are evicted)
    cache_a.simulate_memory_pressure_eviction("item:retained", evict_data=True, evict_metadata=False)
    assert cache_a._read_cache("item:retained") is None
    # Fencing metadata is securely retained
    assert cache_a.get_generation("item:retained") == 1
    assert cache_a.get_watermark("item:retained") == 2

    # Delayed Reader 1 awakens with captured gen 0 and stale v1
    accepted_a = cache_a.put_cache("item:retained", data_v1, ver_1, captured_gen=gen_reader_1)
    assert accepted_a is False, "Stale fill MUST be rejected when fencing metadata is retained!"
    assert cache_a.stale_fill_rejections == 1
    assert cache_a._read_cache("item:retained") is None

    # -------------------------------------------------------------------------
    # Scenario B: Metadata Evicted (allkeys-lru memory pressure)
    # -------------------------------------------------------------------------
    db.write("item:evicted", {"price": 100})  # Version 1 in DB
    cache_b = VersionedCacheAside(db=db)

    # Reader 2 reads DB v1, captures gen 0
    gen_reader_2 = cache_b.get_generation("item:evicted")
    assert gen_reader_2 == 0
    data_v1_b, ver_1_b = db.read("item:evicted")

    # Writer updates DB to v2 and invalidates cache (gen -> 1, watermark -> 2)
    db.write("item:evicted", {"price": 200})
    cache_b.invalidate("item:evicted", watermark=2)
    assert cache_b.get_generation("item:evicted") == 1
    assert cache_b.get_watermark("item:evicted") == 2

    # Memory pressure under allkeys-lru evicts EVERYTHING including metadata!
    cache_b.simulate_memory_pressure_eviction("item:evicted", evict_data=True, evict_metadata=True)
    # Verification: metadata has been evicted, defaulting back to 0
    assert cache_b.get_generation("item:evicted") == 0
    assert cache_b.get_watermark("item:evicted") == 0
    assert cache_b._read_cache("item:evicted") is None

    # Delayed Reader 2 awakens with captured gen 0 and stale v1
    # Because metadata was evicted, current_gen is 0 and current_watermark is 0!
    accepted_b = cache_b.put_cache("item:evicted", data_v1_b, ver_1_b, captured_gen=gen_reader_2)
    # The race window is recreated: stale fill is erroneously accepted!
    assert accepted_b is True, "Stale fill is accepted because fencing metadata was evicted by memory pressure!"
    # The cache is now poisoned with stale version 1 data, while DB holds version 2!
    cached_record = cache_b._read_cache("item:evicted")
    assert cached_record is not None
    assert cached_record.value == {"price": 100}  # STALE V1!
    authoritative_db_val, authoritative_db_ver = db.read("item:evicted")
    assert authoritative_db_ver == 2
    assert authoritative_db_val == {"price": 200}


# =============================================================================
# LIVE REDIS LUA INTEGRATION TESTS (Optional: Requires Redis / FakeRedis)
# =============================================================================

@pytest.mark.skipif(not REDIS_AVAILABLE, reason=_redis_skip_reason)
def test_real_redis_lua_integration_atomic_set_and_generation_fence():
    """LIVE REDIS LUA INTEGRATION TEST: Executes LUA_VERSIONED_SET and LUA_INVALIDATE on Redis.

    NOTE: This test executes actual Redis Lua scripts against a live Redis/FakeRedis instance,
    strictly distinguished from the in-memory Python simulator tests above.
    Never label a Redis Lua guarantee as integration-tested when only the Python simulator ran.

    Verifies on live Redis:
    1. LUA_VERSIONED_SET populates data, watermark, and generation keys atomically in Redis.
    2. LUA_INVALIDATE removes data, advances generation fence via INCR, and persists keys.
    3. Delayed reader fill with stale generation is rejected by Redis Lua engine.
    """
    assert _redis_client_factory is not None
    r = _redis_client_factory()
    db = SimulatedDatabase()

    test_entity = "test_redis_lua_item_1"
    data_key = VersionedCacheAside._data_key(test_entity)
    watermark_key = VersionedCacheAside._watermark_key(test_entity)
    gen_key = VersionedCacheAside._gen_key(test_entity)

    try:
        # Pre-clean test keys in Redis
        r.delete(data_key, watermark_key, gen_key)

        cache = VersionedCacheAside(db=db, redis_client=r)

        # 1. Database initial state
        db.write(test_entity, {"name": "Widget v1"})

        # Reader A captures generation before DB read
        gen_reader_a = cache.get_generation(test_entity)
        assert gen_reader_a == 0
        v1_data, v1_ver = db.read(test_entity)

        # 2. Normal cache-aside miss via cache.get() populates Redis via Lua
        val = cache.get(test_entity)
        assert val == {"name": "Widget v1"}
        assert r.exists(data_key) == 1
        assert int(r.get(watermark_key)) == 1
        assert cache.get_generation(test_entity) == 0
        assert int(r.get(gen_key) or 0) == 0

        # Cache hit reads directly from Redis
        val_hit = cache.get(test_entity)
        assert val_hit == {"name": "Widget v1"}
        assert cache.cache_hits == 1

        # 3. Writer updates DB to v2 and calls invalidate()
        db.write(test_entity, {"name": "Widget v2"})
        cache.invalidate(test_entity, watermark=2)

        # Verify Redis state after LUA_INVALIDATE:
        assert r.exists(data_key) == 0  # Data deleted
        assert int(r.get(gen_key)) == 1  # Generation advanced
        assert int(r.get(watermark_key)) == 2  # Watermark updated

        # 4. Delayed Reader A attempts to fill Redis cache with v1 data and captured gen 0
        # Redis evaluates LUA_VERSIONED_SET directly on the Redis engine
        accepted = cache.put_cache(test_entity, v1_data, v1_ver, captured_gen=gen_reader_a)
        assert accepted is False, "Redis Lua script must reject stale fill when captured_gen != current_gen!"
        assert cache.stale_fill_rejections == 1
        assert r.exists(data_key) == 0  # Cache remains clean

        # 5. Subsequent reader fetches authoritative v2 from DB and successfully populates Redis
        v2_cached = cache.get(test_entity)
        assert v2_cached == {"name": "Widget v2"}
        assert r.exists(data_key) == 1
        assert int(r.get(watermark_key)) == 2
        assert int(r.get(gen_key)) == 1

    finally:
        # Ensure test isolation in Redis
        r.delete(data_key, watermark_key, gen_key)


@pytest.mark.skipif(not REDIS_AVAILABLE, reason=_redis_skip_reason)
def test_real_redis_lua_integration_metadata_persistence_and_memory_pressure_eviction():
    """LIVE REDIS LUA INTEGRATION TEST: Verifies PERSIST behavior, data TTL, and memory eviction.

    NOTE: This test executes actual Redis Lua scripts against a live Redis/FakeRedis instance.
    Never label a Redis Lua guarantee as integration-tested when only the Python simulator ran.

    Verifies on live Redis:
    1. Data key receives TTL via EXPIRE in LUA_VERSIONED_SET, while metadata keys receive PERSIST (TTL = -1).
    2. When the data key expires in Redis, metadata keys remain intact in Redis.
    3. Delayed reader is rejected by Redis Lua even after data key expiration.
    4. When simulated memory pressure deletes metadata from Redis, Redis Lua coerces nil to 0,
       recreating the stale fill race window in actual Redis!
    """
    assert _redis_client_factory is not None
    r = _redis_client_factory()
    db = SimulatedDatabase()

    test_entity = "test_redis_lua_item_2"
    data_key = VersionedCacheAside._data_key(test_entity)
    watermark_key = VersionedCacheAside._watermark_key(test_entity)
    gen_key = VersionedCacheAside._gen_key(test_entity)

    try:
        # Pre-clean
        r.delete(data_key, watermark_key, gen_key)

        cache = VersionedCacheAside(db=db, redis_client=r)

        # 1. DB write v1
        db.write(test_entity, {"stock": 100})
        gen_reader_1 = cache.get_generation(test_entity)
        assert gen_reader_1 == 0
        v1_data, v1_ver = db.read(test_entity)

        # 2. Writer updates DB to v2 and updates cache with a short TTL (1 second) for the data key
        cache.update(test_entity, {"stock": 80}, ttl_seconds=1.0)

        # Check TTL properties directly in Redis:
        data_ttl = r.ttl(data_key)
        gen_ttl = r.ttl(gen_key)
        wm_ttl = r.ttl(watermark_key)

        # Data key has active TTL
        assert data_ttl > 0
        # Generation and watermark keys are PERSIST (TTL is -1 in Redis, indicating no expiration)
        assert gen_ttl == -1, f"Expected gen_key to be persistent (TTL -1), got {gen_ttl}"
        assert wm_ttl == -1, f"Expected watermark_key to be persistent (TTL -1), got {wm_ttl}"

        # 3. Wait 1.2s for data key to expire in Redis
        time.sleep(1.2)

        # Data key has expired from Redis
        assert r.exists(data_key) == 0
        # Fencing metadata remains persistent in Redis
        assert r.exists(gen_key) == 1
        assert r.exists(watermark_key) == 1

        # 4. Delayed Reader 1 attempts to write stale v1 to Redis
        accepted_before_eviction = cache.put_cache(
            test_entity, v1_data, v1_ver, captured_gen=gen_reader_1
        )
        assert accepted_before_eviction is False, "Redis Lua must reject stale fill while metadata is retained!"
        assert cache.stale_fill_rejections == 1

        # 5. Simulate Redis memory pressure eviction (allkeys-lru) on live Redis
        # Under allkeys-lru, Redis evicts persistent metadata keys when memory is exhausted
        cache.simulate_memory_pressure_eviction(test_entity, evict_data=True, evict_metadata=True)
        assert r.exists(gen_key) == 0
        assert r.exists(watermark_key) == 0

        # 6. Delayed reader arrives after memory pressure eviction
        # Redis Lua evaluates GET gen_key -> nil (coerced to 0) and GET watermark_key -> nil (coerced to 0)
        accepted_after_eviction = cache.put_cache(
            test_entity, v1_data, v1_ver, captured_gen=0
        )
        # The race window is recreated in actual Redis!
        assert accepted_after_eviction is True, "Redis Lua accepts stale fill because metadata was evicted!"
        # Redis now holds the stale v1 data!
        assert r.exists(data_key) == 1
        cached_stale = cache._read_cache(test_entity)
        assert cached_stale is not None
        assert cached_stale.value == {"stock": 100}  # STALE V1 resurrected in Redis!

    finally:
        # Cleanup
        r.delete(data_key, watermark_key, gen_key)
