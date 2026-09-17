"""Problem 01 — Weighted Least Connections

Topic: 04 Load Balancing Algorithms Health Probes
Target: Production-grade implementation

Pick backend server with lowest active connection to weight ratio that passes health check.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def weighted_least_connections(servers: list[dict]) -> str | None:
    """Each server dict: {'id': str, 'weight': int, 'active_conns': int, 'is_healthy': bool}.
    Select healthy server minimizing (active_conns / weight).
    Ties broken by server id ascending.
    Return id, or None if no healthy servers.
    """
    raise NotImplementedError("Implement weighted_least_connections")
