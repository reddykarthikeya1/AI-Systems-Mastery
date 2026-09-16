"""Module 13 Test Suite: Redis Sentinel, Clustering, Lua Scripting & Streams."""

from __future__ import annotations

import pytest
from sentinel_cluster_streams import (
    ClusterMovedError,
    LuaScriptExecutor,
    RedisClusterRouter,
    RedisStreamEngine,
    SentinelCoordinator,
    token_bucket_rate_limiter,
)


def test_cluster_hash_tag_and_slot_computation() -> None:
    # Keys with matching hash tags must yield the exact same slot
    slot_profile = RedisClusterRouter.compute_slot("{user:99}:profile")
    slot_orders = RedisClusterRouter.compute_slot("{user:99}:orders")
    slot_settings = RedisClusterRouter.compute_slot("{user:99}:settings")

    assert slot_profile == slot_orders
    assert slot_orders == slot_settings
    assert 0 <= slot_profile < 16384

    # Different tags should hash across different slots
    slot_user_1 = RedisClusterRouter.compute_slot("{user:1}:profile")
    slot_user_2 = RedisClusterRouter.compute_slot("{user:2}:profile")
    assert slot_user_1 != slot_user_2


def test_cluster_moved_redirection() -> None:
    router = RedisClusterRouter()
    # 3-shard topology
    router.assign_range("node-a", 0, 5460)
    router.assign_range("node-b", 5461, 10922)
    router.assign_range("node-c", 10923, 16383)

    test_key = "{user:99}:profile"
    slot = router.compute_slot(test_key)
    assigned_node = router.get_node_for_key(test_key)

    # Executing on the correct node succeeds
    res = router.execute_command(assigned_node, test_key, "GET")
    assert "OK" in res
    assert assigned_node in res

    # Executing on an incorrect node raises ClusterMovedError
    wrong_node = "node-a" if assigned_node != "node-a" else "node-b"
    with pytest.raises(ClusterMovedError) as exc_info:
        router.execute_command(wrong_node, test_key, "GET")

    assert exc_info.value.slot == slot
    assert exc_info.value.target_node == assigned_node


def test_sentinel_sdown_to_odown_and_promotion() -> None:
    coordinator = SentinelCoordinator(master_id="master-1", quorum=2)
    coordinator.register_replica("replica-1", priority=100, repl_offset=1000)
    coordinator.register_replica("replica-2", priority=100, repl_offset=5000)  # Best eligible
    coordinator.register_replica("replica-3", priority=0, repl_offset=9000)    # Priority 0: ineligible

    # 1 Sentinel reports failure -> Subjective Down (SDOWN)
    coordinator.report_heartbeat("sentinel-1", is_master_alive=False)
    assert coordinator.check_health() == "SDOWN"

    # Cannot failover yet
    with pytest.raises(RuntimeError):
        coordinator.execute_failover()

    # 2nd Sentinel reports failure -> Objective Down (ODOWN)
    coordinator.report_heartbeat("sentinel-2", is_master_alive=False)
    assert coordinator.check_health() == "ODOWN"

    # Failover promotes replica-2 (highest offset among priority > 0)
    promoted = coordinator.execute_failover()
    assert promoted == "replica-2"
    assert coordinator.master_id == "replica-2"
    assert "replica-2" not in coordinator.replicas


def test_lua_atomic_rate_limiter() -> None:
    executor = LuaScriptExecutor()
    src = "local key = KEYS[1] ... simulated token bucket"
    sha = executor.register_script(token_bucket_rate_limiter, src)

    storage: dict = {}
    key = "rate_limit:user:42"

    # Capacity = 3, refill rate = 1 token/sec
    # Request 1 token at t=0 -> Allowed (tokens left: 2)
    res1 = executor.evalsha(sha, [key], [3, 1.0, 1, 0.0], storage)
    assert res1 == 1

    # Request 2 tokens at t=0 -> Allowed (tokens left: 0)
    res2 = executor.evalsha(sha, [key], [3, 1.0, 2, 0.0], storage)
    assert res2 == 1

    # Request 1 token at t=0 -> Rejected (tokens: 0)
    res3 = executor.evalsha(sha, [key], [3, 1.0, 1, 0.0], storage)
    assert res3 == 0

    # Advance time to t=2.0 -> Refills 2 tokens -> Request 1 token -> Allowed!
    res4 = executor.evalsha(sha, [key], [3, 1.0, 1, 2.0], storage)
    assert res4 == 1


def test_streams_consumer_group_and_pel() -> None:
    engine = RedisStreamEngine()
    stream = "events:checkout"
    engine.xadd(stream, {"cart_id": "c1", "total": 100}, entry_id="1-0")
    engine.xadd(stream, {"cart_id": "c2", "total": 250}, entry_id="2-0")
    engine.xadd(stream, {"cart_id": "c3", "total": 499}, entry_id="3-0")

    # Create consumer group
    engine.xgroup_create(stream, "workers")

    # Worker-1 reads 2 events
    delivered = engine.xreadgroup(stream, "workers", "worker-1", count=2, now=100.0)
    assert len(delivered) == 2
    assert delivered[0]["id"] == "1-0"
    assert delivered[1]["id"] == "2-0"

    # PEL has 2 pending unacknowledged entries
    group = engine.consumer_groups[f"{stream}:workers"]
    assert len(group["pel"]) == 2
    assert "1-0" in group["pel"]
    assert "2-0" in group["pel"]

    # Worker-1 acknowledges 1-0
    acked = engine.xack(stream, "workers", ["1-0"])
    assert acked == 1
    assert len(group["pel"]) == 1
    assert "2-0" in group["pel"]


def test_streams_xclaim_dead_consumer() -> None:
    engine = RedisStreamEngine()
    stream = "tasks:email"
    engine.xadd(stream, {"to": "user@example.com", "tmpl": "welcome"}, entry_id="10-0")
    engine.xgroup_create(stream, "mailers")

    # Crashed worker reads message at t=100.0
    _ = engine.xreadgroup(stream, "mailers", "crashed-worker", count=1, now=100.0)

    # At t=5000.0 (idle 4900ms), worker-healthy reclaims messages idle > 2000ms
    reclaimed = engine.xclaim(stream, "mailers", "worker-healthy", min_idle_ms=2000, now=5000.0)
    assert len(reclaimed) == 1
    assert reclaimed[0]["id"] == "10-0"
    assert reclaimed[0]["consumer"] == "worker-healthy"

    # PEL now attributes message to worker-healthy
    group = engine.consumer_groups[f"{stream}:mailers"]
    assert group["pel"]["10-0"]["consumer"] == "worker-healthy"
