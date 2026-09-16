"""Unit and integration test suite for Module 24: Raft Consensus & Vector Clocks."""

from raft_cluster_engine import (
    CausalityRelation,
    LogEntry,
    RaftCluster,
    RaftNode,
    RaftRole,
    RequestVoteArgs,
    VectorClock,
)


def test_vector_clock_causality() -> None:
    vc1 = VectorClock()
    vc2 = VectorClock()

    vc1.tick("A")
    msg = vc1.send_event("A")
    vc2.receive_event("B", msg)

    # vc1 happened before vc2
    assert VectorClock.compare(vc1, vc2) == CausalityRelation.HAPPENED_BEFORE
    assert VectorClock.compare(vc2, vc1) == CausalityRelation.HAPPENED_AFTER

    # Independent concurrent event on node C
    vc3 = VectorClock()
    vc3.tick("C")
    assert VectorClock.compare(vc1, vc3) == CausalityRelation.CONCURRENT


def test_raft_election_and_quorum() -> None:
    cluster = RaftCluster(["n1", "n2", "n3"])
    assert cluster.quorum_size == 2

    # n1 initiates election
    elected = cluster.run_election("n1")
    assert elected is True
    assert cluster.nodes["n1"].role == RaftRole.LEADER
    assert cluster.nodes["n1"].current_term == 1
    assert cluster.nodes["n2"].role == RaftRole.FOLLOWER
    assert cluster.nodes["n3"].role == RaftRole.FOLLOWER


def test_raft_log_replication_and_commit() -> None:
    cluster = RaftCluster(["n1", "n2", "n3"])
    cluster.run_election("n1")

    success, idx = cluster.client_write("n1", "SET key=val")
    assert success is True
    assert idx == 1

    # Check that all nodes have committed the log entry
    for nid in ["n1", "n2", "n3"]:
        node = cluster.nodes[nid]
        assert node.commit_index == 1
        assert len(node.log) == 1
        assert node.log[0].command == "SET key=val"


def test_raft_election_safety_log_up_to_date() -> None:
    # Voter has log up to index 2; Candidate only has log up to index 1 in the same term
    voter = RaftNode("voter", ["candidate"])
    voter.current_term = 1
    voter.log = [LogEntry(term=1, index=1, command="c1"), LogEntry(term=1, index=2, command="c2")]

    candidate_args = RequestVoteArgs(
        term=1,
        candidate_id="candidate",
        last_log_index=1,  # Outdated log
        last_log_term=1,
    )

    reply = voter.handle_request_vote(candidate_args)
    assert reply.vote_granted is False  # Reject outdated candidate


def test_non_leader_rejects_client_write() -> None:
    cluster = RaftCluster(["n1", "n2", "n3"])
    cluster.run_election("n1")

    # Attempt to issue write to follower n2
    success, idx = cluster.client_write("n2", "SET invalid=1")
    assert success is False
    assert idx == -1
