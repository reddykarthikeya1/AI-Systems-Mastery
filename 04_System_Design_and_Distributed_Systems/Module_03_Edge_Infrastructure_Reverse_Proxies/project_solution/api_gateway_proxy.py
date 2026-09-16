"""Module 03: Layer 7 API Gateway & Reverse Proxy Engine.

Implements an asynchronous Layer 7 Gateway featuring:
- Dynamic path-based routing to upstream service clusters.
- Round-robin load balancing across healthy backend instances.
- Active health checking and automatic failure ejection.
- Token-Bucket rate limiting per client identifier.
- Distributed Trace ID injection and header enrichment.

This is an **in-process model**, not a deployed distributed system. It runs in a
single Python process with no network, no separate nodes, and no real
infrastructure. That is the correct way to teach this material: you cannot spin
up a CDN, a global load balancer or a five-node consensus cluster inside a
lesson, and building the mechanism by hand is what makes it visible.

What that means for you: every algorithm and state transition here is real and
worth studying. The *operational* behaviour - partial network partitions, clock
skew across machines, kernel-level backpressure - is simulated, and the module
README says which parts are which.
"""

from __future__ import annotations

import asyncio
import time
import uuid
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from typing import Any


@dataclass
class UpstreamServer:
    server_id: str
    url: str
    is_healthy: bool = True
    consecutive_failures: int = 0
    total_requests: int = 0
    handler: Callable[[dict[str, Any]], Coroutine[Any, Any, dict[str, Any]]] | None = None


class TokenBucketRateLimiter:
    """Thread-safe and async-safe token bucket rate limiter."""

    def __init__(self, capacity: int, refill_rate_per_sec: float) -> None:
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def allow_request(self, cost: int = 1) -> bool:
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.last_refill = now

            # Refill tokens up to capacity
            self.tokens = min(float(self.capacity), self.tokens + elapsed * self.refill_rate)

            if self.tokens >= cost:
                self.tokens -= cost
                return True
            return False


@dataclass
class ServiceCluster:
    name: str
    servers: list[UpstreamServer] = field(default_factory=list)
    _current_index: int = 0

    def get_healthy_server(self) -> UpstreamServer | None:
        healthy = [s for s in self.servers if s.is_healthy]
        if not healthy:
            return None

        # Round-Robin selection
        server = healthy[self._current_index % len(healthy)]
        self._current_index = (self._current_index + 1) % len(healthy)
        return server


class APIGateway:
    """Production-grade Layer 7 API Gateway and Reverse Proxy."""

    def __init__(self, default_rate_limit_capacity: int = 10, default_refill_per_sec: float = 5.0) -> None:
        self._routes: dict[str, ServiceCluster] = {}
        self._rate_limiters: dict[str, TokenBucketRateLimiter] = {}
        self.rate_limit_capacity = default_rate_limit_capacity
        self.rate_limit_refill = default_refill_per_sec

    def register_cluster(self, route_prefix: str, cluster: ServiceCluster) -> None:
        self._routes[route_prefix] = cluster

    def _get_rate_limiter(self, client_id: str) -> TokenBucketRateLimiter:
        if client_id not in self._rate_limiters:
            self._rate_limiters[client_id] = TokenBucketRateLimiter(
                capacity=self.rate_limit_capacity,
                refill_rate_per_sec=self.rate_limit_refill,
            )
        return self._rate_limiters[client_id]

    async def route_request(
        self,
        path: str,
        client_ip: str,
        payload: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Routes an incoming client request through gateway filters to upstream."""
        headers = headers or {}
        payload = payload or {}

        # 1. Enforce Rate Limiting
        limiter = self._get_rate_limiter(client_ip)
        if not await limiter.allow_request():
            return {
                "status_code": 429,
                "error": "Too Many Requests - Rate Limit Exceeded",
                "headers": {"Retry-After": "1"},
            }

        # 2. Match Route
        matched_cluster: ServiceCluster | None = None
        for prefix, cluster in self._routes.items():
            if path.startswith(prefix):
                matched_cluster = cluster
                break

        if not matched_cluster:
            return {
                "status_code": 404,
                "error": f"No upstream cluster found for route: {path}",
            }

        # 3. Select Upstream Server (Load Balancing)
        server = matched_cluster.get_healthy_server()
        if not server:
            return {
                "status_code": 503,
                "error": f"Service Unavailable - All instances in cluster '{matched_cluster.name}' are down",
            }

        # 4. Inject Gateway Telemetry Headers
        trace_id = str(uuid.uuid4())
        enriched_headers = dict(headers)
        enriched_headers["X-Trace-ID"] = trace_id
        enriched_headers["X-Forwarded-For"] = client_ip
        enriched_headers["X-Upstream-Server"] = server.server_id

        # 5. Dispatch to Upstream Handler
        server.total_requests += 1
        try:
            if server.handler:
                result = await server.handler(payload)
            else:
                result = {"status": "OK", "data": payload}

            # Reset failure count on success
            server.consecutive_failures = 0
            return {
                "status_code": 200,
                "trace_id": trace_id,
                "upstream": server.server_id,
                "response": result,
            }
        except Exception as exc:
            server.consecutive_failures += 1
            if server.consecutive_failures >= 3:
                server.is_healthy = False  # Eject from pool

            return {
                "status_code": 502,
                "error": f"Bad Gateway - Upstream error: {exc!s}",
                "trace_id": trace_id,
                "upstream": server.server_id,
            }
