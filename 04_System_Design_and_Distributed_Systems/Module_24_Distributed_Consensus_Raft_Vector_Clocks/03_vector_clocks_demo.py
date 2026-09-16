"""Module 24: Standalone Interactive Demo - Vector Clocks & Raft Consensus Cluster."""

from project_solution.raft_cluster_engine import (
    RaftCluster,
    VectorClock,
)


def main() -> None:
    print("=" * 80)
    print(" MODULE 24: DISTRIBUTED CONSENSUS (RAFT) & CAUSAL VECTOR CLOCKS")
    print("=" * 80)

    # ---------------------------------------------------------
    # Part 1: Vector Clocks & Causality Detection
    # ---------------------------------------------------------
    print("\n--- 1. Vector Clocks & Causality Tracking ---")
    vc_a = VectorClock()
    vc_b = VectorClock()
    vc_c = VectorClock()

    # Step 1: Node A performs internal event
    vc_a.tick("A")
    print(f" Event 1 (A internal):  Clock A = {vc_a.clock}")

    # Step 2: Node A sends message to Node B
    msg_clock = vc_a.send_event("A")
    print(f" Event 2 (A sends):     Clock A = {vc_a.clock}")
    vc_b.receive_event("B", msg_clock)
    print(f" Event 3 (B receives):  Clock B = {vc_b.clock}")

    rel_ab = VectorClock.compare(vc_a, vc_b)
    print(f" Causality Check (A vs B): {rel_ab.value} (A happened-before B: Guaranteed causally ordered)")

    # Step 3: Node C performs independent event without communicating with A or B
    vc_c.tick("C")
    print(f" Event 4 (C internal):  Clock C = {vc_c.clock}")

    rel_ac = VectorClock.compare(vc_a, vc_c)
    print(f" Causality Check (A vs C): {rel_ac.value} (Concurrent updates! Branch detected -> Requires merge)")

    # ---------------------------------------------------------
    # Part 2: Raft Consensus Cluster (Leader Election & Quorum Replication)
    # ---------------------------------------------------------
    print("\n--- 2. Raft Cluster Simulation: Election & Quorum Replication ---")
    node_ids = ["node_1", "node_2", "node_3"]
    cluster = RaftCluster(node_ids)
    print(f" Cluster Nodes: {node_ids} | Majority Quorum Required: {cluster.quorum_size} nodes")

    # Round 1: Node 1 initiates election
    print("\n [ELECTION] Node 1 initiates election for Term 1...")
    elected = cluster.run_election("node_1")
    print(f" Election Success: {elected} | Node 1 Role: {cluster.nodes['node_1'].role.value}")

    # Client Write to Leader
    cmd1 = "SET account_balance_101 = 5000"
    print(f"\n [CLIENT WRITE] Issuing command: '{cmd1}' to Leader 'node_1'...")
    success, commit_idx = cluster.client_write("node_1", cmd1)
    print(f" Quorum Commit Success: {success} | Committed Log Index: {commit_idx}")

    for nid in node_ids:
        node = cluster.nodes[nid]
        log_summary = [(e.term, e.index, e.command) for e in node.log]
        print(f"   {nid:<8}: Role={node.role.value:<9} | Term={node.current_term} | CommitIdx={node.commit_index} | Log={log_summary}")

    # Round 2: Failover to Node 2
    print("\n [FAILOVER] Node 1 partitioned/crashed! Node 2 times out and starts Term 2 election...")
    elected_2 = cluster.run_election("node_2")
    print(f" Node 2 Election Success: {elected_2} | Node 2 Role: {cluster.nodes['node_2'].role.value}")

    cmd2 = "UPDATE account_balance_101 = 6200"
    success2, commit_idx2 = cluster.client_write("node_2", cmd2)
    print(f" Write to new Leader: Success={success2} | Committed Log Index: {commit_idx2}")

    for nid in ["node_2", "node_3"]:
        node = cluster.nodes[nid]
        log_summary = [(e.term, e.index, e.command) for e in node.log]
        print(f"   {nid:<8}: Role={node.role.value:<9} | Term={node.current_term} | CommitIdx={node.commit_index} | Log={log_summary}")

    print("=" * 80)


if __name__ == "__main__":
    main()
