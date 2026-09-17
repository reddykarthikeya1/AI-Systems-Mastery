"""Reference Solution — Problem 01: Raft Leader Election

Topic: 24 Distributed Consensus Raft Vector Clocks
"""

from __future__ import annotations


def raft_leader_election(cluster_size: int, candidate_term: int, votes_received: list[tuple[str, int, bool]]) -> tuple[str, int]:
    votes = 1  # self vote
    for peer, term, granted in votes_received:
        if term > candidate_term:
            return ('FOLLOWER', term)
        if term == candidate_term and granted:
            votes += 1
    if votes > cluster_size // 2:
        return ('LEADER', candidate_term)
    return ('CANDIDATE', candidate_term)
