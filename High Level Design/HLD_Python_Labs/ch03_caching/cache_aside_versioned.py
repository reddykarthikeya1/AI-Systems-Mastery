"""Versioned Cache-Aside with Stale-Fill Race Prevention and Dogpile Protection.

Architectural Problem:
----------------------
In standard Cache-Aside:
1. Reader A misses in cache.
2. Reader A reads from DB (returns row version 1).
3. Writer B updates DB to version 2, and either invalidates or updates cache with version 2.
4. Reader A (delayed by GC/network) finally writes row version 1 to cache.
Result: The cache is poisoned with stale version 1 indefinitely!

CRITICAL FIX: Decoupled Monotonic Version Watermark
---------------------------------------------------
Naive versioned caching stores `_version` inside the cached data entry.
When an invalidation occurs (`DEL {entity}`), the version watermark is wiped out!
A delayed Reader A with version 1 arrives after invalidation, sees no cached version,
and successfully repopulates the cache with stale v1 data.

To eliminate this race:
1. Separate Cached Value Key from Monotonic Version Watermark Key:
   - Data Key: `{entity}:data`
   - Watermark Key: `{entity}:v_watermark`
2. Invalidation removes `{entity}:data`, but STRICTLY ADVANCES `{entity}:v_watermark`.
   - If invalidating without an explicit version (watermark=None), the watermark is automatically
     incremented (watermark = current + 1 / Redis INCR) so in-flight readers are rejected.
   - If invalidating with an explicit version V, the watermark advances to max(current + 1, V).
3. Incoming cache fills atomically compare `incoming_version >= watermark` via Lua script.
   Stale fills (`incoming_version < watermark`) are unconditionally REJECTED!
4. SingleFlight Coalescing Mutex:
   Protects against cache stampedes / dogpile effect by coalescing concurrent misses.
   (Documented: in-process SingleFlight is process-local and does NOT coordinate across
   multiple server instances without a distributed lock).

WATERMARK EXPIRY TIME WINDOW HEURISTIC:
---------------------------------------
In Redis deployments, setting a watermark expiry (e.g., 2 * data TTL) represents a practical
heuristic time window, NOT an unconditional guarantee against arbitrarily delayed readers.
If a reader is delayed (e.g., multi-minute stop-the-world GC pause) beyond the watermark TTL,
the watermark key expires and evicts. A delayed fill arriving after watermark eviction would
then repopulate stale data. Absolute protection against arbitrary delays requires persistent
tombstones or infinite TTL watermarks.
"""

from __future__ import annotations
import copy
import json
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple

# Production Redis Lua Script for Atomic Stale-Fill Rejection
LUA_VERSIONED_SET = """
-- KEYS[1]: Data key (e.g. record:{id}:data)
-- KEYS[2]: Watermark key (e.g. record:{id}:v_watermark)
-- ARGV[1]: Serialized value
-- ARGV[2]: Incoming Version (integer)
-- ARGV[3]: TTL in seconds (optional, 0 for none)

local data_key = KEYS[1]
local watermark_key = KEYS[2]
local val = ARGV[1]
local incoming_ver = tonumber(ARGV[2])
local ttl = tonumber(ARGV[3])

local current_watermark = tonumber(redis.call('GET', watermark_key) or '0')

if incoming_ver >= current_watermark then
    redis.call('SET', data_key, val)
    if incoming_ver > current_watermark then
        redis.call('SET', watermark_key, incoming_ver)
    end
    if ttl and ttl > 0 then
        redis.call('EXPIRE', data_key, ttl)
        -- Preserve watermark longer than data to protect against stale fills after eviction
        redis.call('EXPIRE', watermark_key, ttl * 2)
    end
    return 1 -- Accepted
else
    return 0 -- Rejected: Stale fill attempt
end
"""

# Production Redis Lua Script for Safe Invalidation (advancing watermark)
LUA_INVALIDATE = """
-- KEYS[1]: Data key (e.g. record:{id}:data)
-- KEYS[2]: Watermark key (e.g. record:{id}:v_watermark)
-- ARGV[1]: New watermark version (optional, 0 to auto-increment)

local data_key = KEYS[1]
local watermark_key = KEYS[2]
local new_ver = tonumber(ARGV[1] or '0')

redis.call('DEL', data_key)
if new_ver and new_ver > 0 then
    local current_watermark = tonumber(redis.call('GET', watermark_key) or '0')
    if new_ver > current_watermark then
        redis.call('SET', watermark_key, new_ver)
    else
        redis.call('INCR', watermark_key)
    end
else
    redis.call('INCR', watermark_key)
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
    """Cache-aside coordinator with version-checked atomic writes and SingleFlight."""

    def __init__(self, db: SimulatedDatabase, redis_client: Any = None) -> None:
        self.db = db
        self.redis = redis_client
        # Memory storage: data_key -> CacheRecord
        self._memory_cache: Dict[str, CacheRecord] = {}
        # Watermark storage: watermark_key -> int
        self._watermarks: Dict[str, int] = {}
        self._cache_lock = threading.Lock()
        self.single_flight = SingleFlight()
        self.stale_fill_rejections = 0
        self.cache_hits = 0
        self.cache_misses = 0

    @staticmethod
    def _data_key(key_or_id: str) -> str:
        base = key_or_id
        if base.endswith(":data"):
            return base
        if base.endswith(":v_watermark"):
            base = base[:-len(":v_watermark")]
        if not base.startswith("record:"):
            base = f"record:{base}"
        return f"{base}:data"

    @staticmethod
    def _watermark_key(key_or_id: str) -> str:
        base = key_or_id
        if base.endswith(":v_watermark"):
            return base
        if base.endswith(":data"):
            base = base[:-len(":data")]
        if not base.startswith("record:"):
            base = f"record:{base}"
        return f"{base}:v_watermark"

    def _execute_lua_in_memory(
        self, key: str, val: Any, ver: int, ttl: Optional[float] = None
    ) -> bool:
        """Exact memory simulation of the Redis Lua script logic with watermark separation."""
        data_key = self._data_key(key)
        watermark_key = self._watermark_key(key)
        now = time.monotonic()

        with self._cache_lock:
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

    def put_cache(self, key: str, value: Any, version: int, ttl_seconds: float = 300.0) -> bool:
        """Atomically stores value and updates watermark only if version >= watermark."""
        data_key = self._data_key(key)
        watermark_key = self._watermark_key(key)

        if self.redis is not None:
            serialized = json.dumps(value)
            res = self.redis.eval(
                LUA_VERSIONED_SET,
                2,
                data_key,
                watermark_key,
                serialized,
                version,
                int(ttl_seconds),
            )
            accepted = bool(res == 1)
            if not accepted:
                self.stale_fill_rejections += 1
            return accepted

        return self._execute_lua_in_memory(key, value, version, ttl=ttl_seconds)

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

            db_result = self.db.read(record_id)
            if db_result is None:
                return None

            val, ver = db_result
            # Attempt versioned write to cache
            self.put_cache(flight_key, val, ver, ttl_seconds=ttl_seconds)
            return val

        return self.single_flight.do(flight_key, loader)

    def update(self, record_id: str, new_data: Any, ttl_seconds: float = 300.0) -> int:
        """Write-through DB update with cache synchronization."""
        new_version = self.db.write(record_id, new_data)
        flight_key = f"record:{record_id}"
        # Update cache atomically with the new version
        self.put_cache(flight_key, new_data, new_version, ttl_seconds=ttl_seconds)
        return new_version

    def invalidate(
        self,
        record_id: str,
        watermark: Optional[int] = None,
        new_version: Optional[int] = None,
    ) -> None:
        """Evicts cached value data while strictly advancing the watermark.

        Safety Contract:
        ----------------
        1. Default Invalidation (watermark=None):
           Automatically increments the watermark (`current_watermark + 1`). This guarantees
           that any in-flight Reader reading prior to this invalidation (with version <= current_watermark)
           is strictly rejected when attempting a delayed cache fill.
        2. Explicit Version Invalidation (watermark=V):
           Sets the watermark to max(current_watermark + 1, V) or V if V > current_watermark.
           This ensures monotonicity and prevents delayed stale fills from preceding DB states.

        Watermark Expiry Limitation (Heuristic Window):
        -----------------------------------------------
        In Redis deployments, setting a watermark TTL (e.g., 2 * data TTL) provides a heuristic
        safety window rather than an unconditional mathematical guarantee. If a reader is paused
        (e.g., severe GC pause or network partition) longer than the watermark TTL, the watermark key
        evicts, leaving the entity vulnerable to a stale fill upon wakeup. Eliminating this completely
        requires persistent tombstones or indefinite/infinite watermark TTLs.

        Args:
            record_id: Entity ID to invalidate.
            watermark: Optional new watermark to advance to.
            new_version: Alias for watermark for convenience.
        """
        data_key = self._data_key(record_id)
        watermark_key = self._watermark_key(record_id)
        target_wm = watermark if watermark is not None else new_version

        if self.redis is not None:
            self.redis.eval(
                LUA_INVALIDATE,
                2,
                data_key,
                watermark_key,
                target_wm if target_wm is not None else 0,
            )
        else:
            with self._cache_lock:
                self._memory_cache.pop(data_key, None)
                curr_wm = self._watermarks.get(watermark_key, 0)
                if target_wm is None:
                    self._watermarks[watermark_key] = curr_wm + 1
                else:
                    self._watermarks[watermark_key] = (
                        target_wm if target_wm > curr_wm else curr_wm + 1
                    )

    def get_watermark(self, record_id: str) -> int:
        """Returns the current watermark version for a record."""
        watermark_key = self._watermark_key(record_id)
        if self.redis is not None:
            val = self.redis.get(watermark_key)
            return int(val) if val is not None else 0
        with self._cache_lock:
            return self._watermarks.get(watermark_key, 0)

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
