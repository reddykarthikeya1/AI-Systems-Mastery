"""Versioned Cache-Aside with Stale-Fill Race Prevention and Dogpile Protection.

Architectural Problem:
----------------------
In standard Cache-Aside:
1. Reader A misses in cache.
2. Reader A reads from DB (returns row version 1).
3. Writer B updates DB to version 2, and either invalidates or updates cache with version 2.
4. Reader A (delayed by GC/network) finally writes row version 1 to cache.
Result: The cache is poisoned with stale version 1 indefinitely!

Solution:
---------
1. Version-Checked Atomic Write (via Redis Lua script):
   Cache entries store data along with their database `row_version`.
   The Lua script atomically checks:
       `if not cached_version or new_version > cached_version then SET else REJECT`
2. Dogpile / Cache Stampede Protection (SingleFlight / Coalescing Mutex):
   When a popular key expires, 10,000 concurrent requests would otherwise flood
   the database. SingleFlight ensures exactly ONE thread/process executes the DB fetch,
   and all other concurrent callers await that single result.
"""

from __future__ import annotations
import json
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple

# Production Redis Lua Script
LUA_VERSIONED_SET = """
-- KEYS[1]: Cache key
-- ARGV[1]: Serialized value
-- ARGV[2]: Version (integer)
-- ARGV[3]: TTL in seconds (optional, 0 for none)

local key = KEYS[1]
local val = ARGV[1]
local ver = tonumber(ARGV[2])
local ttl = tonumber(ARGV[3])

local current_ver = redis.call('HGET', key, '_version')
if (not current_ver) or (ver > tonumber(current_ver)) then
    redis.call('HSET', key, 'data', val, '_version', ver)
    if ttl and ttl > 0 then
        redis.call('EXPIRE', key, ttl)
    end
    return 1 -- Accepted
else
    return 0 -- Rejected: Stale fill attempt
end
"""


@dataclass(frozen=True)
class CacheRecord:
    value: Any
    version: int
    expires_at: Optional[float] = None


class SingleFlight:
    """Coalesces concurrent requests for the exact same key to avoid Dogpile/Stampede."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._in_flight: Dict[str, Tuple[threading.Event, Dict[str, Any]]] = {}

    def do(self, key: str, fn: Callable[[], Any]) -> Any:
        """Executes fn only once for concurrent requests with the same key."""
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
            event.wait()
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
                del self._in_flight[key]
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
            self._rows[record_id] = {"data": data, "version": new_version}
            return new_version

    def read(self, record_id: str) -> Optional[Tuple[Any, int]]:
        with self._lock:
            self.read_count += 1
            row = self._rows.get(record_id)
            if row is None:
                return None
            return row["data"], row["version"]


class VersionedCacheAside:
    """Cache-aside coordinator with version-checked atomic writes and SingleFlight."""

    def __init__(self, db: SimulatedDatabase, redis_client: Any = None) -> None:
        self.db = db
        self.redis = redis_client
        self._memory_cache: Dict[str, CacheRecord] = {}
        self._cache_lock = threading.Lock()
        self.single_flight = SingleFlight()
        self.stale_fill_rejections = 0
        self.cache_hits = 0
        self.cache_misses = 0

    def _execute_lua_in_memory(
        self, key: str, val: Any, ver: int, ttl: Optional[float] = None
    ) -> bool:
        """Exact memory simulation of the Redis Lua script logic."""
        now = time.monotonic()
        with self._cache_lock:
            current = self._memory_cache.get(key)
            if current is not None and current.expires_at and current.expires_at < now:
                current = None
                del self._memory_cache[key]

            if current is None or ver > current.version:
                expires_at = (now + ttl) if ttl and ttl > 0 else None
                self._memory_cache[key] = CacheRecord(value=val, version=ver, expires_at=expires_at)
                return True
            else:
                self.stale_fill_rejections += 1
                return False

    def put_cache(self, key: str, value: Any, version: int, ttl_seconds: float = 300.0) -> bool:
        """Atomically stores value and version only if version > cached_version."""
        if self.redis is not None:
            # Live Redis call with Lua script
            serialized = json.dumps(value)
            res = self.redis.eval(LUA_VERSIONED_SET, 1, key, serialized, version, int(ttl_seconds))
            accepted = bool(res == 1)
            if not accepted:
                self.stale_fill_rejections += 1
            return accepted
        return self._execute_lua_in_memory(key, value, version, ttl=ttl_seconds)

    def get(self, record_id: str, ttl_seconds: float = 300.0) -> Optional[Any]:
        """Fetch item using Cache-Aside with Dogpile protection and stale-fill defense."""
        cache_key = f"record:{record_id}"

        # 1. Check cache first
        cached = self._read_cache(cache_key)
        if cached is not None:
            self.cache_hits += 1
            return cached.value

        self.cache_misses += 1

        # 2. Coalesce concurrent cache misses via SingleFlight to prevent Dogpile
        def loader() -> Optional[Any]:
            # Double check cache inside singleflight in case earlier coalesced caller filled it
            cached_check = self._read_cache(cache_key)
            if cached_check is not None:
                return cached_check.value

            db_result = self.db.read(record_id)
            if db_result is None:
                return None

            val, ver = db_result
            # Attempt versioned write to cache
            self.put_cache(cache_key, val, ver, ttl_seconds=ttl_seconds)
            return val

        return self.single_flight.do(cache_key, loader)

    def update(self, record_id: str, new_data: Any, ttl_seconds: float = 300.0) -> int:
        """Write-through DB update with cache synchronization."""
        new_version = self.db.write(record_id, new_data)
        cache_key = f"record:{record_id}"
        # Update cache atomically with the new version
        self.put_cache(cache_key, new_data, new_version, ttl_seconds=ttl_seconds)
        return new_version

    def invalidate(self, record_id: str) -> None:
        """Evicts a key from cache."""
        cache_key = f"record:{record_id}"
        if self.redis is not None:
            self.redis.delete(cache_key)
        else:
            with self._cache_lock:
                self._memory_cache.pop(cache_key, None)

    def _read_cache(self, key: str) -> Optional[CacheRecord]:
        now = time.monotonic()
        if self.redis is not None:
            raw = self.redis.hgetall(key)
            if not raw:
                return None
            val = json.loads(raw.get(b"data", raw.get("data")))
            ver = int(raw.get(b"_version", raw.get("_version")))
            return CacheRecord(value=val, version=ver)
        else:
            with self._cache_lock:
                rec = self._memory_cache.get(key)
                if rec is None:
                    return None
                if rec.expires_at and rec.expires_at < now:
                    del self._memory_cache[key]
                    return None
                return rec
