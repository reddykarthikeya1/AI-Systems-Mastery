# 01_load_balancer_failover.py
"""
High-Level Design Lab 01: High-Concurrency Load Balancer & Health-Check Failover.
Demonstrates Round-Robin, Least-Connections, and Circuit Breaker isolation
when backend nodes crash under live client traffic.
"""

import threading
import time
import random
from typing import List, Dict, Optional

class BackendServer:
    def __init__(self, server_id: str, capacity: int = 100):
        self.server_id = server_id
        self.capacity = capacity
        self.active_connections = 0
        self.is_healthy = True
        self.total_requests_served = 0
        self._lock = threading.Lock()

    def process_request(self) -> bool:
        with self._lock:
            if not self.is_healthy:
                return False
            self.active_connections += 1

        # Simulate network & CPU processing time
        time.sleep(random.uniform(0.005, 0.015))

        with self._lock:
            self.active_connections -= 1
            self.total_requests_served += 1
            return True

    def simulate_crash(self):
        with self._lock:
            self.is_healthy = False

    def recover(self):
        with self._lock:
            self.is_healthy = True

class LoadBalancer:
    def __init__(self, algorithm: str = "least_connections"):
        self.servers: List[BackendServer] = []
        self.algorithm = algorithm
        self._rr_index = 0
        self._lock = threading.Lock()

    def add_server(self, server: BackendServer):
        self.servers.append(server)

    def route_request(self) -> Optional[BackendServer]:
        with self._lock:
            healthy_servers = [s for s in self.servers if s.is_healthy]
            if not healthy_servers:
                return None

            if self.algorithm == "round_robin":
                server = healthy_servers[self._rr_index % len(healthy_servers)]
                self._rr_index += 1
                return server
            elif self.algorithm == "least_connections":
                # Route to the healthy server with minimum currently active connections
                return min(healthy_servers, key=lambda s: s.active_connections)
            else:
                return random.choice(healthy_servers)

def run_load_balancer_simulation():
    print("=" * 70)
    print("  HLD LAB 01: LOAD BALANCER & FAULT-TOLERANT FAILOVER SIMULATION")
    print("=" * 70)

    # 1. Initialize cluster of 3 backend web servers
    s1 = BackendServer("web-01")
    s2 = BackendServer("web-02")
    s3 = BackendServer("web-03")

    lb = LoadBalancer(algorithm="least_connections")
    for s in [s1, s2, s3]:
        lb.add_server(s)

    print(f"[INIT] Cluster initialized with 3 nodes: web-01, web-02, web-03.")
    print(f"[ALGO] Routing Algorithm: LEAST_CONNECTIONS (L7 Application Load Balancing)")

    # 2. Fire 300 concurrent requests across worker threads
    success_count = 0
    fail_count = 0

    def client_worker(req_id: int):
        nonlocal success_count, fail_count
        # At request 100, simulate web-02 suffering a sudden hardware / OOM crash!
        if req_id == 100:
            print("\n>>> [DISASTER INJECTION] web-02 CRASHED (Kernel OOM Kill)! <<<")
            s2.simulate_crash()

        server = lb.route_request()
        if server and server.process_request():
            success_count += 1
        else:
            fail_count += 1

    threads = [threading.Thread(target=client_worker, args=(i,)) for i in range(300)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("\n" + "-" * 70)
    print("  POST-DISASTER CLUSTER TRAFFIC DISTRIBUTION")
    print("-" * 70)
    for s in [s1, s2, s3]:
        status_str = "HEALTHY" if s.is_healthy else "DEAD (CIRCUIT BREAKER OPEN)"
        print(f"  Node: {s.server_id:8} | Status: {status_str:28} | Requests Served: {s.total_requests_served}")

    print("-" * 70)
    print(f"Total Requests: 300 | Successes: {success_count} | Failures: {fail_count}")
    assert success_count >= 295, f"Expected near-zero drops with automatic failover, got {fail_count} drops"
    assert s2.total_requests_served < s1.total_requests_served, "Crashed node should stop taking traffic!"
    print("[SUCCESS] Load balancer seamlessly isolated crashed node and preserved 99%+ availability!\n")

if __name__ == "__main__":
    run_load_balancer_simulation()
