"""Module 24: Distributed Consensus (Raft State Machine) & Vector Clocks.

Reference implementation of Raft consensus primitives (Leader Election, Quorum commits,
Log Replication safety) and Vector Clock causal event ordering.

This is an **in-process model**, not a deployed distributed system. It runs in a
single Python process with no network, no separate nodes, and no real
infrastructure. That is the correct way to teach this material: you cannot spin
up a CDN, a global load balancer or a five-node consensus cluster inside a
lesson, and building the mechanism by hand is what makes it visible.

What that means for you: every algorithm and state transition here is real and
worth studying. The *operational* behaviour - partial network partitions, clock
skew across machines, kernel-level backpressure - is simulated, and the module
README says which parts are which.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field

# ============================================================================
# 1. Vector Clock & Causal Consistency Engine
# ============================================================================

class CausalityRelation(enum.StrEnum):
    HAPPENED_BEFORE = "HAPPENED_BEFORE"  # A -> B
    HAPPENED_AFTER = "HAPPENED_AFTER"    # B -> A
    EQUAL = "EQUAL"                      # A == B
    CONCURRENT = "CONCURRENT"            # A || B (Conflict/Branch)


@dataclass
class VectorClock:
    """Logical vector clock tracking causality across distributed nodes."""
    clock: dict[str, int] = field(default_factory=dict)

    def tick(self, node_id: str) -> None:
        """Increments node's local logical clock on an internal event."""
        self.clock[node_id] = self.clock.get(node_id, 0) + 1

    def send_event(self, node_id: str) -> VectorClock:
        """Ticks node clock and returns a snapshot to attach to an outgoing message."""
        self.tick(node_id)
        return VectorClock(clock=dict(self.clock))

    def receive_event(self, node_id: str, incoming: VectorClock) -> None:
        """Merges incoming message clock and ticks node's local clock."""
        all_nodes = set(self.clock.keys()).union(set(incoming.clock.keys()))
        for n in all_nodes:
            self.clock[n] = max(self.clock.get(n, 0), incoming.clock.get(n, 0))
        self.tick(node_id)

    @staticmethod
    def compare(v1: VectorClock, v2: VectorClock) -> CausalityRelation:
        """Evaluates causal ordering between two vector clock states."""
        if v1.clock == v2.clock:
            return CausalityRelation.EQUAL

        all_nodes = set(v1.clock.keys()).union(set(v2.clock.keys()))
        v1_le_v2 = True
        v2_le_v1 = True

        for n in all_nodes:
            c1 = v1.clock.get(n, 0)
            c2 = v2.clock.get(n, 0)
            if c1 > c2:
                v1_le_v2 = False
            if c2 > c1:
                v2_le_v1 = False

        if v1_le_v2 and not v2_le_v1:
            return CausalityRelation.HAPPENED_BEFORE
        elif v2_le_v1 and not v1_le_v2:
            return CausalityRelation.HAPPENED_AFTER
        else:
            return CausalityRelation.CONCURRENT


# ============================================================================
# 2. Raft Consensus Node State Machine
# ============================================================================

class RaftRole(enum.StrEnum):
    FOLLOWER = "FOLLOWER"
    CANDIDATE = "CANDIDATE"
    LEADER = "LEADER"


@dataclass
class LogEntry:
    term: int
    index: int
    command: str


@dataclass
class RequestVoteArgs:
    term: int
    candidate_id: str
    last_log_index: int
    last_log_term: int


@dataclass
class RequestVoteReply:
    term: int
    vote_granted: bool


@dataclass
class AppendEntriesArgs:
    term: int
    leader_id: str
    prev_log_index: int
    prev_log_term: int
    entries: list[LogEntry]
    leader_commit: int


@dataclass
class AppendEntriesReply:
    term: int
    success: bool
    match_index: int


class RaftNode:
    """Individual participant node in a Raft consensus cluster."""

    def __init__(self, node_id: str, cluster_node_ids: list[str]) -> None:
        self.node_id = node_id
        self.cluster_nodes = [nid for nid in cluster_node_ids if nid != node_id]

        # Persistent state
        self.current_term: int = 0
        self.voted_for: str | None = None
        self.log: list[LogEntry] = []  # 0-indexed internally, 1-indexed in Raft protocol

        # Volatile state on all servers
        self.commit_index: int = 0
        self.last_applied: int = 0
        self.role: RaftRole = RaftRole.FOLLOWER

    @property
    def last_log_index(self) -> int:
        return len(self.log)

    @property
    def last_log_term(self) -> int:
        return self.log[-1].term if self.log else 0

    def start_election(self) -> RequestVoteArgs:
        """Transitions to CANDIDATE, increments term, and votes for self."""
        self.role = RaftRole.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id

        return RequestVoteArgs(
            term=self.current_term,
            candidate_id=self.node_id,
            last_log_index=self.last_log_index,
            last_log_term=self.last_log_term,
        )

    def handle_request_vote(self, args: RequestVoteArgs) -> RequestVoteReply:
        """Evaluates RequestVote RPC from a candidate."""
        # 1. Rule: If args.term > current_term, step down to FOLLOWER
        if args.term > self.current_term:
            self.current_term = args.term
            self.role = RaftRole.FOLLOWER
            self.voted_for = None

        # 2. Reject if candidate's term is older
        if args.term < self.current_term:
            return RequestVoteReply(term=self.current_term, vote_granted=False)

        # 3. Check if we already voted for someone else in this term
        can_vote = (self.voted_for is None or self.voted_for == args.candidate_id)

        # 4. Check Election Safety: Candidate's log must be at least as up-to-date as ours
        my_last_term = self.last_log_term
        my_last_index = self.last_log_index

        candidate_is_uptodate = False
        if args.last_log_term > my_last_term or (args.last_log_term == my_last_term and args.last_log_index >= my_last_index):
            candidate_is_uptodate = True

        if can_vote and candidate_is_uptodate:
            self.voted_for = args.candidate_id
            return RequestVoteReply(term=self.current_term, vote_granted=True)

        return RequestVoteReply(term=self.current_term, vote_granted=False)

    def handle_append_entries(self, args: AppendEntriesArgs) -> AppendEntriesReply:
        """Evaluates AppendEntries RPC (heartbeat or log replication)."""
        # 1. Reply false if term < current_term
        if args.term < self.current_term:
            return AppendEntriesReply(term=self.current_term, success=False, match_index=self.last_log_index)

        # If term > current_term, update term and convert to FOLLOWER
        if args.term > self.current_term:
            self.current_term = args.term
            self.voted_for = None

        self.role = RaftRole.FOLLOWER

        # 2. Reply false if log doesn't contain an entry at prev_log_index matching prev_log_term
        if args.prev_log_index > 0:
            if len(self.log) < args.prev_log_index:
                return AppendEntriesReply(term=self.current_term, success=False, match_index=len(self.log))
            if self.log[args.prev_log_index - 1].term != args.prev_log_term:
                # Log conflict: delete conflicting entries
                self.log = self.log[:args.prev_log_index - 1]
                return AppendEntriesReply(term=self.current_term, success=False, match_index=len(self.log))

        # 3. Append any new entries not already in the log
        for entry in args.entries:
            if entry.index <= len(self.log):
                self.log[entry.index - 1] = entry
            else:
                self.log.append(entry)

        # 4. If leader_commit > commit_index, set commit_index = min(leader_commit, last_log_index)
        if args.leader_commit > self.commit_index:
            self.commit_index = min(args.leader_commit, self.last_log_index)

        return AppendEntriesReply(term=self.current_term, success=True, match_index=self.last_log_index)


# ============================================================================
# 3. Raft Cluster Simulator
# ============================================================================

class RaftCluster:
    """Manages a cluster of simulated Raft nodes and coordinates quorums."""

    def __init__(self, node_ids: list[str]) -> None:
        self.nodes = {nid: RaftNode(nid, node_ids) for nid in node_ids}
        self.quorum_size = (len(node_ids) // 2) + 1

    def run_election(self, candidate_id: str) -> bool:
        """Executes an election round for the specified candidate."""
        candidate = self.nodes[candidate_id]
        args = candidate.start_election()
        votes_received = 1  # Candidate votes for self

        for peer_id, peer in self.nodes.items():
            if peer_id == candidate_id:
                continue
            reply = peer.handle_request_vote(args)
            if reply.vote_granted:
                votes_received += 1

        if votes_received >= self.quorum_size:
            candidate.role = RaftRole.LEADER
            return True
        return False

    def client_write(self, leader_id: str, command: str) -> tuple[bool, int]:
        """Leader appends entry, replicates to followers, and commits upon majority ACK."""
        leader = self.nodes[leader_id]
        if leader.role != RaftRole.LEADER:
            return False, -1

        new_index = leader.last_log_index + 1
        entry = LogEntry(term=leader.current_term, index=new_index, command=command)
        leader.log.append(entry)

        # Replicate to followers
        ack_count = 1  # Leader itself
        prev_idx = new_index - 1
        prev_term = leader.log[prev_idx - 1].term if prev_idx > 0 else 0

        for peer_id, peer in self.nodes.items():
            if peer_id == leader_id:
                continue
            args = AppendEntriesArgs(
                term=leader.current_term,
                leader_id=leader_id,
                prev_log_index=prev_idx,
                prev_log_term=prev_term,
                entries=[entry],
                leader_commit=leader.commit_index,
            )
            reply = peer.handle_append_entries(args)
            if reply.success:
                ack_count += 1

        # Check quorum commit
        if ack_count >= self.quorum_size:
            leader.commit_index = new_index
            # Send updated commit_index in heartbeats
            for peer_id, peer in self.nodes.items():
                if peer_id == leader_id:
                    continue
                args = AppendEntriesArgs(
                    term=leader.current_term,
                    leader_id=leader_id,
                    prev_log_index=new_index,
                    prev_log_term=entry.term,
                    entries=[],
                    leader_commit=leader.commit_index,
                )
                peer.handle_append_entries(args)
            return True, new_index

        return False, -1
