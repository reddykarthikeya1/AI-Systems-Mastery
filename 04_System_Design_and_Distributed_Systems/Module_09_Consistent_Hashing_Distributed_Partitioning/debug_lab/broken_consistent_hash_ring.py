#!/usr/bin/env python3
"""DEBUG LAB: Hot Partition Cascade Triggered by Inadequate Virtual Node Density

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

class DefectiveHashRing:
    def __init__(self, nodes: list[str]):
        self.ring = {hash(n) % 1000: n for n in nodes}


def reproduce_defect():
    print("Executing defective simulation for Module_09_Consistent_Hashing_Distributed_Partitioning...")
    _ = DefectiveHashRing(['nodeA', 'nodeB', 'nodeC'])
    raise RuntimeError('With 1 vnode, token spacing is non-uniform; one node handles >70% of keys!')
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[DEFECT TRIGGERED SUCCESSFULLY]\nException: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
