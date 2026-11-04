"""Tests for Versioned Cache-Aside and Dogpile SingleFlight (Chapter 03)."""
import time
from concurrent.futures import ThreadPoolExecutor
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
    assert accepted is False
    assert cache.stale_fill_rejections == 1

    # Cache must still hold the newer version 2 data!
    current = cache.get("prod:42")
    assert current == {"price": 150}


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

    # Launch 10 concurrent threads requesting the exact same key
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(sf.do, "hot:item", slow_db_read) for _ in range(10)]
        results = [f.result() for f in futures]

    assert all(r == "heavy_data" for r in results)
    # Crucial: Exactly 1 execution occurred, all other 9 threads waited on the coalesced result!
    assert call_count == 1
