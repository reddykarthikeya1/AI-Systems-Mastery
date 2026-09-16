"""Module 23: Transactions, Write Skew & Raft Consensus Demo.

Demonstrates:
1. The Write Skew anomaly breaking business invariants under Snapshot Isolation.
2. Two-Phase Commit (2PC) atomic commit and abort voting.
3. Raft distributed consensus leader election with majority voting.
"""

from __future__ import annotations


def demo_write_skew() -> None:
    print("=" * 75)
    print("    1. SNAPSHOT ISOLATION ANOMALY: WRITE SKEW")
    print("=" * 75)

    # Invariant: At least 1 doctor on call
    db_state = {"Alice": True, "Bob": True}
    print(f"Initial State: Alice on-call={db_state['Alice']}, Bob on-call={db_state['Bob']}")
    print("Business Invariant: Count(on_call == True) >= 1\n")

    # Tx 1: Dr. Alice wants to take time off
    # Snapshot at start of Tx 1
    snap_1 = dict(db_state)
    on_call_count_1 = sum(1 for v in snap_1.values() if v)
    print(f"Tx 1 (Alice): Reads on_call count = {on_call_count_1}. (Count >= 1 holds!)")

    # Tx 2: Dr. Bob concurrently wants to take time off
    # Snapshot at start of Tx 2
    snap_2 = dict(db_state)
    on_call_count_2 = sum(1 for v in snap_2.values() if v)
    print(f"Tx 2 (Bob)  : Reads on_call count = {on_call_count_2}. (Count >= 1 holds!)")

    # Both transactions proceed because their write sets are disjoint!
    print("\nExecuting mutations:")
    print("  -> Tx 1 updates 'Alice' -> False")
    db_state["Alice"] = False

    print("  -> Tx 2 updates 'Bob'   -> False (No write conflict! Different key)")
    db_state["Bob"] = False

    final_count = sum(1 for v in db_state.values() if v)
    print(f"\nFinal State: Alice={db_state['Alice']}, Bob={db_state['Bob']}")
    print(f"Final On-Call Doctors: {final_count}")
    print("Result: [VIOLATION] Write Skew corrupted invariant! Zero doctors are on-call.")
    print("Serializable Snapshot Isolation (SSI) prevents this by detecting rw-antidependencies!")


def demo_two_phase_commit() -> None:
    print("\n" + "=" * 75)
    print("    2. DISTRIBUTED TRANSACTIONS: TWO-PHASE COMMIT (2PC)")
    print("=" * 75)

    participants = ["Shard_US_East", "Shard_EU_Central", "Shard_AP_Tokyo"]
    print(f"Coordinating distributed commit across shards: {participants}")

    # Phase 1: Prepare Phase
    print("\nPhase 1 (PREPARE): Coordinator asks participants to prepare locks & WAL")
    votes = {
        "Shard_US_East": True,     # Vote YES
        "Shard_EU_Central": True,  # Vote YES
        "Shard_AP_Tokyo": False,   # Vote NO (e.g. disk full / lock timeout)
    }

    for shard, vote in votes.items():
        print(f"  [{shard}] Voted: {'YES' if vote else 'NO (Abort)'}")

    # Coordinator decision
    all_yes = all(votes.values())
    decision = "COMMIT" if all_yes else "GLOBAL ABORT"

    print(f"\nPhase 2 (DECISION): Coordinator broadcasts '{decision}'")
    print("  -> Result: All shards rollback prepared locks. Atomicity preserved across network!")


def demo_raft_election() -> None:
    print("\n" + "=" * 75)
    print("    3. RAFT DISTRIBUTED CONSENSUS: LEADER ELECTION")
    print("=" * 75)

    nodes = ["Node_1", "Node_2", "Node_3", "Node_4", "Node_5"]
    majority_needed = len(nodes) // 2 + 1
    print(f"Cluster Size: {len(nodes)} nodes | Majority Quorum Needed: {majority_needed} votes")

    candidate = "Node_1"
    term = 1
    print(f"\nLeader heartbeat timed out! {candidate} transitions to CANDIDATE for Term {term}.")
    print(f"{candidate} votes for itself (1 vote). Broadcasts RequestVote RPC to peers:")

    # Simulated peer responses
    votes_received = {
        "Node_1": True,  # Voted for itself
        "Node_2": True,  # Voted YES
        "Node_3": True,  # Voted YES
        "Node_4": False, # Network partitioned
        "Node_5": False, # Already voted in term
    }

    total_yes = sum(1 for v in votes_received.values() if v)
    print(f"Votes Counted: {total_yes} / {len(nodes)}")

    if total_yes >= majority_needed:
        print(f"Result: Quorum ({total_yes} >= {majority_needed}) reached! {candidate} elected LEADER.")
        print(f"{candidate} sends initial heartbeat AppendEntries to assert authority.")


def main() -> None:
    demo_write_skew()
    demo_two_phase_commit()
    demo_raft_election()


if __name__ == "__main__":
    main()
