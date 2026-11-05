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

CRITICAL FIX: Decoupled Invalidation-Generation Fence and Monotonic Watermark
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

PERSISTENCE AND TTL REQUIREMENTS OF FENCING METADATA:
-----------------------------------------------------
In Redis deployments, setting a TTL on `{entity}:gen` and `{entity}:v_watermark` (e.g. 2 * data TTL)
represents a practical heuristic time window, NOT an unconditional mathematical guarantee against
arbitrarily delayed readers. If a reader is paused (e.g., severe stop-the-world GC pause or network
partition) beyond the metadata TTL, the generation and watermark keys evict. A delayed fill arriving
after eviction could repopulate stale data. Absolute protection against arbitrary delays requires
persistent fencing metadata (no TTL) or persistent tombstones.
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

local current_gen = tonumber(redis.call('GET', gen_key) or '0')
if captured_gen ~= current_gen then
    return 0 -- Rejected: Invalidation generation mismatch
end

local current_watermark = tonumber(redis.call('GET', watermark_key) or '0')
if incoming_ver >= current_watermark then
    redis.call('SET', data_key, val)
    if incoming_ver > current_watermark then
        redis.call('SET', watermark_key, incoming_ver)
    end
    if ttl and ttl > 0 then
        redis.call('EXPIRE', data_key, ttl)
        -- Preserve watermark and generation fence longer than data to protect against stale fills after eviction
        redis.call('EXPIRE', watermark_key, ttl * 2)
        redis.call('EXPIRE', gen_key, ttl * 2)
    end
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
-- Persist fence metadata to ensure it does not prematurely expire while delayed readers are in flight
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
        """Atomically stores value and updates watermark only if captured_gen == current_gen and version >= watermark."""
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
        # Capture current generation at write time so update never uses an obsolete fence
        current_gen = self.get_generation(record_id)
        flight_key = f"record:{record_id}"
        # Update cache atomically with the new version and active generation fence
        self.put_cache(flight_key, new_data, new_version, captured_gen=current_gen, ttl_seconds=ttl_seconds)
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

        Persistence/TTL Requirements:
        -----------------------------
        In Redis deployments, setting a metadata TTL (e.g. 2 * data TTL) provides a heuristic
        safety window rather than an unconditional mathematical guarantee. If a reader is paused
        longer than the metadata TTL, the generation and watermark keys evict, leaving the entity
        vulnerable to a stale fill upon wakeup. Eliminating this completely requires persistent
        fencing metadata without TTL or persistent tombstones.

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
