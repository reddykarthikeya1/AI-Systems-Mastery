"""Module 12: Real Redis Operational Client & Production Patterns (Track B).

Interacts directly with a live Redis instance using redis-py. Demonstrates:
1. Pipeline batching vs sequential round-trip network latency measurement.
2. Production SETNX distributed lock with TTL and atomic Lua release.
3. Sorted Set (ZSET) real-time gaming/financial leaderboard.
4. Sliding-window rate limiter utilizing microsecond ZSET timestamps.
5. Memory fragmentation & RSS inspection via INFO memory.
6. SCAN cursor iteration vs dangerous blocking KEYS pattern.
"""

from __future__ import annotations

import os

import time
import uuid
from typing import Any, Generator

try:
    import redis
except ImportError:
    redis = None  # type: ignore


class RedisLiveClient:
    """Production Redis client wrapper demonstrating operational patterns."""

    def __init__(self, host: str = os.environ.get("COURSE_DB_HOST", "localhost"), port: int = int(os.environ.get("COURSE_REDIS_PORT", "16379")), db: int = 0):
        if redis is None:
            raise RuntimeError("redis package is not installed. Install with: pip install redis")
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def ping(self) -> bool:
        """Check Redis connectivity."""
        try:
            return bool(self.client.ping())
        except Exception:
            return False

    def benchmark_pipeline_vs_roundtrip(self, n_commands: int = 500) -> dict[str, float]:
        """Compares sequential round-trips vs a single batched pipeline."""
        pipe_key = "bench:pipe"
        seq_key = "bench:seq"

        # Sequential round-trips
        start_seq = time.perf_counter()
        for i in range(n_commands):
            self.client.set(f"{seq_key}:{i}", f"val_{i}")
        seq_time = time.perf_counter() - start_seq

        # Pipelined batch
        start_pipe = time.perf_counter()
        pipeline = self.client.pipeline(transaction=False)
        for i in range(n_commands):
            pipeline.set(f"{pipe_key}:{i}", f"val_{i}")
        pipeline.execute()
        pipe_time = time.perf_counter() - start_pipe

        # Cleanup
        with self.client.pipeline(transaction=False) as cleanup_pipe:
            for i in range(n_commands):
                cleanup_pipe.delete(f"{seq_key}:{i}", f"{pipe_key}:{i}")
            cleanup_pipe.execute()

        speedup = seq_time / pipe_time if pipe_time > 0 else float("inf")
        return {
            "n_commands": float(n_commands),
            "sequential_duration_s": seq_time,
            "pipelined_duration_s": pipe_time,
            "pipeline_speedup_factor": speedup,
        }

    def acquire_lock(self, lock_key: str, ttl_seconds: int = 10) -> str | None:
        """Acquires a distributed lock using SETNX + EX."""
        token = str(uuid.uuid4())
        # SET key value NX EX ttl
        acquired = self.client.set(lock_key, token, nx=True, ex=ttl_seconds)
        return token if acquired else None

    def release_lock(self, lock_key: str, token: str) -> bool:
        """Releases the lock atomically using Lua so we never delete another client's expired lock."""
        lua_release = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        result = self.client.eval(lua_release, 1, lock_key, token)
        return bool(result)

    # Leaderboard methods (ZSET)
    def update_leaderboard_score(self, board_key: str, member: str, score: float) -> float:
        self.client.zadd(board_key, {member: score})
        return float(self.client.zscore(board_key, member) or 0.0)

    def get_top_players(self, board_key: str, n: int = 5) -> list[tuple[str, float]]:
        return self.client.zrevrange(board_key, 0, n - 1, withscores=True)

    def get_player_rank(self, board_key: str, member: str) -> int | None:
        """Returns 1-based rank (1 is highest score)."""
        rank = self.client.zrevrank(board_key, member)
        return rank + 1 if rank is not None else None

    # Sliding-window Rate Limiter
    def check_rate_limit(self, user_id: str, limit: int, window_seconds: int) -> bool:
        """Implements sliding-window rate limiting via Redis ZSET timestamps."""
        key = f"rate_limit:{user_id}"
        now = time.time()
        clear_before = now - window_seconds
        req_id = f"{now}-{uuid.uuid4().hex[:8]}"

        pipe = self.client.pipeline(transaction=True)
        # 1. Remove old timestamps outside the window
        pipe.zremrangebyscore(key, 0, clear_before)
        # 2. Count current entries
        pipe.zcard(key)
        # 3. Add current timestamp
        pipe.zadd(key, {req_id: now})
        # 4. Refresh key TTL
        pipe.expire(key, window_seconds + 1)
        results = pipe.execute()

        current_count = results[1]
        if current_count >= limit:
            # Over quota -> reject
            self.client.zrem(key, req_id)
            return False
        return True

    # Memory inspection
    def inspect_memory(self) -> dict[str, Any]:
        """Returns parsed INFO memory metrics."""
        info = self.client.info("memory")
        return {
            "used_memory_bytes": info.get("used_memory", 0),
            "used_memory_human": info.get("used_memory_human", "0B"),
            "used_memory_peak_human": info.get("used_memory_peak_human", "0B"),
            "mem_fragmentation_ratio": info.get("mem_fragmentation_ratio", 1.0),
        }

    # SCAN vs KEYS
    def safe_scan(self, match_pattern: str = "*", count: int = 100) -> Generator[str, None, None]:
        """Non-blocking cursor-based iteration over keyspace."""
        cursor = 0
        while True:
            cursor, keys = self.client.scan(cursor=cursor, match=match_pattern, count=count)
            for k in keys:
                yield k
            if cursor == 0:
                break
