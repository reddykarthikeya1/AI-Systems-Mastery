"""Reference Solution — Problem 01: Weighted Least Connections

Topic: 04 Load Balancing Algorithms Health Probes
"""

from __future__ import annotations


def weighted_least_connections(servers: list[dict]) -> str | None:
    healthy = [s for s in servers if s.get('is_healthy', False) and s.get('weight', 0) > 0]
    if not healthy:
        return None
    # Sort by ratio ascending, then id ascending
    healthy.sort(key=lambda s: (s['active_conns'] / s['weight'], s['id']))
    return healthy[0]['id']
