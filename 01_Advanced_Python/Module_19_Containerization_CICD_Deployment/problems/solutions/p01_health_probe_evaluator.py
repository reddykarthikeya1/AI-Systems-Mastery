"""Problem 01 — Readiness & Liveness Consensus

Target: Production-grade implementation
"""

from __future__ import annotations


def evaluate_cluster_health(probes: list[dict[str, bool]], min_healthy_pct: float) -> bool:
    if not probes: return False
    healthy = sum(1 for p in probes if p.get('liveness') and p.get('readiness'))
    return (healthy / len(probes)) >= min_healthy_pct
