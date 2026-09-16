"""Chaos harness: partition the cluster, drop the packets, and see what breaks.

This is an **in-process model**. There is no network here - `ChaosNetwork` is a
predicate that decides whether one simulated node may hear another, and latency
is an accounting number rather than a delay anyone waits for. Nothing sleeps.

That is the point rather than a limitation. A real five-node cluster with a real
network partition is a day's work to set up and impossible to reproduce; this
runs in milliseconds and is deterministic given a seed, so a test can assert
that split brain did not happen rather than hoping nobody noticed.

Why this exists
---------------
`raft_cluster_engine.py` shows that Raft *works*. It cannot show the thing Raft
is actually for, because with a perfect network every consensus algorithm looks
correct - including wrong ones. The interesting question is what happens when:

- the cluster splits into two groups that cannot hear each other,
- a third of the messages are silently dropped,
- a leader is isolated but does not know it yet,
- the partition heals and two histories have to be reconciled.

The three faults modelled here are the three that matter:

| Fault | What it models | What it should NOT break |
| :--- | :--- | :--- |
| Partition | a switch or a rack losing its uplink | safety - at most one leader commits |
| Message loss | congestion, a full queue, a GC pause | safety; liveness recovers on retry |
| Asymmetric reachability | a one-way firewall rule | safety, even though A hears B and B does not hear A |

The guarantee being tested is **safety, not liveness**. Raft is allowed to stop
making progress during a partition; it is never allowed to commit two different
values at the same index. A harness that only measured "did it keep working"
would be testing the wrong property.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from raft_cluster_engine import (
    AppendEntriesArgs,
    LogEntry,
    RaftNode,
    RaftRole,
)


@dataclass
class DeliveryStats:
    delivered: int = 0
    dropped_by_partition: int = 0
    dropped_by_loss: int = 0
    total_latency_ms: float = 0.0

    @property
    def attempted(self) -> int:
        return self.delivered + self.dropped_by_partition + self.dropped_by_loss

    @property
    def delivery_rate(self) -> float:
        return self.delivered / self.attempted if self.attempted else 1.0


class ChaosNetwork:
    """Decides whether one node may hear another, and records what happened.

    Deterministic given a seed: the same seed replays the same faults, which is
    what makes a failing test reproducible rather than a story about a flake.
    """

    def __init__(self, node_ids: list[str], seed: int = 0) -> None:
        self.node_ids = list(node_ids)
        self.random = random.Random(seed)
        self.partitions: list[set[str]] | None = None
        self.loss_rate = 0.0
        self.latency_ms = 0.0
        self.jitter_ms = 0.0
        self.one_way_blocks: set[tuple[str, str]] = set()
        self.stats = DeliveryStats()

    # -- fault injection ----------------------------------------------------

    def partition(self, *groups: list[str]) -> None:
        """Split the cluster into isolated factions.

        `network.partition(["n1", "n2", "n3"], ["n4", "n5"])` puts three nodes
        on one side of the break and two on the other. Nodes in different
        groups cannot exchange anything at all.
        """
        named = {node for group in groups for node in group}
        missing = set(self.node_ids) - named
        if missing:
            raise ValueError(f"partition does not account for {sorted(missing)}")
        duplicated = len(named) != sum(len(g) for g in groups)
        if duplicated:
            raise ValueError("a node cannot be in two partitions at once")
        self.partitions = [set(group) for group in groups]

    def heal(self) -> None:
        """Restore full connectivity. Faults stay recorded in `stats`."""
        self.partitions = None
        self.one_way_blocks.clear()

    def block_one_way(self, sender: str, receiver: str) -> None:
        """`sender` can no longer reach `receiver`, but the reverse still works.

        This is the fault people forget. A firewall rule or a half-open
        connection produces it, and it breaks any failure detector that assumes
        "I can see you" implies "you can see me".
        """
        self.one_way_blocks.add((sender, receiver))

    def set_loss(self, rate: float) -> None:
        if not 0.0 <= rate <= 1.0:
            raise ValueError("loss rate must be between 0 and 1")
        self.loss_rate = rate

    def set_latency(self, base_ms: float, jitter_ms: float = 0.0) -> None:
        """Record a per-message cost. Nothing sleeps - this is bookkeeping, so
        a test can assert on the latency budget without taking that long."""
        self.latency_ms = base_ms
        self.jitter_ms = jitter_ms

    # -- delivery -----------------------------------------------------------

    def same_side(self, a: str, b: str) -> bool:
        if self.partitions is None:
            return True
        return any(a in group and b in group for group in self.partitions)

    def deliver(self, sender: str, receiver: str) -> bool:
        """True if a message from `sender` reaches `receiver` this attempt."""
        if not self.same_side(sender, receiver) or (sender, receiver) in self.one_way_blocks:
            self.stats.dropped_by_partition += 1
            return False
        if self.loss_rate and self.random.random() < self.loss_rate:
            self.stats.dropped_by_loss += 1
            return False
        self.stats.delivered += 1
        self.stats.total_latency_ms += self.latency_ms + (
            self.random.uniform(0, self.jitter_ms) if self.jitter_ms else 0.0)
        return True


@dataclass
class ChaosCluster:
    """A Raft cluster whose every RPC goes through a `ChaosNetwork`.

    Same node implementation as `RaftCluster`; the only difference is that a
    peer which cannot be reached simply does not reply, exactly as it would not
    on a real network. A node never learns "the message was dropped" - it
    learns nothing, which is the whole difficulty of distributed systems.
    """

    node_ids: list[str]
    seed: int = 0
    nodes: dict[str, RaftNode] = field(init=False)
    network: ChaosNetwork = field(init=False)

    def __post_init__(self) -> None:
        self.nodes = {nid: RaftNode(nid, self.node_ids) for nid in self.node_ids}
        self.network = ChaosNetwork(self.node_ids, seed=self.seed)

    @property
    def quorum_size(self) -> int:
        return len(self.node_ids) // 2 + 1

    def reachable_from(self, node_id: str) -> list[str]:
        return [peer for peer in self.node_ids
                if peer != node_id and self.network.same_side(node_id, peer)]

    # -- elections ----------------------------------------------------------

    def run_election(self, candidate_id: str) -> bool:
        """One election round. Returns True only on a real majority.

        A candidate that cannot reach a majority stays a candidate. It does not
        become a leader "locally" - that would be the split-brain bug this
        harness exists to rule out.
        """
        candidate = self.nodes[candidate_id]
        args = candidate.start_election()
        votes = 1                                    # its own

        for peer_id in self.node_ids:
            if peer_id == candidate_id:
                continue
            if not self.network.deliver(candidate_id, peer_id):
                continue                             # request lost
            reply = self.nodes[peer_id].handle_request_vote(args)
            if not self.network.deliver(peer_id, candidate_id):
                continue                             # reply lost; vote is cast
            if reply.vote_granted:                   # but the candidate never hears it
                votes += 1

        if votes >= self.quorum_size:
            candidate.role = RaftRole.LEADER
            return True
        return False

    def elect_with_retries(self, candidate_id: str, attempts: int = 20) -> bool:
        """Retry an election until it succeeds or the attempts run out.

        Real Raft does this with randomised election timeouts. Under message
        loss a single round often fails; the point is that it recovers, which
        is liveness, and that it never elects two leaders, which is safety.
        """
        # `any` short-circuits, so this stops at the first successful round -
        # it does not run all `attempts` elections.
        return any(self.run_election(candidate_id) for _ in range(attempts))

    def leaders(self) -> list[str]:
        return [nid for nid, node in self.nodes.items() if node.role == RaftRole.LEADER]

    # -- replication --------------------------------------------------------

    def client_write(self, leader_id: str, command: str) -> tuple[bool, int]:
        """Append and replicate. Commits only on a majority of ACKs actually heard.

        Returns `(committed, index)`. A leader on the minority side of a
        partition returns `(False, -1)` - it can append to its own log, but it
        cannot commit, so the value is never acknowledged to the client.
        """
        leader = self.nodes[leader_id]
        if leader.role != RaftRole.LEADER:
            return False, -1

        new_index = leader.last_log_index + 1
        entry = LogEntry(term=leader.current_term, index=new_index, command=command)
        leader.log.append(entry)

        prev_index = new_index - 1
        prev_term = leader.log[prev_index - 1].term if prev_index > 0 else 0
        acks = 1                                     # the leader's own copy

        for peer_id in self.node_ids:
            if peer_id == leader_id:
                continue
            if not self.network.deliver(leader_id, peer_id):
                continue
            reply = self.nodes[peer_id].handle_append_entries(AppendEntriesArgs(
                term=leader.current_term,
                leader_id=leader_id,
                prev_log_index=prev_index,
                prev_log_term=prev_term,
                entries=[entry],
                leader_commit=leader.commit_index,
            ))
            if not self.network.deliver(peer_id, leader_id):
                continue
            if reply.success:
                acks += 1

        if acks < self.quorum_size:
            return False, -1

        leader.commit_index = new_index
        for peer_id in self.node_ids:
            if peer_id == leader_id or not self.network.deliver(leader_id, peer_id):
                continue
            self.nodes[peer_id].handle_append_entries(AppendEntriesArgs(
                term=leader.current_term,
                leader_id=leader_id,
                prev_log_index=new_index,
                prev_log_term=entry.term,
                entries=[],
                leader_commit=leader.commit_index,
            ))
        return True, new_index

    # -- inspection ---------------------------------------------------------

    def committed_commands(self, node_id: str) -> list[str]:
        node = self.nodes[node_id]
        return [e.command for e in node.log[:node.commit_index]]

    def divergence(self) -> list[tuple[int, dict[str, str]]]:
        """Indexes where two nodes have COMMITTED different commands.

        This must always be empty. It is the definition of split brain, and it
        is the single assertion every test in this harness ultimately makes.
        """
        conflicts = []
        longest = max((n.commit_index for n in self.nodes.values()), default=0)
        for index in range(1, longest + 1):
            at_index: dict[str, str] = {}
            for nid, node in self.nodes.items():
                if node.commit_index >= index and len(node.log) >= index:
                    at_index[nid] = node.log[index - 1].command
            if len(set(at_index.values())) > 1:
                conflicts.append((index, at_index))
        return conflicts
