#!/usr/bin/env python3
"""Module 04: In-Process Architectural Simulation Model: Layer 4 / Layer 7 Load Balancer Engine.

Implements core load balancing strategies, active health checking, and
graceful connection draining.
"""

from __future__ import annotations

import hashlib
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class HealthStatus(StrEnum):
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"
    DRAINING = "DRAINING"


@dataclass
class BackendServer:
    server_id: str
    host: str
    port: int
    weight: int = 1
    active_connections: int = 0
    total_requests_served: int = 0
    status: HealthStatus = HealthStatus.HEALTHY
    consecutive_failures: int = 0
    consecutive_successes: int = 0

    @property
    def is_routable(self) -> bool:
        """Server can receive new traffic only if strictly HEALTHY."""
        return self.status == HealthStatus.HEALTHY


class LoadBalancingStrategy(Protocol):
    """Protocol for pluggable balancing algorithms."""

    def select(
        self,
        servers: list[BackendServer],
        client_ip: str | None = None,
    ) -> BackendServer | None: ...


class RoundRobinStrategy:
    """Standard stateless round-robin distribution with atomic index rotation."""

    def __init__(self) -> None:
        self._index = 0
        self._lock = threading.Lock()

    def select(
        self,
        servers: list[BackendServer],
        client_ip: str | None = None,
    ) -> BackendServer | None:
        routable = [s for s in servers if s.is_routable]
        if not routable:
            return None

        with self._lock:
            selected = routable[self._index % len(routable)]
            self._index = (self._index + 1) % len(routable)
            return selected


class WeightedRoundRobinStrategy:
    """Weighted Round-Robin using NGINX-style smooth deficit / credit allocation."""

    def __init__(self) -> None:
        self._current_weights: dict[str, int] = {}
        self._lock = threading.Lock()

    def select(
        self,
        servers: list[BackendServer],
        client_ip: str | None = None,
    ) -> BackendServer | None:
        routable = [s for s in servers if s.is_routable]
        if not routable:
            return None

        with self._lock:
            # Initialize any new servers
            for s in routable:
                if s.server_id not in self._current_weights:
                    self._current_weights[s.server_id] = 0

            # Increment current weight by nominal weight
            for s in routable:
                self._current_weights[s.server_id] += s.weight

            # Pick server with highest current weight
            best_server = max(routable, key=lambda s: self._current_weights[s.server_id])
            total_weight = sum(s.weight for s in routable)

            # Decrement chosen server's current weight by total weight
            self._current_weights[best_server.server_id] -= total_weight
            return best_server


class LeastConnectionsStrategy:
    """Directs new requests to the routable server with fewest active connections."""

    def select(
        self,
        servers: list[BackendServer],
        client_ip: str | None = None,
    ) -> BackendServer | None:
        routable = [s for s in servers if s.is_routable]
        if not routable:
            return None
        # Sort primarily by active connections, secondarily by total requests served
        return min(routable, key=lambda s: (s.active_connections, s.total_requests_served))


class IPHashStrategy:
    """Deterministic client-IP affinity (session persistence without cookies)."""

    def select(
        self,
        servers: list[BackendServer],
        client_ip: str | None = None,
    ) -> BackendServer | None:
        routable = [s for s in servers if s.is_routable]
        if not routable:
            return None
        if not client_ip:
            # Fall back to first routable if no IP is provided
            return routable[0]

        ip_digest = int(hashlib.md5(client_ip.encode("utf-8")).hexdigest(), 16)
        return routable[ip_digest % len(routable)]


class HealthChecker(ABC):
    """Abstract health probe checker."""

    @abstractmethod
    def probe(self, server: BackendServer) -> bool:
        """Returns True if probe succeeds, False otherwise."""


class LoadBalancer:
    """Enterprise Layer 4/7 Load Balancer orchestrating pool, checks, and routing."""

    def __init__(
        self,
        strategy: LoadBalancingStrategy | None = None,
        unhealthy_threshold: int = 3,
        healthy_threshold: int = 2,
    ) -> None:
        self.strategy: LoadBalancingStrategy = strategy or RoundRobinStrategy()
        self.unhealthy_threshold = unhealthy_threshold
        self.healthy_threshold = healthy_threshold
        self._servers: list[BackendServer] = []
        self._lock = threading.RLock()

    def register_server(self, server: BackendServer) -> None:
        with self._lock:
            if not any(s.server_id == server.server_id for s in self._servers):
                self._servers.append(server)

    def remove_server(self, server_id: str) -> None:
        with self._lock:
            self._servers = [s for s in self._servers if s.server_id != server_id]

    def drain_server(self, server_id: str) -> bool:
        """Mark server as DRAINING: stops receiving new connections, finishes current."""
        with self._lock:
            for s in self._servers:
                if s.server_id == server_id:
                    s.status = HealthStatus.DRAINING
                    return True
            return False

    def route_request(self, client_ip: str | None = None) -> BackendServer:
        """Select a backend server and increment active connection counters."""
        with self._lock:
            server = self.strategy.select(self._servers, client_ip)
            if server is None:
                raise RuntimeError("503 Service Unavailable: No healthy backend servers in pool")
            server.active_connections += 1
            server.total_requests_served += 1
            return server

    def release_connection(self, server_id: str) -> None:
        """Decrements active connection counter when request completes."""
        with self._lock:
            for s in self._servers:
                if s.server_id == server_id:
                    s.active_connections = max(0, s.active_connections - 1)
                    break

    def record_health_result(self, server_id: str, is_healthy: bool) -> None:
        """Updates health states using hysteresis thresholds to prevent flap."""
        with self._lock:
            for s in self._servers:
                if s.server_id != server_id:
                    continue

                if is_healthy:
                    s.consecutive_successes += 1
                    s.consecutive_failures = 0
                    if (
                        s.status == HealthStatus.UNHEALTHY
                        and s.consecutive_successes >= self.healthy_threshold
                    ):
                        s.status = HealthStatus.HEALTHY
                else:
                    s.consecutive_failures += 1
                    s.consecutive_successes = 0
                    if (
                        s.status == HealthStatus.HEALTHY
                        and s.consecutive_failures >= self.unhealthy_threshold
                    ):
                        s.status = HealthStatus.UNHEALTHY
                break

    def get_server(self, server_id: str) -> BackendServer | None:
        with self._lock:
            return next((s for s in self._servers if s.server_id == server_id), None)

    def healthy_servers(self) -> list[BackendServer]:
        with self._lock:
            return [s for s in self._servers if s.is_routable]
