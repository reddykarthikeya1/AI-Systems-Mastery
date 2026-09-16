#!/usr/bin/env python3
"""Module 04 Demo: Live Simulation of Load Balancing & Failover."""

import sys
from pathlib import Path

# Add project_solution to sys.path
sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from load_balancer import (
    BackendServer,
    LeastConnectionsStrategy,
    LoadBalancer,
    RoundRobinStrategy,
    WeightedRoundRobinStrategy,
)


def main() -> None:
    print("=" * 70)
    print("  MODULE 04: LOAD BALANCER SIMULATION & FAILOVER DEMO")
    print("=" * 70)

    # 1. Round-Robin vs Weighted Round-Robin
    servers = [
        BackendServer("srv-alpha", "10.0.0.1", 8080, weight=3),
        BackendServer("srv-beta", "10.0.0.2", 8080, weight=1),
        BackendServer("srv-gamma", "10.0.0.3", 8080, weight=2),
    ]

    print("\n--- 1. Weighted Round-Robin Distribution (Weights: Alpha=3, Beta=1, Gamma=2) ---")
    wrr_lb = LoadBalancer(strategy=WeightedRoundRobinStrategy())
    for s in servers:
        wrr_lb.register_server(s)

    for i in range(12):
        srv = wrr_lb.route_request()
        print(f"Request #{i + 1:02d} -> Routed to: {srv.server_id:<10} (Weight: {srv.weight})")

    # 2. Least Connections
    print("\n--- 2. Least Connections Routing Under Uneven Load ---")
    lc_lb = LoadBalancer(strategy=LeastConnectionsStrategy())
    c1 = BackendServer("srv-fast", "10.0.0.10", 8080, active_connections=12)
    c2 = BackendServer("srv-idle", "10.0.0.11", 8080, active_connections=2)
    c3 = BackendServer("srv-busy", "10.0.0.12", 8080, active_connections=8)
    for c in [c1, c2, c3]:
        lc_lb.register_server(c)

    chosen = lc_lb.route_request()
    print(f"Server pool connections: Fast={c1.active_connections}, Idle={c2.active_connections}, Busy={c3.active_connections}")
    print(f"-> LeastConnections selected: {chosen.server_id} (active connections was {chosen.active_connections - 1})")

    # 3. Active Health Check & Automatic Failover
    print("\n--- 3. Active Health Check Failover & Hysteresis ---")
    rr_lb = LoadBalancer(strategy=RoundRobinStrategy(), unhealthy_threshold=3, healthy_threshold=2)
    h1 = BackendServer("node-1", "10.1.0.1", 8080)
    h2 = BackendServer("node-2", "10.1.0.2", 8080)
    rr_lb.register_server(h1)
    rr_lb.register_server(h2)

    print("Initial state: Both node-1 and node-2 healthy.")
    print(f"Request A -> {rr_lb.route_request().server_id}")
    print(f"Request B -> {rr_lb.route_request().server_id}")

    print("\nSimulating node-1 failing health probes (threshold=3)...")
    for probe_num in range(1, 4):
        rr_lb.record_health_result("node-1", is_healthy=False)
        print(f"  Probe #{probe_num} failed -> node-1 status: {h1.status.value}")

    print("Traffic routed after node-1 failed:")
    for _ in range(3):
        print(f"  Request -> {rr_lb.route_request().server_id}")

    print("\nSimulating node-1 recovering...")
    rr_lb.record_health_result("node-1", is_healthy=True)
    print(f"  Recovery probe #1 -> node-1 status: {h1.status.value} (still unhealthy, needs 2)")
    rr_lb.record_health_result("node-1", is_healthy=True)
    print(f"  Recovery probe #2 -> node-1 status: {h1.status.value} (restored to healthy)")

    print(f"Next request after recovery -> {rr_lb.route_request().server_id}")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
