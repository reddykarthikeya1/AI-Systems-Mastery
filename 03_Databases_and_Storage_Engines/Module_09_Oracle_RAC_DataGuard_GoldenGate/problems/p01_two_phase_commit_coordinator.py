"""Problem 01 — Two Phase Commit Coordinator

Topic: 09 Oracle RAC DataGuard GoldenGate
Target: Production-grade implementation

Simulate 2PC protocol across distributed database nodes.

Example:
    >>> nodes = ['nodeA', 'nodeB', 'nodeC']
    >>> two_phase_commit_coordinator(nodes, {'nodeA': True, 'nodeB': False, 'nodeC': True})
    'ABORT'

Hints:
    Hint 1: The coordinator's decision is a single AND across every node in
        the cluster — one unprepared node is enough to sink the whole
        transaction, no matter how many others said yes.
    Hint 2: Walk the required `nodes` list (not just the votes dict) and
        look up each node's vote with dict.get, defaulting to False.
    Hint 3: A node that never voted at all (absent from `votes`) must count
        the same as an explicit False vote and force ABORT — don't iterate
        only over votes.items(), since that silently ignores nodes that
        never checked in.
"""

from __future__ import annotations


def two_phase_commit_coordinator(nodes: list[str], votes: dict[str, bool]) -> str:
    """Return 'COMMIT' if all nodes voted True (PREPARED).
    Return 'ABORT' if any node voted False or is missing.
    """
    raise NotImplementedError("Implement two_phase_commit_coordinator")
