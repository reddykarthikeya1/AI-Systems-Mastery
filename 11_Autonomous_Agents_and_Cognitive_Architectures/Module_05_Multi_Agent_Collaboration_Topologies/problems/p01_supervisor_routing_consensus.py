"""Problem 01 — Supervisor Routing Consensus

Topic: 05 Multi Agent Collaboration Topologies
Target: Production-grade implementation

Supervisor routes query to specialized agent based on task keywords.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def supervisor_routing_consensus(query: str) -> str:
    """Classify query:
    - If 'sql' or 'database' in query.lower(): return 'DatabaseAgent'
    - If 'code' or 'python' in query.lower(): return 'CoderAgent'
    - If 'test' or 'eval' in query.lower(): return 'TesterAgent'
    - Otherwise: return 'GeneralAgent'
    """
    raise NotImplementedError("Implement supervisor_routing_consensus")
