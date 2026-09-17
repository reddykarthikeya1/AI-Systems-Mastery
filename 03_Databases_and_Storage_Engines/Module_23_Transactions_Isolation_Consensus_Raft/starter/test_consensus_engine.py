"""Module 23 Test Suite: Transactions, Write Skew & Raft Distributed Consensus."""

from __future__ import annotations

from consensus_engine import (
    ParticipantShard,
    RaftNode,
    TwoPhaseCommitCoordinator,
    WriteSkewSimulator,
)


def test_write_skew_under_snapshot_isolation() -> None:
    simulator = WriteSkewSimulator()
    violated, remaining = simulator.run_snapshot_isolation()

    # Under Snapshot Isolation, disjoint write sets cause both to commit,
    # leaving 0 doctors on call (breaking business invariant!)
    assert violated is True
    assert remaining == 0


def test_serializable_snapshot_isolation_prevents_write_skew() -> None:
    simulator = WriteSkewSimulator()
    violated, remaining = simulator.run_serializable_snapshot_isolation()

    # Under SSI, rw-antidependency cycle is detected, aborting the second mutation
    assert violated is False
    assert remaining == 1


def test_two_phase_commit_all_commit() -> None:
    s1 = ParticipantShard("shard_us_east")
    s2 = ParticipantShard("shard_eu_central")
    s3 = ParticipantShard("shard_ap_tokyo")

    coordinator = TwoPhaseCommitCoordinator([s1, s2, s3])
    committed = coordinator.execute_transaction()

    assert committed is True
    assert s1.state == "COMMITTED"
    assert s2.state == "COMMITTED"
    assert s3.state == "COMMITTED"


def test_two_phase_commit_abort_on_single_failure() -> None:
    s1 = ParticipantShard("shard_us_east", should_fail=False)
    s2 = ParticipantShard("shard_eu_central", should_fail=True)  # Disk full / Lock timeout
    s3 = ParticipantShard("shard_ap_tokyo", should_fail=False)

    coordinator = TwoPhaseCommitCoordinator([s1, s2, s3])
    committed = coordinator.execute_transaction()

    # Single negative vote forces GLOBAL ABORT across all participants
    assert committed is False
    assert s1.state == "ABORTED"
    assert s2.state == "ABORTED"
    assert s3.state == "ABORTED"


def test_raft_leader_election_majority() -> None:
    nodes = [RaftNode(f"node_{i}") for i in range(5)]
    candidate = nodes[0]
    peers = nodes[1:]

    # Candidate initiates election
    won = candidate.start_election(peers)

    assert won is True
    assert candidate.role == "LEADER"
    assert candidate.current_term == 1

    # Peers transitioned to followers of term 1
    for p in peers:
        assert p.role == "FOLLOWER"
        assert p.current_term == 1


def test_raft_log_replication_and_commit_index() -> None:
    nodes = [RaftNode(f"node_{i}") for i in range(3)]
    leader = nodes[0]
    peers = nodes[1:]

    leader.start_election(peers)
    assert leader.role == "LEADER"

    # Leader replicates a client write
    replicated = leader.replicate_entry("SET account:101 500", peers)
    assert replicated is True

    # Quorum reached -> Commit index incremented to 0 on leader and peers
    assert leader.commit_index == 0
    for p in peers:
        assert p.commit_index == 0
        assert len(p.log) == 1
        assert p.log[0]["data"] == "SET account:101 500"
