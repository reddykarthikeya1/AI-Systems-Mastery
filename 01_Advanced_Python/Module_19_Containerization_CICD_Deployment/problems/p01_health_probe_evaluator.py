"""Problem 01 — Readiness & Liveness Consensus

Target: Production-grade implementation

Example:
    >>> probes = [{'liveness': True, 'readiness': True}, {'liveness': True, 'readiness': False}]
    >>> evaluate_cluster_health(probes, 0.5)
    True
    >>> evaluate_cluster_health(probes, 0.6)
    False

Hints:
    Hint 1: A single probe only counts as "healthy" when both of its signals
        agree — being alive but not ready (or vice versa) doesn't count.
    Hint 2: Count how many dicts in `probes` have both `'liveness'` and
        `'readiness'` truthy, then compare that count as a fraction of
        `len(probes)` against `min_healthy_pct`.
    Hint 3: An empty `probes` list must return `False` (there's no cluster to
        call healthy, and it also avoids a zero-division), and the comparison
        against `min_healthy_pct` is inclusive (`>=`), so a probe list that
        hits the threshold exactly still counts as healthy.
"""

from __future__ import annotations


def evaluate_cluster_health(probes: list[dict[str, bool]], min_healthy_pct: float) -> bool:
    raise NotImplementedError('Implement evaluate_cluster_health')
