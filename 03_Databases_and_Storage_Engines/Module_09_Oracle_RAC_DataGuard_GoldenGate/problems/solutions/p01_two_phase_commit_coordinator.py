"""Reference Solution — Problem 01: Two Phase Commit Coordinator

Topic: 09 Oracle RAC DataGuard GoldenGate
"""

from __future__ import annotations


def two_phase_commit_coordinator(nodes: list[str], votes: dict[str, bool]) -> str:
    for node in nodes:
        if not votes.get(node, False):
            return 'ABORT'
    return 'COMMIT'
