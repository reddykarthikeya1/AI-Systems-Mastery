"""Reference Solution — Problem 01: Supervisor Routing Consensus

Topic: 05 Multi Agent Collaboration Topologies
"""

from __future__ import annotations


def supervisor_routing_consensus(query: str) -> str:
    q = query.lower()
    if 'sql' in q or 'database' in q:
        return 'DatabaseAgent'
    if 'code' in q or 'python' in q:
        return 'CoderAgent'
    if 'test' in q or 'eval' in q:
        return 'TesterAgent'
    return 'GeneralAgent'
