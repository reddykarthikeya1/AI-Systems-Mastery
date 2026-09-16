#!/usr/bin/env python3
"""DEBUG LAB: Split-Vote Deadlock in Raft Leader Election Without Timeout Jitter

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def run_election(nodes: list[str]):
    _timeout = 150  # No jitter!
    votes = {n: 1 for n in nodes}  # Everyone votes for themselves
    if max(votes.values()) <= len(nodes) // 2:
        raise RuntimeError('Split-vote deadlock! No candidate attained majority quorum.')


def reproduce_defect():
    print("Executing defective simulation for Module_24_Distributed_Consensus_Raft_Vector_Clocks...")
    run_election(['node1', 'node2', 'node3'])
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[DEFECT TRIGGERED SUCCESSFULLY]\nException: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
