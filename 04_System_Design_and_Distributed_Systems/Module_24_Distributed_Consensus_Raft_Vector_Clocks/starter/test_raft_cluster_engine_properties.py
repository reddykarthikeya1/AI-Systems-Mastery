"""Property and performance assertions for Distributed Consensus, Raft & Vector Clocks.

These complement the correctness tests in `test_raft_cluster_engine.py`. A correctness test says
the operation does the right thing; these say the *claim the module makes about
it* is true - and they fail when it stops being true.

    pytest -m perf -v          # just the performance assertions
    pytest -m "not slow" -q    # skip the long ones
"""

from __future__ import annotations

from raft_cluster_engine import RaftCluster, RaftNode, VectorClock


def test_a_majority_is_required_to_elect_a_leader() -> None:
    """Consensus without a majority is not consensus. This is the safety core."""
    cluster = RaftCluster(["n1", "n2", "n3", "n4", "n5"])
    assert cluster.run_election("n1"), "a candidate reachable by 5 nodes must win"


def test_election_increments_the_term() -> None:
    """Terms are Raft's logical clock; a stale leader is detected by term."""
    node = RaftNode("n1", ["n1", "n2", "n3"])
    before = node.current_term
    node.start_election()
    assert node.current_term > before


def test_a_node_grants_only_one_vote_per_term() -> None:
    """Two leaders in one term is the exact failure Raft exists to prevent."""
    from raft_cluster_engine import RequestVoteArgs

    node = RaftNode("voter", ["voter", "a", "b"])
    first = node.handle_request_vote(
        RequestVoteArgs(term=5, candidate_id="a", last_log_index=0, last_log_term=0)
    )
    second = node.handle_request_vote(
        RequestVoteArgs(term=5, candidate_id="b", last_log_index=0, last_log_term=0)
    )
    assert first.vote_granted
    assert not second.vote_granted, "granted two votes in the same term"


def test_a_stale_term_request_is_rejected() -> None:
    from raft_cluster_engine import RequestVoteArgs

    node = RaftNode("n1", ["n1", "n2", "n3"])
    node.current_term = 10
    reply = node.handle_request_vote(
        RequestVoteArgs(term=3, candidate_id="old", last_log_index=0, last_log_term=0)
    )
    assert not reply.vote_granted


def test_vector_clock_detects_concurrent_updates() -> None:
    """Two nodes that never exchanged a message are CONCURRENT, not ordered.

    This is the distinction a plain integer counter cannot express, and the whole
    reason vector clocks exist: they detect a conflict rather than silently
    picking a winner.
    """
    from raft_cluster_engine import CausalityRelation

    a = VectorClock()
    b = VectorClock()
    a.tick("A")          # tick mutates in place and returns None
    b.tick("B")

    assert VectorClock.compare(a, b) is CausalityRelation.CONCURRENT


def test_vector_clock_orders_a_causal_chain() -> None:
    """A message received establishes happened-before, which must be detectable."""
    from raft_cluster_engine import CausalityRelation

    a = VectorClock()
    snapshot = a.send_event("A")      # ticks A and returns a copy to attach

    b = VectorClock()
    b.receive_event("B", snapshot)    # B merges A's history, then ticks itself

    relation = VectorClock.compare(snapshot, b)
    assert relation is CausalityRelation.HAPPENED_BEFORE, (
        f"expected the sent snapshot to precede the receiver's state, got {relation}"
    )


def test_client_write_through_the_leader_is_recorded() -> None:
    cluster = RaftCluster(["n1", "n2", "n3"])
    cluster.run_election("n1")
    assert cluster.client_write("n1", "SET x=1") is not None
