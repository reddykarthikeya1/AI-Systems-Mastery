"""Runnable exercises for textbook chapters without a dedicated implementation lab."""

import pytest

from chapter_reference_solutions import (
    ApiGateway,
    CDNCache,
    DriverCellIndex,
    GraphANNIndex,
    HashShardRouter,
    LSMStore,
    MultipartObjectStore,
    PartitionedLog,
    PresenceRegistry,
    RaftElection,
    ReplicaGroup,
    RoundRobinBalancer,
    ServiceRegistry,
    TumblingWindowAggregator,
    VectorClock,
    cap_choice,
    estimate_capacity,
    pacelc_choice,
)


def test_round_robin_load_balancing():
    balancer = RoundRobinBalancer(["a", "b", "c"])
    assert [balancer.choose() for _ in range(5)] == ["a", "b", "c", "a", "b"]


def test_cdn_cache_ttl_and_invalidation():
    cache = CDNCache(ttl_seconds=10)
    calls = []
    origin = lambda key: calls.append(key) or f"origin:{key}:{len(calls)}"
    assert cache.get("/logo", now=0, origin=origin) == "origin:/logo:1"
    assert cache.get("/logo", now=9, origin=origin) == "origin:/logo:1"
    assert cache.get("/logo", now=10, origin=origin) == "origin:/logo:2"
    cache.invalidate("/logo")
    assert cache.get("/logo", now=11, origin=origin) == "origin:/logo:3"
    assert len(calls) == 3


def test_hash_shard_routing_is_stable():
    router = HashShardRouter(["s0", "s1", "s2", "s3"])
    assert router.shard_for("customer-42") == router.shard_for("customer-42")
    assert router.shard_for("customer-42") in router.shard_ids


def test_replication_lag_read_your_writes_and_read_repair():
    group = ReplicaGroup(replica_count=1)
    version = group.write("account:1", 100)
    assert group.read("account:1", min_version=version).value == 100
    group.replicate(0)
    group.write("account:1", 125)
    assert group.read("account:1", replica_index=0, min_version=2).value == 125
    assert group.replicas[0]["account:1"].version == 2


def test_cap_and_pacelc_decisions():
    assert cap_choice(partitioned=True, prefer_availability=True) == "AP"
    assert cap_choice(partitioned=True, prefer_availability=False) == "CP"
    assert pacelc_choice(False, True, True) == "EL"
    assert pacelc_choice(True, True, False) == "PA"


def test_vector_clock_causal_order_and_concurrency():
    a = VectorClock({"node-a": 1})
    b = VectorClock({"node-a": 2})
    c = VectorClock({"node-a": 1, "node-b": 1})
    assert a.compare(b) == "BEFORE"
    assert b.compare(a) == "AFTER"
    assert a.compare(c) == "BEFORE"
    assert b.compare(c) == "CONCURRENT"


def test_partitioned_log_offsets_and_consumer_groups():
    log = PartitionedLog(partitions=3)
    first = log.append("user:7", {"message": "hello"})
    second = log.append("user:7", {"message": "world"})
    assert first.partition == second.partition
    assert [r.value["message"] for r in log.poll("chat", first.partition)] == ["hello", "world"]
    log.commit("chat", first.partition, 1)
    assert [r.offset for r in log.poll("chat", first.partition)] == [1]
    assert log.poll("analytics", first.partition)[0].offset == 0


def test_service_discovery_registration():
    registry = ServiceRegistry()
    registry.register("payments", "10.0.0.1:8000")
    registry.register("payments", "10.0.0.2:8000")
    assert registry.resolve("payments") == ("10.0.0.1:8000", "10.0.0.2:8000")
    registry.deregister("payments", "10.0.0.1:8000")
    assert registry.resolve("payments") == ("10.0.0.2:8000",)


def test_api_gateway_authentication_boundary():
    gateway = ApiGateway()
    gateway.add_route("/orders", lambda payload: {"accepted": payload["id"]}, require_auth=True)
    assert gateway.dispatch("/orders", {"id": 7}, authenticated=False)[0] == 401
    assert gateway.dispatch("/orders", {"id": 7}, authenticated=True) == (200, {"accepted": 7})
    assert gateway.dispatch("/missing", {}, authenticated=True)[0] == 404


def test_multipart_object_upload_integrity_and_order():
    store = MultipartObjectStore()
    upload_id = store.begin()
    check_2 = store.upload_part(upload_id, 2, b"world")
    check_1 = store.upload_part(upload_id, 1, b"hello ")
    assert store.complete(upload_id, "greeting.txt", {1: check_1, 2: check_2}) == b"hello world"
    assert store.objects["greeting.txt"] == b"hello world"


def test_multipart_rejects_checksum_mismatch():
    store = MultipartObjectStore()
    upload_id = store.begin()
    store.upload_part(upload_id, 1, b"payload")
    with pytest.raises(ValueError, match="checksum mismatch"):
        store.complete(upload_id, "bad.bin", {1: "wrong"})


def test_back_of_envelope_capacity_estimates():
    estimate = estimate_capacity(
        daily_active_users=100_000,
        requests_per_user=20,
        peak_factor=5,
        average_object_bytes=1_024,
    )
    assert estimate["daily_requests"] == 2_000_000
    assert estimate["peak_rps"] == pytest.approx(2_000_000 / 86_400 * 5)
    assert estimate["daily_storage_bytes"] == 2_048_000_000


def test_graph_ann_retrieves_nearby_vector():
    index = GraphANNIndex(max_neighbors=2)
    index.add("a", [0.0, 0.0])
    index.add("b", [1.0, 1.0])
    index.add("c", [10.0, 10.0])
    results = index.search([0.1, 0.1], entry_id="a", ef=3)
    assert results[0][0] == "a"
    assert {item for item, _ in results} == {"a", "b", "c"}


def test_raft_election_requires_majority_and_one_vote_per_term():
    raft = RaftElection(["n1", "n2", "n3", "n4", "n5"])
    assert raft.elect("n1", term=1, votes=["n1", "n2", "n3"]) is True
    assert raft.leader == "n1"
    # A later candidate cannot collect a second vote from the same nodes in the same term.
    assert raft.elect("n2", term=1, votes=["n1", "n2"]) is False
    assert raft.elect("n2", term=2, votes=["n2", "n3", "n4"]) is True
    assert raft.leader == "n2"


def test_event_time_windows_close_on_watermark():
    agg = TumblingWindowAggregator(window_seconds=10)
    assert agg.add(1.0, 2)
    assert agg.add(7.0, 3)
    assert agg.add(12.0, 4)
    assert agg.advance_watermark(10.0) == {0: 5}
    assert agg.add(5.0, 9) is False
    assert agg.late_events == 1
    assert agg.advance_watermark(20.0) == {10: 4}


def test_lsm_flush_and_compaction_preserve_latest_value():
    store = LSMStore()
    store.put("k", "v1")
    store.flush()
    store.put("k", "v2")
    store.flush()
    store.put("other", "x")
    assert store.get("k") == "v2"
    store.compact()
    assert store.get("k") == "v2"
    assert store.get("other") == "x"
    assert len(store.sstables) == 1


def test_chat_presence_ttl():
    presence = PresenceRegistry()
    presence.heartbeat("user-1", now=100.0)
    assert presence.is_online("user-1", now=109.0, ttl_seconds=10.0)
    assert not presence.is_online("user-1", now=110.0, ttl_seconds=10.0)


def test_ride_hailing_driver_cell_candidates():
    index = DriverCellIndex(cell_size_degrees=0.01)
    index.add_driver("near", 17.385, 78.486)
    index.add_driver("far", 17.45, 78.55)
    candidates = index.candidates(17.386, 78.487, neighboring_cells=1)
    assert "near" in candidates
    assert "far" not in candidates
