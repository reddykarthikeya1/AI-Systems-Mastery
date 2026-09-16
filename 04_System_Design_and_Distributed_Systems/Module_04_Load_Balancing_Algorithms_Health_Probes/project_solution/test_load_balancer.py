"""Unit tests for Layer 4 / Layer 7 Load Balancer Engine."""

from __future__ import annotations

import pytest
from load_balancer import (
    BackendServer,
    HealthStatus,
    IPHashStrategy,
    LeastConnectionsStrategy,
    LoadBalancer,
    RoundRobinStrategy,
    WeightedRoundRobinStrategy,
)


def test_round_robin_distribution() -> None:
    lb = LoadBalancer(strategy=RoundRobinStrategy())
    s1 = BackendServer(server_id="s1", host="10.0.0.1", port=8080)
    s2 = BackendServer(server_id="s2", host="10.0.0.2", port=8080)
    s3 = BackendServer(server_id="s3", host="10.0.0.3", port=8080)

    for s in [s1, s2, s3]:
        lb.register_server(s)

    routed = [lb.route_request().server_id for _ in range(6)]
    assert routed == ["s1", "s2", "s3", "s1", "s2", "s3"]


def test_weighted_round_robin_distribution() -> None:
    lb = LoadBalancer(strategy=WeightedRoundRobinStrategy())
    s1 = BackendServer(server_id="s1", host="10.0.0.1", port=8080, weight=3)
    s2 = BackendServer(server_id="s2", host="10.0.0.2", port=8080, weight=1)

    lb.register_server(s1)
    lb.register_server(s2)

    routed = [lb.route_request().server_id for _ in range(8)]
    # Over 8 requests with 3:1 weights, s1 should receive 6 and s2 should receive 2
    assert routed.count("s1") == 6
    assert routed.count("s2") == 2


def test_least_connections_strategy() -> None:
    lb = LoadBalancer(strategy=LeastConnectionsStrategy())
    s1 = BackendServer(server_id="s1", host="10.0.0.1", port=8080, active_connections=5)
    s2 = BackendServer(server_id="s2", host="10.0.0.2", port=8080, active_connections=1)
    s3 = BackendServer(server_id="s3", host="10.0.0.3", port=8080, active_connections=3)

    for s in [s1, s2, s3]:
        lb.register_server(s)

    # First route goes to s2 (1 connection)
    routed1 = lb.route_request()
    assert routed1.server_id == "s2"
    assert s2.active_connections == 2

    # Second route also goes to s2 (now tied at 2, but s3 has 3)
    routed2 = lb.route_request()
    assert routed2.server_id == "s2"
    assert s2.active_connections == 3


def test_ip_hash_session_affinity() -> None:
    lb = LoadBalancer(strategy=IPHashStrategy())
    s1 = BackendServer(server_id="s1", host="10.0.0.1", port=8080)
    s2 = BackendServer(server_id="s2", host="10.0.0.2", port=8080)

    lb.register_server(s1)
    lb.register_server(s2)

    # The same client IP must consistently map to the same server
    ip_a = "192.168.1.100"
    ip_b = "10.200.5.88"

    target_a1 = lb.route_request(client_ip=ip_a).server_id
    target_a2 = lb.route_request(client_ip=ip_a).server_id
    assert target_a1 == target_a2

    target_b1 = lb.route_request(client_ip=ip_b).server_id
    target_b2 = lb.route_request(client_ip=ip_b).server_id
    assert target_b1 == target_b2


def test_health_check_hysteresis_and_failover() -> None:
    lb = LoadBalancer(strategy=RoundRobinStrategy(), unhealthy_threshold=3, healthy_threshold=2)
    s1 = BackendServer(server_id="s1", host="10.0.0.1", port=8080)
    s2 = BackendServer(server_id="s2", host="10.0.0.2", port=8080)

    lb.register_server(s1)
    lb.register_server(s2)

    # 2 consecutive failures on s1 (below threshold of 3) -> s1 remains HEALTHY
    lb.record_health_result("s1", is_healthy=False)
    lb.record_health_result("s1", is_healthy=False)
    assert s1.status == HealthStatus.HEALTHY

    # 3rd failure -> s1 transitions to UNHEALTHY
    lb.record_health_result("s1", is_healthy=False)
    assert s1.status == HealthStatus.UNHEALTHY
    assert len(lb.healthy_servers()) == 1

    # All traffic now automatically routes exclusively to s2
    for _ in range(5):
        assert lb.route_request().server_id == "s2"

    # s1 recovers: requires 2 consecutive successes
    lb.record_health_result("s1", is_healthy=True)
    assert s1.status == HealthStatus.UNHEALTHY  # only 1 success
    lb.record_health_result("s1", is_healthy=True)
    assert s1.status == HealthStatus.HEALTHY  # 2nd success restored it
    assert len(lb.healthy_servers()) == 2


def test_graceful_draining_stops_new_traffic() -> None:
    lb = LoadBalancer(strategy=RoundRobinStrategy())
    s1 = BackendServer(server_id="s1", host="10.0.0.1", port=8080, active_connections=2)
    s2 = BackendServer(server_id="s2", host="10.0.0.2", port=8080, active_connections=0)

    lb.register_server(s1)
    lb.register_server(s2)

    # Drain s1
    lb.drain_server("s1")
    assert s1.status == HealthStatus.DRAINING
    assert not s1.is_routable

    # New requests only go to s2
    assert lb.route_request().server_id == "s2"

    # In-flight connections on s1 complete
    lb.release_connection("s1")
    lb.release_connection("s1")
    assert s1.active_connections == 0


def test_503_when_no_healthy_servers() -> None:
    lb = LoadBalancer()
    with pytest.raises(RuntimeError, match="503 Service Unavailable"):
        lb.route_request()
