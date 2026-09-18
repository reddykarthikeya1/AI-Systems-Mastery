"""DEBUG LAB: Split-Brain Dual Leader Election in Raft Cluster

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

def wins_election(votes_received: int, cluster_size: int) -> bool:
    """Should require a strict majority; instead uses a fixed threshold of 2
    votes regardless of how large the cluster actually is."""
    return votes_received >= 2  # majority for a 5-node cluster is 3, not 2

def reproduce_defect() -> None:
    print("Two candidates request votes in the same term on a 5-node cluster...")
    cluster_size = 5
    node_a_votes = 2
    node_b_votes = 3

    node_a_is_leader = wins_election(node_a_votes, cluster_size)
    node_b_is_leader = wins_election(node_b_votes, cluster_size)

    print(f"Node A claims leadership with {node_a_votes}/{cluster_size} votes: {node_a_is_leader}")
    print(f"Node B claims leadership with {node_b_votes}/{cluster_size} votes: {node_b_is_leader}")

    if node_a_is_leader and node_b_is_leader:
        print("[DEFECT OBSERVED] Two nodes are simultaneously LEADER in the same "
              "term -- split brain. A correct quorum check (>= 3/5) would have "
              "rejected node A's 2-vote claim.")
        log_index_5_on_a = "SET balance=100"
        log_index_5_on_b = "SET balance=250"
        print(f"Node A commits log[5] = {log_index_5_on_a!r}")
        print(f"Node B commits log[5] = {log_index_5_on_b!r}")
        if log_index_5_on_a != log_index_5_on_b:
            print("[DEFECT OBSERVED] The cluster now has two different committed "
                  "values at the same log index.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
