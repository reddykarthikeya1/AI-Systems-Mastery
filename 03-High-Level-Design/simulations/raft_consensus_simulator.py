"""
================================================================================
SIMULATION 02: Raft Distributed Consensus Simulator (Leader Election)
================================================================================
Zero-Prerequisite Intuition:
Imagine a committee of 5 people who must pick a single Chairperson (Leader).
If the current Chairperson stops speaking for 3 seconds, anyone can raise their
hand and say: "I want to be Chairperson! Vote for me!"
If 3 out of 5 people (a Quorum: N/2 + 1) vote YES, that person becomes the Leader.
The Leader immediately sends regular "I am alive" heartbeats so nobody else tries
to hold an election.

Run this script to observe Raft leader election, terms, and heartbeats live!
================================================================================
"""

import time
import random
from enum import Enum
from typing import List

class NodeRole(Enum):
    FOLLOWER = "Follower"
    CANDIDATE = "Candidate"
    LEADER = "Leader"

class RaftNode:
    def __init__(self, node_id: int, cluster: List["RaftNode"]):
        self.node_id = node_id
        self.cluster = cluster
        self.role = NodeRole.FOLLOWER
        self.current_term = 0
        self.voted_for = None
        self.votes_received = 0
        
        # Randomized election timeout between 150ms and 300ms
        self.election_timeout_ms = random.randint(150, 300)
        self.last_heartbeat_time = time.monotonic() * 1000

    def check_election_timeout(self):
        now = time.monotonic() * 1000
        if self.role != NodeRole.LEADER:
            if now - self.last_heartbeat_time > self.election_timeout_ms:
                self.start_election()

    def start_election(self):
        self.role = NodeRole.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        self.votes_received = 1 # Votes for self
        self.last_heartbeat_time = time.monotonic() * 1000
        # Reset randomized timeout to avoid repeated split votes
        self.election_timeout_ms = random.randint(150, 300)
        
        print(f"[ELECTION] Node {self.node_id} became CANDIDATE for Term {self.current_term}!")
        
        # Broadcast RequestVote RPCs to all peers
        quorum = (len(self.cluster) // 2) + 1
        for peer in self.cluster:
            if peer.node_id != self.node_id:
                if peer.request_vote(self.current_term, self.node_id):
                    self.votes_received += 1

        if self.votes_received >= quorum:
            self.become_leader()

    def request_vote(self, candidate_term: int, candidate_id: int) -> bool:
        if candidate_term > self.current_term:
            self.current_term = candidate_term
            self.role = NodeRole.FOLLOWER
            self.voted_for = None

        if candidate_term == self.current_term and (self.voted_for is None or self.voted_for == candidate_id):
            self.voted_for = candidate_id
            self.last_heartbeat_time = time.monotonic() * 1000 # Reset timeout on grant
            return True
        return False

    def become_leader(self):
        self.role = NodeRole.LEADER
        print(f"[LEADER ELECTED] >>> Node {self.node_id} is now LEADER for Term {self.current_term}! (Received {self.votes_received} votes) <<<")

    def broadcast_heartbeats(self):
        if self.role == NodeRole.LEADER:
            for peer in self.cluster:
                if peer.node_id != self.node_id:
                    peer.receive_heartbeat(self.current_term, self.node_id)

    def receive_heartbeat(self, term: int, leader_id: int):
        if term >= self.current_term:
            self.current_term = term
            self.role = NodeRole.FOLLOWER
            self.last_heartbeat_time = time.monotonic() * 1000


def run_raft_simulation():
    print("--- [STAGE 1] Spinning Up 5-Node Raft Cluster (Quorum = 3) ---")
    cluster: List[RaftNode] = []
    for i in range(5):
        cluster.append(RaftNode(node_id=i, cluster=[]))
    
    for node in cluster:
        node.cluster = cluster

    print("Nodes initialized as Followers. Advancing clock to trigger election...")
    
    # Tick simulation forward until a leader is chosen
    leader = None
    start = time.monotonic()
    while not leader and (time.monotonic() - start < 2.0):
        time.sleep(0.02)
        for node in cluster:
            node.check_election_timeout()
            if node.role == NodeRole.LEADER:
                leader = node
                break

    assert leader is not None, "Leader should have been elected!"
    
    print("\n--- [STAGE 2] Leader Maintaining Heartbeats ---")
    for _ in range(3):
        time.sleep(0.05)
        leader.broadcast_heartbeats()
        print(f"Leader {leader.node_id} broadcasted AppendEntries heartbeat. Term: {leader.current_term}")

    print("\n--- [STAGE 3] Leader Crashes! (Simulating Failover) ---")
    print(f"Simulating sudden power loss on Leader {leader.node_id}...")
    dead_leader_id = leader.node_id
    surviving_cluster = [n for n in cluster if n.node_id != dead_leader_id]
    for n in surviving_cluster:
        n.cluster = surviving_cluster

    # Advance clock without leader heartbeats to trigger new election
    new_leader = None
    start = time.monotonic()
    while not new_leader and (time.monotonic() - start < 2.0):
        time.sleep(0.02)
        for node in surviving_cluster:
            node.check_election_timeout()
            if node.role == NodeRole.LEADER:
                new_leader = node
                break

    print(f"\n[FAILOVER RECOVERY SUCCESSFUL] New Leader {new_leader.node_id} elected in Term {new_leader.current_term}!")

if __name__ == "__main__":
    run_raft_simulation()
