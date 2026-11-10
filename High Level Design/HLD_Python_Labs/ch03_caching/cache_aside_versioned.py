"""Versioned Cache-Aside with Stale-Fill Race Prevention, Dogpile Protection, and Generation Fence.

Architectural Problem:
----------------------
In standard Cache-Aside:
1. Reader A misses in cache.
2. Reader A reads from DB (returns row version 1).
3. Writer B updates DB to version 2, and either invalidates or updates cache with version 2.
4. Reader A (delayed by GC/network) finally writes row version 1 to cache.
Result: The cache is poisoned with stale version 1 indefinitely!

The Cold-Cache Invalidation Race:
---------------------------------
Watermark-only approaches fail when the cache is cold.
Suppose an entity has no cached entry and no watermark stored (watermark = 0):
1. Reader A starts loading version 1 while cache and watermark are empty.
2. Writer updates DB to version 2 and calls invalidate().
3. If invalidation merely deletes the data or auto-increments watermark from 0 to 1,
   delayed Reader A arrives with version 1 >= watermark (1 or 0), and its stale fill is accepted!
Inventing database versions during invalidation is fundamentally unsafe.

CRITICAL FIX: Decoupled Invalidation-Generation Fence and Monotonic Watermark:
-----------------------------------------------------------------------------
To completely eliminate both stale fills and cold-cache invalidation races:
1. Invalidation-Generation Fence:
   - Generation Key: `{entity}:gen` (in-memory `self._generations: Dict[str, int]`, Redis `record:{id}:gen`).
   - Monotonic Invalidation Counter: incremented on every `invalidate()` call (`INCR {entity}:gen`).
   - Invalidation removes `{entity}:data` and increments `{entity}:gen`.
   - Invalidation does NOT invent database versions!
2. Monotonic DB Watermark:
   - Watermark Key: `{entity}:v_watermark`
   - Strictly tracks monotonic observed database row versions.
3. Two-Tiered Validation on Cache Fill:
   - Reader captures generation fence BEFORE querying the DB: `captured_gen = cache.get_generation(record_id)`.
   - When attempting to populate the cache (`put_cache` / `LUA_VERSIONED_SET`), fill is accepted ONLY if:
     a. `captured_generation == current_generation` (proves NO invalidation occurred while reader fetched from DB).
     b. `incoming_version >= current_watermark` (proves row version is not older than observed DB watermark).
   - If `captured_gen != current_gen` or `incoming_version < current_watermark`, fill is REJECTED (`accepted = False`).
   - When accepted, watermark updates to `max(current_watermark, incoming_version)`.
4. SingleFlight Coalescing Mutex:
   - Protects against cache stampedes / dogpile effect by coalescing concurrent misses.
   - (Process-local; multi-instance clusters require distributed locks or lease tokens).

=============================================================================
COMPREHENSIVE INVARIANT ANALYSIS UNDER REAL-WORLD SYSTEM FAILURES
=============================================================================

1. Data-Key Expiration:
   - Behavior: `{entity}:data` expires via standard TTL (e.g. 5 minutes).
   - Invariant: Fencing metadata (`{entity}:gen` and `{entity}:v_watermark`) MUST NOT expire
     synchronously with the data key! If metadata expired alongside data, a reader whose execution
     is suspended across the TTL window would find an empty fence, allowing stale writes.
   - Solution: Metadata keys are decoupled from data TTL and explicitly persisted (`PERSIST`).

2. Delayed Readers:
   - Behavior: Reader A misses in cache, queries DB, and is suspended (e.g. JVM/Python GC pause,
     thread starvation, OS paging, hypervisor steal, or network latency) for seconds or minutes.
   - Invariant: When Reader A awakens, any concurrent DB write/invalidation that occurred during its
     pause must cause Reader A's cache fill attempt to be strictly rejected.
   - Guarantee: The generation fence check (`captured_gen == current_gen`) rejects fills if any
     invalidation occurred; the watermark check (`ver >= watermark`) rejects fills if a newer version
     was already committed.

3. Invalidation During Database Reads:
   - Behavior: Reader A queries DB (version 1). Concurrently, Writer B commits version 2 to DB and
     triggers `invalidate(record_id)`. Invalidation executes before Reader A completes its write to cache.
   - Invariant: Reader A's write must never overwrite the invalidation.
   - Guarantee: Invalidation increments `{entity}:gen`. When Reader A calls `put_cache` with its
     pre-read `captured_gen`, the Lua script observes `captured_gen < current_gen` and rejects the write.

4. Cold-Cache Invalidation:
   - Behavior: An entity exists in the DB (version 1) but has never been cached (`gen = 0`, `watermark = 0`).
     Reader A initiates a read. Before Reader A populates cache, Writer B updates DB to version 2 and
     invalidates the cache.
   - Invariant: The invalidation must fence out Reader A even though the cache had no prior record of the key.
   - Guarantee: Invalidation advances `{entity}:gen` from 0 to 1. Reader A's `captured_gen = 0` no longer
     matches `current_gen = 1`. Invalidation avoids inventing arbitrary database version numbers.

5. Concurrent Fills (Dogpile / Cache Stampede):
   - Behavior: A hot key expires or is invalidated. Hundreds of concurrent requests miss simultaneously.
   - Invariant: The database must not be overwhelmed by identical queries, and concurrent cache writers
     must not race into inconsistent states.
   - Guarantee: Process-local `SingleFlight` mutex coalesces concurrent misses into a single DB read.
     The atomic Lua script (`LUA_VERSIONED_SET`) ensures that if multiple fills execute, monotonic
     watermarks and generation fences serialize them safely.

6. Redis Eviction Policies & The Fallacy of `PERSIST` Immunity:
   - Crucial Distinction: `PERSIST` removes the key's TTL, making it immune to TTL-based expiry.
     HOWEVER, `PERSIST` does NOT make Redis keys immune to memory eviction policies!
   - Redis eviction behavior by `maxmemory-policy`:
     * `allkeys-lru` / `allkeys-lfu` / `allkeys-random`:
       Redis evicts ANY key (even persistent keys without TTL) when memory exceeds `maxmemory`.
       Under these policies, severe memory pressure can evict `{entity}:gen` and `{entity}:v_watermark`!
     * `volatile-lru` / `volatile-lfu` / `volatile-ttl` / `volatile-random`:
       Redis evicts ONLY keys that have an expiration (TTL) set. Because `{entity}:gen` and
       `{entity}:v_watermark` are marked with `PERSIST` (no TTL), they are IMMUNE to eviction under
       `volatile-*` policies! Only `{entity}:data` (which has a TTL) will be evicted.
     * `noeviction`:
       Redis never evicts keys. Writes return OOM errors when memory is exhausted. Invalidation
       fencing guarantees remain intact, but cache write availability is degraded.

7. Redis Memory Pressure & Race Window Recreation:
   - Failure Scenario under `allkeys-lru`:
     1. Reader A captures `captured_gen = 0`, reads version 1 from DB, and suffers a GC pause.
     2. Writer B updates DB to version 2, and invalidates cache (`gen = 1`, `v_watermark = 2`).
     3. Heavy traffic causes Redis to exceed `maxmemory`. Under `allkeys-lru`, Redis evicts
        `{entity}:gen` and `{entity}:v_watermark` because they have not been recently accessed.
     4. Because Redis returns `nil` for nonexistent keys, Lua coerces `GET {entity}:gen` to `0`
        and `GET {entity}:v_watermark` to `0`.
     5. Reader A awakens and calls `put_cache(ver=1, captured_gen=0)`.
     6. Lua check evaluates:
        - `captured_gen (0) == current_gen (0)` -> PASS!
        - `incoming_ver (1) >= current_watermark (0)` -> PASS!
     7. The stale fill is ACCEPTED! The cache is poisoned with stale version 1!
   - Takeaway: Memory pressure under `allkeys-*` evicts metadata, completely recreating the race window.

=============================================================================
STORAGE-GROWTH TRADE-OFF & PRODUCTION ALTERNATIVES
=============================================================================

The O(N) Storage Growth Problem:
--------------------------------
If fencing metadata keys (`{entity}:gen` and `{entity}:v_watermark`) are permanently persisted
(`PERSIST`) to ensure absolute stale-fill safety under `volatile-lru`, every unique entity ever
accessed or invalidated retains metadata forever.
In systems with high entity churn (e.g. transient sessions, short-lived orders, deleted users),
fencing metadata accumulates without bound:
   Metadata Memory = O(N_total_entities_over_lifetime * metadata_bytes_per_entity)
Over months or years, orphaned metadata keys consume gigabytes of Redis RAM, leading to memory
exhaustion even when the active working set of cached data is tiny!

Production Mitigation Strategies:
---------------------------------
To balance stale-fill safety against unbounded memory growth, production systems employ three
architectural patterns:

1. Bounded Epoch TTL:
   - Instead of permanent `PERSIST`, assign metadata keys a generous, bounded TTL:
     `TTL(metadata) = max_expected_reader_delay + safety_margin`
     (e.g., if max query timeout is 30s and max client delay is 60s, set metadata TTL to 1 hour or 24 hours).
   - Invariant: Bounds Redis memory growth to active entities within the epoch window, while
     protecting against 99.999% of realistic delays. Any reader delayed beyond 1 hour is assumed dead.

2. Epoch / Generation Tombstone Garbage Collection:
   - Retain metadata as tombstones upon entity deletion/invalidation.
   - A background worker/sweeper scans tombstones and deletes metadata whose last-updated timestamp
     exceeds the database `statement_timeout` + maximum application connection lifetime.
   - Guarantees memory is reclaimed for historical entities without risking race conditions
     during active query execution.

3. Lease Tokens / SingleFlight Version Fencing (e.g. Memcached Leases / Boxed Leases):
   - On cache miss, reader requests a short-lived lease token (e.g. TTL 10-30 seconds) from Redis.
   - Only the holder of the active lease token for the current generation may fill the cache.
   - If the lease expires before the reader completes the DB fetch, or if an invalidation revoked
     the lease, the cache fill is rejected immediately.
   - Eliminates the need for permanent metadata keys entirely.

=============================================================================
TRADE-OFF MATRIX: MEMORY PRESSURE VS STALE-FILL SAFETY
=============================================================================
+-----------------------+-------------------+--------------------+--------------------+--------------------+
| Strategy              | Redis Policy Req  | Delayed Reader     | Memory Footprint   | Complexity         |
|                       |                   | Safety Guarantee   |                    |                    |
+-----------------------+-------------------+--------------------+--------------------+--------------------+
| Permanent PERSIST     | volatile-lru or   | Unconditional      | Unbounded O(N)     | Low (Current       |
|                       | noeviction        | (fails under       | (leaks dead keys)  | implementation)    |
|                       | (NOT allkeys-*)   | allkeys-lru)       |                    |                    |
+-----------------------+-------------------+--------------------+--------------------+--------------------+
| Bounded Epoch TTL     | volatile-lru or   | Bounded by TTL     | Bounded to active  | Low                |
| (e.g. TTL = 1 hour)   | allkeys-lru       | window (e.g. 1h)   | working set window |                    |
+-----------------------+-------------------+--------------------+--------------------+--------------------+
| Tombstone GC Sweeper  | Any               | Safe outside       | Bounded by GC      | Medium (requires   |
|                       |                   | active DB queries  | sweep cadence      | background worker) |
+-----------------------+-------------------+--------------------+--------------------+--------------------+
| Lease Tokens          | Any               | Strictly safe      | Zero permanent     | High (requires     |
|                       |                   | within lease TTL   | metadata overhead  | lease protocol)    |
+-----------------------+-------------------+--------------------+--------------------+--------------------+
"""

from __future__ import annotations
import copy
import json
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple

# Production Redis Lua Script for Atomic Stale-Fill Rejection with Generation Fence
LUA_VERSIONED_SET = """
-- KEYS[1]: Data key (e.g. record:{id}:data)
-- KEYS[2]: Watermark key (e.g. record:{id}:v_watermark)
-- KEYS[3]: Generation key (e.g. record:{id}:gen)
-- ARGV[1]: Serialized value
-- ARGV[2]: Incoming Version (integer)
-- ARGV[3]: Captured Generation (integer)
-- ARGV[4]: TTL in seconds (optional, 0 for none)

local data_key = KEYS[1]
local watermark_key = KEYS[2]
local gen_key = KEYS[3]
local val = ARGV[1]
local incoming_ver = tonumber(ARGV[2])
local captured_gen = tonumber(ARGV[3])
local ttl = tonumber(ARGV[4])

-- Check Generation Fence:
-- Note: If gen_key was evicted by allkeys-lru memory pressure, redis.call returns nil,
-- defaulting to '0'. If reader captured gen=0, captured_gen == current_gen evaluates to true,
-- recreating the race window! Fencing metadata must be protected against eviction.
local current_gen = tonumber(redis.call('GET', gen_key) or '0')
if captured_gen ~= current_gen then
    return 0 -- Rejected: Invalidation generation mismatch
end

-- Check Watermark:
-- Note: If watermark_key was evicted by allkeys-lru, it defaults to '0', which allows
-- any positive incoming_ver to pass.
local current_watermark = tonumber(redis.call('GET', watermark_key) or '0')
if incoming_ver >= current_watermark then
    redis.call('SET', data_key, val)
    if incoming_ver > current_watermark then
        redis.call('SET', watermark_key, incoming_ver)
    end
    if ttl and ttl > 0 then
        redis.call('EXPIRE', data_key, ttl)
    end
    -- Architectural Note: Invalidation metadata (watermark and generation fence) is marked PERSIST
    -- to remove volatile TTL expiration.
    -- CRITICAL CAVEAT: PERSIST does NOT protect against allkeys-lru/allkeys-lfu maxmemory eviction policies!
    -- Under memory pressure in allkeys-lru, Redis can evict gen_key and watermark_key, causing GET
    -- to return nil (defaulting to 0) and recreating the race window for delayed readers.
    -- volatile-lru protects these persistent keys, but risks O(N) storage growth without GC/TTL bounding.
    redis.call('PERSIST', watermark_key)
    redis.call('PERSIST', gen_key)
    return 1 -- Accepted
else
    return 0 -- Rejected: Stale version fill attempt
end
"""

# Production Redis Lua Script for Safe Invalidation (advancing generation fence)
LUA_INVALIDATE = """
-- KEYS[1]: Data key (e.g. record:{id}:data)
-- KEYS[2]: Watermark key (e.g. record:{id}:v_watermark)
-- KEYS[3]: Generation key (e.g. record:{id}:gen)
-- ARGV[1]: New watermark version (optional, 0 to leave unchanged)

local data_key = KEYS[1]
local watermark_key = KEYS[2]
local gen_key = KEYS[3]
local new_ver = tonumber(ARGV[1] or '0')

redis.call('DEL', data_key)
redis.call('INCR', gen_key)
-- Persist fence metadata to remove TTL; protected under volatile-lru, but susceptible to allkeys-lru eviction
redis.call('PERSIST', gen_key)
redis.call('PERSIST', watermark_key)

if new_ver and new_ver > 0 then
    local current_watermark = tonumber(redis.call('GET', watermark_key) or '0')
    if new_ver > current_watermark then
        redis.call('SET', watermark_key, new_ver)
    end
end
return 1
"""


@dataclass(frozen=True)
class CacheRecord:
    value: Any
    version: int
    expires_at: Optional[float] = None


class SingleFlight:
    """Coalesces concurrent requests for the exact same key to avoid Dogpile/Stampede.

    WARNING / ARCHITECTURAL LIMITATION:
    ------------------------------------
    In-process SingleFlight is strictly process-local (in-memory) and does NOT coordinate
    across multiple server instances or cluster nodes.
    For multi-instance distributed deployments, stampede defense requires:
    1. Distributed locks (e.g., Redis Redlock or ZooKeeper recipes)
    2. Probabilistic early expiration (e.g., XFetch algorithm)
    3. Centralized coordinator / cache lease tokens (e.g., Memcached leases)
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._in_flight: Dict[str, Tuple[threading.Event, Dict[str, Any]]] = {}

    def do(
        self,
        key: str,
        fn: Callable[[], Any],
        timeout: Optional[float] = None,
    ) -> Any:
        """Executes fn only once for concurrent requests with the same key.

        Args:
            key: Coalescing key identifier.
            fn: Callable to execute by the leader.
            timeout: Optional maximum wait time for followers awaiting leader completion.
        """
        with self._lock:
            if key in self._in_flight:
                event, result_box = self._in_flight[key]
                first = False
            else:
                event = threading.Event()
                result_box = {"val": None, "err": None}
                self._in_flight[key] = (event, result_box)
                first = True

        if not first:
            signaled = event.wait(timeout=timeout)
            if not signaled:
                raise TimeoutError(f"SingleFlight timed out waiting for key: {key}")
            if result_box["err"] is not None:
                raise result_box["err"]
            return result_box["val"]

        try:
            val = fn()
            result_box["val"] = val
            return val
        except Exception as e:
            result_box["err"] = e
            raise
        finally:
            with self._lock:
                self._in_flight.pop(key, None)
            event.set()


class SimulatedDatabase:
    """Simulated thread-safe relational database with optimistic row versions."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # id -> {"data": Any, "version": int}
        self._rows: Dict[str, Dict[str, Any]] = {}
        self.read_count = 0
        self.write_count = 0

    def write(self, record_id: str, data: Any) -> int:
        with self._lock:
            self.write_count += 1
            current = self._rows.get(record_id, {"version": 0})
            new_version = current["version"] + 1
            self._rows[record_id] = {"data": copy.deepcopy(data), "version": new_version}
            return new_version

    def read(self, record_id: str) -> Optional[Tuple[Any, int]]:
        with self._lock:
            self.read_count += 1
            row = self._rows.get(record_id)
            if row is None:
                return None
            return copy.deepcopy(row["data"]), row["version"]


class VersionedCacheAside:
    """Cache-aside coordinator with version-checked atomic writes, generation fence, and SingleFlight."""

    def __init__(self, db: SimulatedDatabase, redis_client: Any = None) -> None:
        self.db = db
        self.redis = redis_client
        # Memory storage: data_key -> CacheRecord
        self._memory_cache: Dict[str, CacheRecord] = {}
        # Watermark storage: watermark_key -> int
        self._watermarks: Dict[str, int] = {}
        # Invalidation generation fence storage: gen_key -> int
        self._generations: Dict[str, int] = {}
        self._cache_lock = threading.Lock()
        self.single_flight = SingleFlight()
        self.stale_fill_rejections = 0
        self.cache_hits = 0
        self.cache_misses = 0

    @staticmethod
    def _base_id(key_or_id: str) -> str:
        base = key_or_id
        for suffix in (":data", ":v_watermark", ":gen"):
            if base.endswith(suffix):
                base = base[:-len(suffix)]
                break
        if not base.startswith("record:"):
            base = f"record:{base}"
        return base

    @classmethod
    def _data_key(cls, key_or_id: str) -> str:
        return f"{cls._base_id(key_or_id)}:data"

    @classmethod
    def _watermark_key(cls, key_or_id: str) -> str:
        return f"{cls._base_id(key_or_id)}:v_watermark"

    @classmethod
    def _gen_key(cls, key_or_id: str) -> str:
        return f"{cls._base_id(key_or_id)}:gen"

    def _execute_lua_in_memory(
        self,
        key: str,
        val: Any,
        ver: int,
        captured_gen: int,
        ttl: Optional[float] = None,
    ) -> bool:
        """Exact memory simulation of the Redis Lua script logic with watermark separation and generation fence."""
        data_key = self._data_key(key)
        watermark_key = self._watermark_key(key)
        gen_key = self._gen_key(key)
        now = time.monotonic()

        with self._cache_lock:
            current_gen = self._generations.get(gen_key, 0)
            if captured_gen != current_gen:
                self.stale_fill_rejections += 1
                return False

            current_wm = self._watermarks.get(watermark_key, 0)
            if ver >= current_wm:
                expires_at = (now + ttl) if ttl and ttl > 0 else None
                self._memory_cache[data_key] = CacheRecord(
                    value=copy.deepcopy(val),
                    version=ver,
                    expires_at=expires_at,
                )
                if ver > current_wm:
                    self._watermarks[watermark_key] = ver
                return True
            else:
                self.stale_fill_rejections += 1
                return False

    def put_cache(
        self,
        key: str,
        value: Any,
        version: int,
        captured_gen: Optional[int] = None,
        ttl_seconds: float = 300.0,
    ) -> bool:
        """Atomically stores value and updates watermark only if captured_gen == current_gen and version >= watermark.

        Two-Tiered Invariant Verification:
        -----------------------------------
        1. Generation Fence Check: `captured_gen == current_gen`
           Ensures no invalidation has occurred between the reader capturing the fence and attempting to write.
        2. Monotonic Watermark Check: `version >= current_watermark`
           Ensures that incoming data row version is at least as fresh as the observed DB watermark.

        Caveat under Redis memory pressure:
        If `{entity}:gen` or `{entity}:v_watermark` was evicted under `allkeys-lru`, Redis returns `nil`
        which defaults to 0. A delayed reader that started when `gen = 0` will match `current_gen = 0`,
        recreating the stale fill race window! Fencing metadata must be protected by eviction policies.
        """
        if captured_gen is None:
            captured_gen = self.get_generation(key)

        data_key = self._data_key(key)
        watermark_key = self._watermark_key(key)
        gen_key = self._gen_key(key)

        if self.redis is not None:
            serialized = json.dumps(value)
            res = self.redis.eval(
                LUA_VERSIONED_SET,
                3,
                data_key,
                watermark_key,
                gen_key,
                serialized,
                version,
                captured_gen,
                int(ttl_seconds),
            )
            accepted = bool(res == 1)
            if not accepted:
                self.stale_fill_rejections += 1
            return accepted

        return self._execute_lua_in_memory(
            key, value, version, captured_gen=captured_gen, ttl=ttl_seconds
        )

    def get_generation(self, record_id: str) -> int:
        """Returns the current invalidation generation fence for a record."""
        gen_key = self._gen_key(record_id)
        if self.redis is not None:
            val = self.redis.get(gen_key)
            return int(val) if val is not None else 0
        with self._cache_lock:
            return self._generations.get(gen_key, 0)

    def get_watermark(self, record_id: str) -> int:
        """Returns the current watermark version for a record."""
        watermark_key = self._watermark_key(record_id)
        if self.redis is not None:
            val = self.redis.get(watermark_key)
            return int(val) if val is not None else 0
        with self._cache_lock:
            return self._watermarks.get(watermark_key, 0)

    def get(self, record_id: str, ttl_seconds: float = 300.0) -> Optional[Any]:
        """Fetch item using Cache-Aside with Dogpile protection and stale-fill defense."""
        # 1. Check cache first
        cached = self._read_cache(record_id)
        if cached is not None:
            self.cache_hits += 1
            return cached.value

        self.cache_misses += 1
        flight_key = f"record:{record_id}"

        # 2. Coalesce concurrent cache misses via SingleFlight to prevent Dogpile
        def loader() -> Optional[Any]:
            # Double check cache inside singleflight in case earlier coalesced caller filled it
            cached_check = self._read_cache(record_id)
            if cached_check is not None:
                return cached_check.value

            # Capture generation fence BEFORE querying the DB
            captured_gen = self.get_generation(record_id)

            db_result = self.db.read(record_id)
            if db_result is None:
                return None

            val, ver = db_result
            # Attempt versioned write to cache with captured generation fence
            self.put_cache(flight_key, val, ver, captured_gen=captured_gen, ttl_seconds=ttl_seconds)
            return val

        return self.single_flight.do(flight_key, loader)

    def update(self, record_id: str, new_data: Any, ttl_seconds: float = 300.0) -> int:
        """Write-through DB update with cache synchronization."""
        new_version = self.db.write(record_id, new_data)
        gen_key = self._gen_key(record_id)
        if self.redis is not None:
            new_gen = self.redis.incr(gen_key)
            self.redis.persist(gen_key)
        else:
            with self._cache_lock:
                self._generations[gen_key] = self._generations.get(gen_key, 0) + 1
                new_gen = self._generations[gen_key]
        flight_key = f"record:{record_id}"
        # Update cache atomically with the new version and active generation fence
        self.put_cache(flight_key, new_data, new_version, captured_gen=new_gen, ttl_seconds=ttl_seconds)
        return new_version

    def invalidate(
        self,
        record_id: str,
        watermark: Optional[int] = None,
        new_version: Optional[int] = None,
    ) -> None:
        """Evicts cached value data while strictly advancing the invalidation generation fence.

        Safety Contract:
        ----------------
        1. Invalidation-Generation Fence:
           Atomically increments `{entity}:gen` (`self._generations[gen_key] += 1` or Redis `INCR`).
           Any in-flight reader that captured generation prior to this invalidation will have
           its cache fill rejected because `captured_gen != current_gen`.
        2. Monotonic Database Watermark:
           Database versions are NOT invented or auto-incremented during invalidation.
           The DB row-version watermark is kept strictly separate from the invalidation generation.
           Only if an explicit, valid database version is provided (watermark=V or new_version=V)
           is `{entity}:v_watermark` updated to max(current_watermark, V).
        3. Data Removal:
           Removes `{entity}:data` from cache.

        Persistence, Eviction Policies, and Storage Growth:
        ----------------------------------------------------
        - `PERSIST` strips TTL from generation and watermark keys.
        - Under Redis `volatile-lru`, keys without TTL are protected from eviction, ensuring fences hold.
        - Under Redis `allkeys-lru`, memory pressure CAN evict persistent metadata keys, resetting them
          to 0 and recreating the stale-fill race window for delayed readers.
        - Permanent metadata causes an O(N) storage-growth problem as historical entities accumulate.
        - Production alternatives to unbounded permanent metadata:
          a) Bounded Epoch TTL: set metadata TTL = max_expected_read_latency + safety_margin (e.g. 1 hour).
          b) Tombstone Garbage Collection: background worker cleans tombstones older than query timeout.
          c) Lease Tokens: short-lived leases that reject fills if expired.

        Args:
            record_id: Entity ID to invalidate.
            watermark: Optional explicit database watermark version to advance to.
            new_version: Alias for watermark for convenience.
        """
        data_key = self._data_key(record_id)
        watermark_key = self._watermark_key(record_id)
        gen_key = self._gen_key(record_id)
        target_wm = watermark if watermark is not None else new_version

        if self.redis is not None:
            self.redis.eval(
                LUA_INVALIDATE,
                3,
                data_key,
                watermark_key,
                gen_key,
                target_wm if target_wm is not None else 0,
            )
        else:
            with self._cache_lock:
                self._memory_cache.pop(data_key, None)
                self._generations[gen_key] = self._generations.get(gen_key, 0) + 1
                if target_wm is not None and target_wm > 0:
                    curr_wm = self._watermarks.get(watermark_key, 0)
                    if target_wm > curr_wm:
                        self._watermarks[watermark_key] = target_wm

    def simulate_memory_pressure_eviction(
        self,
        record_id: str,
        evict_data: bool = True,
        evict_metadata: bool = True,
    ) -> None:
        """Simulates Redis memory pressure eviction (e.g. under allkeys-lru / allkeys-random).

        Demonstrates how Redis maxmemory eviction can evict persistent metadata keys
        (`{entity}:gen`, `{entity}:v_watermark`) even if marked with PERSIST, recreating
        the stale fill race window for delayed readers.

        Args:
            record_id: Entity ID whose keys are subject to simulated memory pressure.
            evict_data: Whether to evict the data key.
            evict_metadata: Whether to evict the generation fence and watermark metadata keys.
        """
        data_key = self._data_key(record_id)
        watermark_key = self._watermark_key(record_id)
        gen_key = self._gen_key(record_id)

        if self.redis is not None:
            keys_to_del = []
            if evict_data:
                keys_to_del.append(data_key)
            if evict_metadata:
                keys_to_del.extend([watermark_key, gen_key])
            if keys_to_del:
                self.redis.delete(*keys_to_del)
        else:
            with self._cache_lock:
                if evict_data:
                    self._memory_cache.pop(data_key, None)
                if evict_metadata:
                    self._watermarks.pop(watermark_key, None)
                    self._generations.pop(gen_key, None)

    def _read_cache(self, key_or_id: str) -> Optional[CacheRecord]:
        data_key = self._data_key(key_or_id)
        now = time.monotonic()

        if self.redis is not None:
            val_bytes = self.redis.get(data_key)
            if val_bytes is None:
                return None
            val = json.loads(val_bytes)
            ver = self.get_watermark(key_or_id)
            return CacheRecord(value=val, version=ver)
        else:
            with self._cache_lock:
                rec = self._memory_cache.get(data_key)
                if rec is None:
                    return None
                if rec.expires_at and rec.expires_at < now:
                    del self._memory_cache[data_key]
                    return None
                return rec
