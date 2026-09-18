"""Problem 01 — Weighted Least Connections

Topic: 04 Load Balancing Algorithms Health Probes
Target: Production-grade implementation

Pick backend server with lowest active connection to weight ratio that passes health check.

Example:
    >>> weighted_least_connections([{'id': 'srv1', 'weight': 2, 'active_conns': 10, 'is_healthy': True}, {'id': 'srv2', 'weight': 1, 'active_conns': 4, 'is_healthy': True}])
    'srv2'

Hints:
    Hint 1: Raw "least connections" alone unfairly favors low-capacity
        servers -- you need connections normalized by capacity (weight)
        to compare servers on equal footing.
    Hint 2: Filter down to healthy servers with positive weight first,
        then pick the minimum by the ratio `active_conns / weight`, using
        server id ascending as the tiebreaker.
    Hint 3: Unhealthy servers must be excluded entirely before ranking,
        not merely deprioritized (srv2's ratio 4.0 beats srv1's 5.0 only
        once srv3 is dropped for being unhealthy); with no healthy
        servers left, return None instead of raising.
"""

from __future__ import annotations


def weighted_least_connections(servers: list[dict]) -> str | None:
    """Each server dict: {'id': str, 'weight': int, 'active_conns': int, 'is_healthy': bool}.
    Select healthy server minimizing (active_conns / weight).
    Ties broken by server id ascending.
    Return id, or None if no healthy servers.
    """
    raise NotImplementedError("Implement weighted_least_connections")
