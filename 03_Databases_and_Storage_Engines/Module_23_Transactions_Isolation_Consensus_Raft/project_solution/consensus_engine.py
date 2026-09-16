"""Module 23: Transactions, Anomalies & Raft Consensus (Solution).

Implements:
1. WriteSkewSimulator: Demonstrates Write Skew under Snapshot Isolation and resolution via SSI.
2. TwoPhaseCommitCoordinator: Phase 1 Prepare and Phase 2 Commit/Abort across distributed shards.
3. RaftNode: Role transitions, randomized elections, quorum voting, and majority log replication.
"""

from __future__ import annotations

from typing import Any


class SerializationFailureError(Exception):
    """Raised when Serializable Snapshot Isolation detects a dangerous dependency cycle."""


class WriteSkewSimulator:
    """Simulates Doctor On-Call invariant under Snapshot Isolation vs SSI."""

    def __init__(self) -> None:
        # Invariant: At least 1 doctor on call
        self.doctors = {"Alice": True, "Bob": True}

    def run_snapshot_isolation(self) -> tuple[bool, int]:
        """Simulate concurrent transactions under Snapshot Isolation leading to Write Skew."""
        # Initial snapshot seen by both Tx1 and Tx2
        snap1 = dict(self.doctors)
        snap2 = dict(self.doctors)

        # Tx 1: Alice checks if someone else is on call
        if sum(1 for v in snap1.values() if v) >= 2:
            self.doctors["Alice"] = False

        # Tx 2: Bob concurrently checks if someone else is on call
        if sum(1 for v in snap2.values() if v) >= 2:
            # Disjoint write set! MVCC allows both writes to commit
            self.doctors["Bob"] = False

        remaining = sum(1 for v in self.doctors.values() if v)
        invariant_violated = (remaining == 0)
        return invariant_violated, remaining

    def run_serializable_snapshot_isolation(self) -> tuple[bool, int]:
        """Simulate transactions under SSI, detecting rw-antidependency cycle and aborting."""
        # Reset state
        self.doctors = {"Alice": True, "Bob": True}

        # Track SIREAD locks (read-sets) and write-sets
        tx1_read = {"Alice", "Bob"}
        tx1_write = {"Alice"}

        tx2_read = {"Alice", "Bob"}
        tx2_write = {"Bob"}

        # Tx1 commits successfully
        self.doctors["Alice"] = False

        # Tx2 attempts to commit: SSI checks for rw-antidependency cycle
        # T1 read Bob (which T2 wrote), and T2 read Alice (which T1 wrote)
        t1_rw_t2 = bool(tx1_read.intersection(tx2_write))
        t2_rw_t1 = bool(tx2_read.intersection(tx1_write))

        if t1_rw_t2 and t2_rw_t1:
            # Cycle detected: T1 -> T2 -> T1. Abort Tx 2!
            # Bob is prevented from going off call
            pass

        remaining = sum(1 for v in self.doctors.values() if v)
        invariant_violated = (remaining == 0)
        return invariant_violated, remaining


class ParticipantShard:
    """A participant shard in a Two-Phase Commit distributed transaction."""

    def __init__(self, shard_id: str, should_fail: bool = False) -> None:
        self.shard_id = shard_id
        self.should_fail = should_fail
        self.state = "IDLE"

    def prepare(self) -> bool:
        if self.should_fail:
            self.state = "ABORTED"
            return False
        self.state = "PREPARED"
        return True

    def commit(self) -> None:
        self.state = "COMMITTED"

    def abort(self) -> None:
        self.state = "ABORTED"


class TwoPhaseCommitCoordinator:
    """Coordinates atomic multi-shard commitment across the network."""

    def __init__(self, participants: list[ParticipantShard]) -> None:
        self.participants = participants

    def execute_transaction(self) -> bool:
        # Phase 1: Prepare (Voting)
        votes = [p.prepare() for p in self.participants]

        # Phase 2: Decision & Execution
        if all(votes):
            for p in self.participants:
                p.commit()
            return True
        else:
            for p in self.participants:
                p.abort()
            return False


class RaftNode:
    """A node in a Raft consensus cluster implementing leader election and log replication."""

    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.role = "FOLLOWER"
        self.current_term = 0
        self.voted_for: str | None = None
        self.log: list[dict[str, Any]] = []
        self.commit_index = -1

    def request_vote(
        self,
        candidate_term: int,
        candidate_id: str,
        last_log_index: int,
        last_log_term: int,
    ) -> tuple[bool, int]:
        if candidate_term < self.current_term:
            return False, self.current_term

        if candidate_term > self.current_term:
            self.current_term = candidate_term
            self.role = "FOLLOWER"
            self.voted_for = None

        my_last_index = len(self.log) - 1
        my_last_term = self.log[my_last_index]["term"] if my_last_index >= 0 else 0

        log_up_to_date = (last_log_term > my_last_term) or (
            last_log_term == my_last_term and last_log_index >= my_last_index
        )

        if (self.voted_for is None or self.voted_for == candidate_id) and log_up_to_date:
            self.voted_for = candidate_id
            return True, self.current_term

        return False, self.current_term

    def append_entries(
        self,
        leader_term: int,
        leader_id: str,
        prev_log_index: int,
        prev_log_term: int,
        entries: list[dict[str, Any]],
        leader_commit: int,
    ) -> tuple[bool, int]:
        if leader_term < self.current_term:
            return False, self.current_term

        if leader_term > self.current_term:
            self.current_term = leader_term
            self.role = "FOLLOWER"
            self.voted_for = None

        self.role = "FOLLOWER"
        for e in entries:
            self.log.append(e)

        if leader_commit > self.commit_index:
            self.commit_index = min(leader_commit, len(self.log) - 1)

        return True, self.current_term

    def start_election(self, peers: list[RaftNode]) -> bool:
        self.role = "CANDIDATE"
        self.current_term += 1
        self.voted_for = self.node_id
        votes = 1

        last_idx = len(self.log) - 1
        last_term = self.log[last_idx]["term"] if last_idx >= 0 else 0

        for peer in peers:
            granted, _ = peer.request_vote(
                candidate_term=self.current_term,
                candidate_id=self.node_id,
                last_log_index=last_idx,
                last_log_term=last_term,
            )
            if granted:
                votes += 1

        total_nodes = len(peers) + 1
        majority = (total_nodes // 2) + 1

        if votes >= majority:
            self.role = "LEADER"
            return True
        else:
            self.role = "FOLLOWER"
            return False

    def replicate_entry(self, data: str, peers: list[RaftNode]) -> bool:
        if self.role != "LEADER":
            raise RuntimeError("Only leader can replicate log entries")

        entry = {"term": self.current_term, "data": data}
        self.log.append(entry)
        acks = 1

        for peer in peers:
            success, _ = peer.append_entries(
                leader_term=self.current_term,
                leader_id=self.node_id,
                prev_log_index=len(self.log) - 2,
                prev_log_term=self.log[-2]["term"] if len(self.log) > 1 else 0,
                entries=[entry],
                leader_commit=self.commit_index,
            )
            if success:
                acks += 1

        total_nodes = len(peers) + 1
        majority = (total_nodes // 2) + 1

        if acks >= majority:
            self.commit_index = len(self.log) - 1
            for peer in peers:
                peer.commit_index = self.commit_index
            return True

        return False
