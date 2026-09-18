"""Problem 01 — Supervisor Routing Consensus

Topic: 05 Multi Agent Collaboration Topologies
Target: Production-grade implementation

Supervisor routes query to specialized agent based on task keywords.

Example:
    >>> supervisor_routing_consensus('Optimize SQL query')
    'DatabaseAgent'

Hints:
    Hint 1: This is a rule-based classifier — each query maps to exactly
        one of four buckets, decided by which keyword family shows up,
        checked in a fixed priority order.
    Hint 2: Lowercase the query once, then test keyword membership with
        'in' against each category's keyword set in order (database
        keywords, then coder keywords, then tester keywords), falling
        through to a general-purpose default.
    Hint 3: Check order matters when a query could match more than one
        family — return the first matching category in the given priority
        (database, then coder, then tester) rather than the "best" match,
        and treat 'sql'/'database'/etc. as substrings, not whole-word-only
        matches.
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
