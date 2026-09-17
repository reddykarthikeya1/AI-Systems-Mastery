"""Tests for Raft Leader Election."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_raft_leader_election import raft_leader_election
except ImportError:
    from p01_raft_leader_election import raft_leader_election


def test_raft_leader_election():
    votes_quorum = [('node2', 3, True), ('node3', 3, True), ('node4', 3, False), ('node5', 3, False)]
    role, term = raft_leader_election(5, 3, votes_quorum)
    assert role == 'LEADER' and term == 3
    
    votes_higher = [('node2', 4, False)]
    role2, term2 = raft_leader_election(5, 3, votes_higher)
    assert role2 == 'FOLLOWER' and term2 == 4
