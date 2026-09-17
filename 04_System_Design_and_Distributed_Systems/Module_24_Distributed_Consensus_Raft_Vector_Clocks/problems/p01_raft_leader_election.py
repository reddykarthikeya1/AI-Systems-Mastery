"""Problem 01 — Raft Leader Election

Topic: 24 Distributed Consensus Raft Vector Clocks
Target: Production-grade implementation

Simulate Raft candidate election votes and step-down rules.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def raft_leader_election(cluster_size: int, candidate_term: int, votes_received: list[tuple[str, int, bool]]) -> tuple[str, int]:
    """votes_received: list of (peer_id, peer_term, vote_granted).
    If any peer has peer_term > candidate_term:
        candidate immediately steps down to FOLLOWER with updated term = peer_term.
        Returns ('FOLLOWER', peer_term).
    If total vote_granted count (including candidate's self vote of 1) > cluster_size // 2:
        Returns ('LEADER', candidate_term).
    Else:
        Returns ('CANDIDATE', candidate_term).
    """
    raise NotImplementedError("Implement raft_leader_election")
