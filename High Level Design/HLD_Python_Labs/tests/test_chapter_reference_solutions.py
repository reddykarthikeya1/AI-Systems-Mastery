"""Runnable exercises for textbook chapters without a dedicated implementation lab."""

import pytest

from chapter_reference_solutions import (
    ApiGateway,
    BackendHealthMonitor,
    BackendHealthState,
    CDNCache,
    DriverCellIndex,
    GraphANNIndex,
    HashShardRouter,
    HierarchicalRateLimiter,
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
    WeightedRoundRobinBalancer,
    cap_choice,
    estimate_capacity,
    littles_law_concurrency,
    pacelc_choice,
)


def test_round_robin_load_balancing():
    balancer = RoundRobinBalancer(["a", "b", "c"])
    assert [balancer.choose() for _ in range(5)] == ["a", "b", "c", "a", "b"]


def test_weighted_round_robin_distribution():
    balancer = WeightedRoundRobinBalancer({"srv-a": 4, "srv-b": 2, "srv-c": 1})
    counts = {"srv-a": 0, "srv-b": 0, "srv-c": 0}
    for _ in range(70):
        choice = balancer.choose()
        counts[choice] += 1
    assert counts == {"srv-a": 40, "srv-b": 20, "srv-c": 10}


def test_backend_health_state_transitions():
    monitor = BackendHealthMonitor(["srv-1", "srv-2"], suspect_threshold=2, eject_threshold=3, recovery_threshold=2)
    assert monitor.healthy_backends() == ["srv-1", "srv-2"]
    assert monitor.routable_backends() == ["srv-1", "srv-2"]

    # 1st failure: remains HEALTHY
    assert monitor.record_failure("srv-1") == BackendHealthState.HEALTHY
    # 2nd failure: transitions to SUSPECT
    assert monitor.record_failure("srv-1") == BackendHealthState.SUSPECT
    assert monitor.healthy_backends() == ["srv-2"]
    assert "srv-1" in monitor.routable_backends()

    # 3 more failures: srv-1 ejected
    monitor.record_failure("srv-1")
    monitor.record_failure("srv-1")
    assert monitor.record_failure("srv-1") == BackendHealthState.EJECTED
    assert "srv-1" not in monitor.routable_backends()

    # Recovery: 2 successes -> SUSPECT, then 2 successes -> HEALTHY
    assert monitor.record_success("srv-1") == BackendHealthState.EJECTED
    assert monitor.record_success("srv-1") == BackendHealthState.SUSPECT
    assert "srv-1" in monitor.routable_backends()
    assert monitor.record_success("srv-1") == BackendHealthState.SUSPECT
    assert monitor.record_success("srv-1") == BackendHealthState.HEALTHY
    assert monitor.healthy_backends() == ["srv-1", "srv-2"]


def test_littles_law_concurrency_calculation():
    # 2,000 RPS with 350ms mean latency -> 700 concurrent requests
    concurrency = littles_law_concurrency(arrival_rate_rps=2000.0, mean_latency_seconds=0.350)
    assert concurrency == pytest.approx(700.0)

    # With 0 RPS or 0 latency
    assert littles_law_concurrency(0.0, 0.5) == 0.0
    assert littles_law_concurrency(100.0, 0.0) == 0.0

    with pytest.raises(ValueError, match="non-negative"):
        littles_law_concurrency(-10.0, 0.2)


def test_hierarchical_rate_limiter_multilevel_enforcement():
    # Global: 10 req, Tenant: 5 req, IP: 2 req
    limiter = HierarchicalRateLimiter(
        global_capacity=10.0,
        global_refill_rate=1.0,
        tenant_capacity=5.0,
        tenant_refill_rate=1.0,
        ip_capacity=2.0,
        ip_refill_rate=1.0,
    )

    t0 = 100.0
    # IP tier allows 2 requests
    ok, reason = limiter.acquire("tenant_acme", "192.168.1.1", tokens=1, now=t0)
    assert ok is True and reason == "ALLOWED"

    ok, reason = limiter.acquire("tenant_acme", "192.168.1.1", tokens=1, now=t0)
    assert ok is True and reason == "ALLOWED"

    # 3rd request from same IP is rejected by IP limit
    ok, reason = limiter.acquire("tenant_acme", "192.168.1.1", tokens=1, now=t0)
    assert ok is False and reason == "IP_LIMIT_EXCEEDED"

    # Different IP under same tenant succeeds
    ok, reason = limiter.acquire("tenant_acme", "192.168.1.2", tokens=2, now=t0)
    assert ok is True and reason == "ALLOWED"

    # Tenant has now consumed 1 + 1 + 2 = 4 tokens out of 5. Next 2 tokens exceeds tenant limit!
    ok, reason = limiter.acquire("tenant_acme", "192.168.1.3", tokens=2, now=t0)
    assert ok is False and reason == "TENANT_LIMIT_EXCEEDED"

    # Different tenant succeeds (has separate 5 token capacity)
    ok, reason = limiter.acquire("tenant_beta", "10.0.0.1", tokens=2, now=t0)
    assert ok is True and reason == "ALLOWED"

    # Global limit has now consumed 4 (acme) + 2 (beta) = 6 tokens out of 10.
    # Requesting 5 tokens exceeds remaining global capacity (4 available)
    ok, reason = limiter.acquire("tenant_beta", "10.0.0.2", tokens=5, now=t0)
    assert ok is False and reason == "GLOBAL_LIMIT_EXCEEDED"


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


def test_round_robin_balancer_invalid_backends():
    with pytest.raises(ValueError, match="backends must be non-empty and unique"):
        RoundRobinBalancer([])
    with pytest.raises(ValueError, match="backends must be non-empty and unique"):
        RoundRobinBalancer(["a", "a"])


def test_vector_clock_tick_and_monotonicity():
    vc = VectorClock({"node-a": 1})
    vc.tick("node-a")
    assert vc.counters["node-a"] == 2
    vc.tick("node-b")
    assert vc.counters["node-b"] == 1


def test_partitioned_log_backwards_offset_rejected():
    log = PartitionedLog(partitions=2)
    log.append("k1", "v1")
    log.commit("g1", 0, 1)
    with pytest.raises(ValueError, match="consumer offsets cannot move backwards"):
        log.commit("g1", 0, 0)
    with pytest.raises(ValueError, match="next_offset is outside the partition log"):
        log.commit("g1", 0, 999)


def test_tumbling_window_backwards_watermark_rejected():
    agg = TumblingWindowAggregator(window_seconds=10)
    agg.advance_watermark(50.0)
    with pytest.raises(ValueError, match="watermark cannot move backwards"):
        agg.advance_watermark(40.0)


def test_lsm_store_empty_compaction_and_lookup_missing():
    store = LSMStore()
    assert store.get("missing_key") is None
    store.compact()
    assert store.sstables == []


def test_hierarchical_rate_limiter_concurrent_same_ip_barrier():
    import threading

    limiter = HierarchicalRateLimiter(
        global_capacity=100.0,
        global_refill_rate=1.0,
        tenant_capacity=50.0,
        tenant_refill_rate=1.0,
        ip_capacity=5.0,
        ip_refill_rate=0.01,
    )

    thread_count = 15
    barrier = threading.Barrier(thread_count)
    results: List[Tuple[bool, str]] = []
    lock = threading.Lock()

    def worker():
        barrier.wait()
        res = limiter.acquire("tenant_alpha", "10.0.0.1", tokens=1, now=10.0)
        with lock:
            results.append(res)

    threads = [threading.Thread(target=worker) for _ in range(thread_count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    successes = [r for r in results if r[0] is True]
    failures = [r for r in results if r[0] is False]

    assert len(successes) == 5
    assert len(failures) == 10
    assert all(r[1] == "IP_LIMIT_EXCEEDED" for r in failures)
    assert limiter.ip_tokens["tenant_alpha:10.0.0.1"] == 0.0


def test_hierarchical_rate_limiter_different_ips_sharing_tenant_barrier():
    import threading

    limiter = HierarchicalRateLimiter(
        global_capacity=100.0,
        global_refill_rate=1.0,
        tenant_capacity=6.0,
        tenant_refill_rate=0.01,
        ip_capacity=4.0,
        ip_refill_rate=0.01,
    )

    thread_count = 12
    barrier = threading.Barrier(thread_count)
    results: List[Tuple[bool, str]] = []
    lock = threading.Lock()

    def worker(client_ip: str):
        barrier.wait()
        res = limiter.acquire("tenant_beta", client_ip, tokens=1, now=10.0)
        with lock:
            results.append(res)

    threads = [
        threading.Thread(target=worker, args=(f"192.168.1.{i % 4}",))
        for i in range(thread_count)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    successes = [r for r in results if r[0] is True]
    failures = [r for r in results if r[0] is False]
    assert len(successes) == 6  # Capped at tenant capacity of 6
    assert len(failures) == 6
    assert all(r[1] == "TENANT_LIMIT_EXCEEDED" for r in failures)
    assert limiter.tenant_tokens["tenant_beta"] == 0.0


def test_hierarchical_rate_limiter_different_tenants_sharing_global_barrier():
    import threading

    limiter = HierarchicalRateLimiter(
        global_capacity=8.0,
        global_refill_rate=0.01,
        tenant_capacity=5.0,
        tenant_refill_rate=0.01,
        ip_capacity=5.0,
        ip_refill_rate=0.01,
    )

    thread_count = 16
    barrier = threading.Barrier(thread_count)
    results: List[Tuple[bool, str]] = []
    lock = threading.Lock()

    def worker(tenant_id: str, client_ip: str):
        barrier.wait()
        res = limiter.acquire(tenant_id, client_ip, tokens=1, now=10.0)
        with lock:
            results.append(res)

    threads = [
        threading.Thread(target=worker, args=(f"tenant_{i % 4}", f"10.0.{i}.1"))
        for i in range(thread_count)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    successes = [r for r in results if r[0] is True]
    failures = [r for r in results if r[0] is False]
    assert len(successes) == 8  # Strictly capped at global capacity of 8
    assert len(failures) == 8
    assert all(r[1] == "GLOBAL_LIMIT_EXCEEDED" for r in failures)
    assert limiter.global_tokens == 0.0


def test_hierarchical_rate_limiter_simultaneous_requests_exhaust_global():
    import threading

    limiter = HierarchicalRateLimiter(
        global_capacity=6.0,
        global_refill_rate=0.01,
        tenant_capacity=10.0,
        tenant_refill_rate=0.01,
        ip_capacity=10.0,
        ip_refill_rate=0.01,
    )

    thread_count = 18
    barrier = threading.Barrier(thread_count)
    results: List[Tuple[bool, str]] = []
    lock = threading.Lock()

    def worker(i: int):
        barrier.wait()
        res = limiter.acquire(f"tenant_{i % 3}", f"10.0.{i}.1", tokens=1, now=10.0)
        with lock:
            results.append(res)

    threads = [
        threading.Thread(target=worker, args=(i,))
        for i in range(thread_count)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    successes = [r for r in results if r[0] is True]
    failures = [r for r in results if r[0] is False]

    assert len(successes) == 6
    assert len(failures) == 12
    assert all(r[1] == "GLOBAL_LIMIT_EXCEEDED" for r in failures)
    assert limiter.global_tokens == 0.0


def test_hierarchical_rate_limiter_rejected_requests_do_not_consume_tokens():
    limiter = HierarchicalRateLimiter(
        global_capacity=20.0,
        global_refill_rate=1.0,
        tenant_capacity=10.0,
        tenant_refill_rate=1.0,
        ip_capacity=2.0,
        ip_refill_rate=1.0,
    )

    t0 = 100.0
    # Acquire 2 tokens from IP 1 (succeeds)
    assert limiter.acquire("t1", "10.0.0.1", tokens=2, now=t0)[0] is True
    assert limiter.global_tokens == 18.0
    assert limiter.tenant_tokens["t1"] == 8.0

    # 3rd token from same IP is rejected by IP limit
    ok, reason = limiter.acquire("t1", "10.0.0.1", tokens=1, now=t0)
    assert ok is False
    assert reason == "IP_LIMIT_EXCEEDED"

    # Global and tenant tokens must NOT have been deducted!
    assert limiter.global_tokens == 18.0
    assert limiter.tenant_tokens["t1"] == 8.0

    # Different IPs under same tenant acquire remaining tokens up to tenant capacity (2 tokens each)
    assert limiter.acquire("t1", "10.0.0.2", tokens=2, now=t0)[0] is True
    assert limiter.acquire("t1", "10.0.0.3", tokens=2, now=t0)[0] is True
    assert limiter.acquire("t1", "10.0.0.4", tokens=2, now=t0)[0] is True
    assert limiter.acquire("t1", "10.0.0.5", tokens=2, now=t0)[0] is True
    assert limiter.tenant_tokens["t1"] == 0.0
    assert limiter.global_tokens == 10.0

    # Now IP 6 under tenant t1 requests 1 token -> rejected by tenant
    ok, reason = limiter.acquire("t1", "10.0.0.6", tokens=1, now=t0)
    assert ok is False
    assert reason == "TENANT_LIMIT_EXCEEDED"
    assert limiter.tenant_tokens["t1"] == 0.0
    # Global tokens must NOT have been deducted!
    assert limiter.global_tokens == 10.0

    # Another tenant (t2) can still use global tokens!
    assert limiter.acquire("t2", "10.0.1.1", tokens=2, now=t0)[0] is True
    assert limiter.global_tokens == 8.0


def test_hierarchical_rate_limiter_zero_and_negative_costs_rejected():
    limiter = HierarchicalRateLimiter(10.0, 1.0, 5.0, 1.0, 2.0, 1.0)

    with pytest.raises(ValueError, match="tokens must be a positive finite number"):
        limiter.acquire("t1", "ip1", tokens=0)

    with pytest.raises(ValueError, match="tokens must be a positive finite number"):
        limiter.acquire("t1", "ip1", tokens=-1)

    with pytest.raises(ValueError, match="tokens must be a positive finite number"):
        limiter.acquire("t1", "ip1", tokens=float("nan"))

    with pytest.raises(ValueError, match="tokens must be a positive finite number"):
        limiter.acquire("t1", "ip1", tokens=float("inf"))

    with pytest.raises(TypeError, match="tokens must be a number"):
        limiter.acquire("t1", "ip1", tokens="1")  # type: ignore


def test_hierarchical_rate_limiter_invalid_capacities_and_refill_rates():
    with pytest.raises(ValueError, match="global_capacity must be a positive finite number"):
        HierarchicalRateLimiter(0.0, 1.0, 5.0, 1.0, 2.0, 1.0)

    with pytest.raises(ValueError, match="global_refill_rate must be a positive finite number"):
        HierarchicalRateLimiter(10.0, 0.0, 5.0, 1.0, 2.0, 1.0)

    with pytest.raises(ValueError, match="global_refill_rate must be a positive finite number"):
        HierarchicalRateLimiter(10.0, -1.0, 5.0, 1.0, 2.0, 1.0)

    with pytest.raises(TypeError, match="tenant_capacity must be a number"):
        HierarchicalRateLimiter(10.0, 1.0, "5.0", 1.0, 2.0, 1.0)  # type: ignore

    with pytest.raises(ValueError, match="ip_capacity must be a positive finite number"):
        HierarchicalRateLimiter(10.0, 1.0, 5.0, 1.0, float("inf"), 1.0)

    limiter = HierarchicalRateLimiter(10.0, 1.0, 5.0, 1.0, 2.0, 1.0)
    with pytest.raises(ValueError, match="tenant_id must be a non-empty string"):
        limiter.acquire("", "10.0.0.1")
    with pytest.raises(TypeError, match="tenant_id must be a string"):
        limiter.acquire(None, "10.0.0.1")  # type: ignore
    with pytest.raises(ValueError, match="client_ip must be a non-empty string"):
        limiter.acquire("t1", "")
    with pytest.raises(TypeError, match="client_ip must be a string"):
        limiter.acquire("t1", 123)  # type: ignore
    with pytest.raises(ValueError, match="now must be a non-negative finite number"):
        limiter.acquire("t1", "10.0.0.1", now=-1.0)
    with pytest.raises(ValueError, match="now must be a non-negative finite number"):
        limiter.acquire("t1", "10.0.0.1", now=float("nan"))
    with pytest.raises(TypeError, match="now must be a number"):
        limiter.acquire("t1", "10.0.0.1", now="10.0")  # type: ignore


def test_hierarchical_rate_limiter_backward_timestamps_handled_safely():
    limiter = HierarchicalRateLimiter(10.0, 1.0, 10.0, 1.0, 10.0, 1.0)

    # First request at t = 100.0
    assert limiter.acquire("t1", "ip1", tokens=5, now=100.0)[0] is True
    assert limiter.global_tokens == 5.0

    # Backward timestamp at t = 50.0: should clamp delta to 0, NOT deduct or add negative tokens
    assert limiter.acquire("t1", "ip1", tokens=2, now=50.0)[0] is True
    assert limiter.global_tokens == 3.0

    # Advanced timestamp at t = 102.0: refills 2.0 tokens from t=100
    assert limiter.acquire("t1", "ip1", tokens=1, now=102.0)[0] is True
    assert limiter.global_tokens == 4.0  # 3.0 + 2.0 refilled - 1.0 = 4.0


def test_hierarchical_rate_limiter_exact_refill_boundaries():
    limiter = HierarchicalRateLimiter(
        global_capacity=5.0,
        global_refill_rate=2.0,  # 2 tokens per second
        tenant_capacity=5.0,
        tenant_refill_rate=2.0,
        ip_capacity=5.0,
        ip_refill_rate=2.0,
    )

    # Empty all 5 tokens at t=0
    assert limiter.acquire("t1", "ip1", tokens=5, now=0.0)[0] is True
    assert limiter.acquire("t1", "ip1", tokens=1, now=0.0)[0] is False

    # After exactly 0.5s: 1.0 token refilled
    assert limiter.acquire("t1", "ip1", tokens=1, now=0.5)[0] is True
    assert limiter.acquire("t1", "ip1", tokens=1, now=0.5)[0] is False

    # After 1.5s total (1.0s elapsed since t=0.5): 2.0 tokens refilled
    assert limiter.acquire("t1", "ip1", tokens=2, now=1.5)[0] is True
    assert limiter.acquire("t1", "ip1", tokens=1, now=1.5)[0] is False


