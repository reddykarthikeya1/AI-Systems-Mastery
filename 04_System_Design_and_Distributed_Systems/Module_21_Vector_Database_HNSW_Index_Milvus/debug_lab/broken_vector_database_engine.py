#!/usr/bin/env python3
"""DEBUG LAB: HNSW Graph Disconnection Isolates Vector Subsets from Search

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def delete_hnsw_node(graph: dict, node_id: int):
    if node_id in graph:
        del graph[node_id]
        # Did not reconnect neighbors of deleted node! Graph is now severed.
        raise RuntimeError('HNSW graph severed! Navigable paths broken, search recall collapsed.')


def reproduce_defect():
    print("Executing defective simulation for Module_21_Vector_Database_HNSW_Index_Milvus...")
    delete_hnsw_node({1: [2], 2: [1, 3], 3: [2]}, 2)
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[DEFECT TRIGGERED SUCCESSFULLY]\nException: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
