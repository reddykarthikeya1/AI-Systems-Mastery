"""Property and performance assertions for Load Balancing Algorithms & Health Probes.

These complement the correctness tests in `test_load_balancer.py`. A correctness test says
the operation does the right thing; these say the *claim the module makes about
it* is true - and they fail when it stops being true.

    pytest -m perf -v          # just the performance assertions
    pytest -m "not slow" -q    # skip the long ones
"""

from __future__ import annotations

import pytest
from load_balancer import (
    BackendServer,
    LeastConnectionsStrategy,
    LoadBalancer,
    RoundRobinStrategy,
)


def _servers(n: int = 3) -> list[BackendServer]:
    return [BackendServer(server_id=f"s{i}", host=f"10.0.0.{i}", port=80) for i in range(n)]


def test_round_robin_distributes_request_counts_evenly() -> None:
    lb = LoadBalancer(strategy=RoundRobinStrategy())
    for s in _servers():
        lb.register_server(s)
    picks = [lb.route_request(client_ip="1.2.3.4") for _ in range(300)]
    assert all(p is not None for p in picks)
    counts: dict[str, int] = {}
    for p in picks:
        if p:
            counts[p.server_id] = counts.get(p.server_id, 0) + 1
    assert max(counts.values()) - min(counts.values()) <= 1


@pytest.mark.perf
def test_least_connections_beats_round_robin_under_uneven_hold_times() -> None:
    """Equal request *counts* are not equal *load*.

    Round-robin keeps sending to a backend that is still holding connections.
    Least-connections looks at what is actually outstanding. Measured as the
    worst-case concurrent depth on any single backend.
    """

    def peak_depth(strategy) -> int:
        lb = LoadBalancer(strategy=strategy)
        for s in _servers(3):
            lb.register_server(s)
        outstanding: dict[str, int] = {f"s{i}": 0 for i in range(3)}
        worst = 0
        for i in range(180):
            try:
                chosen = lb.route_request(client_ip="1.2.3.4")
            except RuntimeError:
                continue
            outstanding[chosen.server_id] += 1
            worst = max(worst, outstanding[chosen.server_id])
            # every 3rd request completes quickly; the rest linger
            if i % 3 == 0:
                outstanding[chosen.server_id] -= 1
                lb.release_connection(chosen.server_id)
        return worst

    rr = peak_depth(RoundRobinStrategy())
    lc = peak_depth(LeastConnectionsStrategy())
    assert lc <= rr, (
        f"least-connections peaked at {lc} concurrent vs round-robin {rr}. "
        "It must not be worse, or it is not doing its job."
    )


def test_an_unhealthy_server_is_removed_from_rotation() -> None:
    lb = LoadBalancer(strategy=RoundRobinStrategy(), unhealthy_threshold=1)
    for s in _servers(2):
        lb.register_server(s)
    lb.record_health_result("s0", is_healthy=False)
    picks = {lb.route_request(client_ip="1.1.1.1").server_id for _ in range(20)}
    assert "s0" not in picks


def test_a_recovered_server_returns_to_rotation() -> None:
    lb = LoadBalancer(strategy=RoundRobinStrategy(), unhealthy_threshold=1, healthy_threshold=1)
    for s in _servers(2):
        lb.register_server(s)
    lb.record_health_result("s0", is_healthy=False)
    lb.record_health_result("s0", is_healthy=True)
    picks = {lb.route_request(client_ip="1.1.1.1").server_id for _ in range(20)}
    assert "s0" in picks


def test_routing_with_every_backend_down_raises_a_503_signal() -> None:
    """Total outage must be an explicit, catchable decision - never a silent None.

    Returning None here would let a caller forward it downstream and fail far
    from the cause. This implementation raises, so the 503 is decided at the
    place that knows why.
    """
    lb = LoadBalancer(strategy=RoundRobinStrategy(), unhealthy_threshold=1)
    for s in _servers(2):
        lb.register_server(s)
    lb.record_health_result("s0", is_healthy=False)
    lb.record_health_result("s1", is_healthy=False)
    with pytest.raises(RuntimeError, match="503"):
        lb.route_request(client_ip="1.1.1.1")


def test_draining_a_server_stops_new_requests() -> None:
    """Drain is how you deploy without dropping in-flight work."""
    lb = LoadBalancer(strategy=RoundRobinStrategy())
    for s in _servers(2):
        lb.register_server(s)
    lb.drain_server("s0")
    picks = {lb.route_request(client_ip="1.1.1.1").server_id for _ in range(20)}
    assert "s0" not in picks
