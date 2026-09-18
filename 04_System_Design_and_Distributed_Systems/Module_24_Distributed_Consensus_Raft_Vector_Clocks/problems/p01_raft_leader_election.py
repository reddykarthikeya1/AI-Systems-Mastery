"""Problem 01 — Raft Leader Election

Topic: 24 Distributed Consensus Raft Vector Clocks
Target: Production-grade implementation

Simulate Raft candidate election votes and step-down rules.

Example:
    >>> raft_leader_election(5, 3, [('node2', 3, True), ('node3', 3, True), ('node4', 3, False), ('node5', 3, False)])
    ('LEADER', 3)

Hints:
    Hint 1: A candidate wins by MAJORITY, not unanimity, and any peer
        reporting a newer term immediately overrides the whole election,
        even if that peer didn't vote yes.
    Hint 2: Start the vote tally at 1 (the self-vote), scan the peer
        responses once accumulating granted votes at the candidate's own
        term, but bail out the instant a peer's term exceeds
        `candidate_term`; compare the final tally against
        `cluster_size // 2`.
    Hint 3: A peer's vote only counts toward the tally if its `peer_term`
        EQUALS `candidate_term` (a grant at a different term doesn't
        count, and a higher term short-circuits straight to FOLLOWER
        before tallying continues); the majority check is strictly
        greater than `cluster_size // 2`, not `>=`, so an exact half is
        not enough to win.
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
