"""Tests for Module 12: Real Redis Operational Client & Reconciliation (Track B)."""

from __future__ import annotations

import pytest
from redis_live import RedisLiveClient
from redis_engine import RedisEngine

def _redis_is_up() -> bool:
    try:
        client = RedisLiveClient()
        return client.ping()
    except Exception:
        return False

requires_redis = pytest.mark.skipif(
    not _redis_is_up(),
    reason="Redis server is not reachable on localhost:16379 - start with: make up redis"
)

pytestmark = [pytest.mark.requires_redis, requires_redis]


def test_redis_live_ping():
    client = RedisLiveClient()
    assert client.ping() is True


def test_redis_live_lock_acquire_and_release():
    client = RedisLiveClient()
    lock_key = "test:lock:order_123"

    # Acquire lock
    token = client.acquire_lock(lock_key, ttl_seconds=5)
    assert token is not None

    # Cannot acquire same lock while held
    second_token = client.acquire_lock(lock_key, ttl_seconds=5)
    assert second_token is None

    # Releasing with incorrect token fails
    assert client.release_lock(lock_key, "wrong-token") is False

    # Releasing with valid token succeeds
    assert client.release_lock(lock_key, token) is True

    # Lock can now be re-acquired
    re_token = client.acquire_lock(lock_key, ttl_seconds=5)
    assert re_token is not None
    client.release_lock(lock_key, re_token)


def test_redis_live_leaderboard_rankings():
    client = RedisLiveClient()
    board = "test:leaderboard:m12"
    client.client.delete(board)

    client.update_leaderboard_score(board, "Alice", 2500)
    client.update_leaderboard_score(board, "Bob", 1200)
    client.update_leaderboard_score(board, "Charlie", 3400)

    top = client.get_top_players(board, n=2)
    assert len(top) == 2
    assert top[0][0] == "Charlie"
    assert top[0][1] == 3400.0
    assert top[1][0] == "Alice"

    assert client.get_player_rank(board, "Charlie") == 1
    assert client.get_player_rank(board, "Alice") == 2
    assert client.get_player_rank(board, "Bob") == 3

    client.client.delete(board)


def test_redis_live_sliding_window_rate_limiter():
    client = RedisLiveClient()
    user = "user_42"
    key = f"rate_limit:{user}"
    client.client.delete(key)

    limit = 3
    window = 2  # 2 seconds

    # First 3 requests must pass
    assert client.check_rate_limit(user, limit=limit, window_seconds=window) is True
    assert client.check_rate_limit(user, limit=limit, window_seconds=window) is True
    assert client.check_rate_limit(user, limit=limit, window_seconds=window) is True

    # 4th request in the same window must be rejected
    assert client.check_rate_limit(user, limit=limit, window_seconds=window) is False

    client.client.delete(key)


def test_redis_live_memory_inspection():
    client = RedisLiveClient()
    mem = client.inspect_memory()
    assert "used_memory_bytes" in mem
    assert mem["used_memory_bytes"] > 0
    assert "mem_fragmentation_ratio" in mem


def test_redis_live_safe_scan_keys():
    client = RedisLiveClient()
    prefix = "test:scan_m12:"
    for i in range(15):
        client.client.set(f"{prefix}{i}", f"val_{i}")

    scanned = list(client.safe_scan(match_pattern=f"{prefix}*", count=5))
    assert len(scanned) == 15

    for k in scanned:
        client.client.delete(k)


@pytest.mark.perf
def test_redis_pipeline_speedup_assertion():
    client = RedisLiveClient()
    res = client.benchmark_pipeline_vs_roundtrip(n_commands=300)
    # Pipeline should be noticeably faster than roundtrips
    assert res["pipelined_duration_s"] < res["sequential_duration_s"]
    assert res["pipeline_speedup_factor"] > 1.2


def test_track_a_model_matches_real_redis_reconciliation():
    """Track A <-> Track B reconciliation test: Hand-built SDS & SkipList model vs real Redis."""
    model_engine = RedisEngine()
    live_client = RedisLiveClient()

    test_key = "reconciliation:m12:user"
    live_client.client.delete(test_key)

    # 1. String SET / GET
    model_engine.set(test_key, "Alice")
    live_client.client.set(test_key, "Alice")

    model_val = model_engine.get(test_key)
    live_val = live_client.client.get(test_key)
    assert (model_val.decode("utf-8") if isinstance(model_val, bytes) else model_val) == live_val == "Alice"

    # 2. INCRBY counter
    counter_key = "reconciliation:m12:counter"
    live_client.client.delete(counter_key)
    model_engine.set(counter_key, "10")
    live_client.client.set(counter_key, "10")

    model_inc = model_engine.incrby(counter_key, 5)
    live_inc = live_client.client.incrby(counter_key, 5)
    assert model_inc == live_inc == 15

    # 3. ZSET leaderboard ranking
    board_key = "reconciliation:m12:board"
    live_client.client.delete(board_key)
    model_engine.zadd(board_key, "player1", 100.0)
    model_engine.zadd(board_key, "player2", 200.0)
    live_client.client.zadd(board_key, {"player1": 100.0, "player2": 200.0})

    # Reconcile rank semantics: Redis C implementation uses 0-based rank (0, 1)
    # whereas our pure-Python skip list spans use 1-based rank (1, 2)
    assert model_engine.zrank(board_key, "player1") - 1 == live_client.client.zrank(board_key, "player1") == 0
    assert model_engine.zrank(board_key, "player2") - 1 == live_client.client.zrank(board_key, "player2") == 1

    live_client.client.delete(counter_key, board_key, test_key)
