"""Module 16: Graph Databases, Index-Free Adjacency & Cypher Demo.

Demonstrates:
1. Index-Free Adjacency direct pointer dereference vs multi-table index lookup.
2. Shortest Path graph navigation using Breadth-First Search (BFS).
3. Circular fraud ring cycle detection in payment networks.
"""

from __future__ import annotations

from collections import deque


class DemoGraphNode:
    """A node maintaining direct physical reference pointers to its relationships (Index-Free Adjacency)."""

    def __init__(self, node_id: str, label: str, name: str) -> None:
        self.node_id = node_id
        self.label = label
        self.name = name
        # Direct references: outgoing and incoming edges
        self.outgoing: list[DemoGraphEdge] = []
        self.incoming: list[DemoGraphEdge] = []


class DemoGraphEdge:
    """A directed edge linking start node and end node directly."""

    def __init__(self, rel_type: str, start_node: DemoGraphNode, end_node: DemoGraphNode, props: dict) -> None:
        self.rel_type = rel_type
        self.start_node = start_node
        self.end_node = end_node
        self.props = props


def demo_index_free_adjacency() -> None:
    print("=" * 75)
    print("    1. INDEX-FREE ADJACENCY (IFA) vs RELATIONAL INDEX SEARCH")
    print("=" * 75)

    # Build connected nodes with direct pointer linking
    alice = DemoGraphNode("u1", "User", "Alice")
    bob = DemoGraphNode("u2", "User", "Bob")
    carol = DemoGraphNode("u3", "User", "Carol")
    gadget = DemoGraphNode("p1", "Product", "Quantum Laptop")

    # Connect via pointers
    rel1 = DemoGraphEdge("FOLLOWS", alice, bob, {"since": 2023})
    alice.outgoing.append(rel1)
    bob.incoming.append(rel1)

    rel2 = DemoGraphEdge("FOLLOWS", bob, carol, {"since": 2024})
    bob.outgoing.append(rel2)
    carol.incoming.append(rel2)

    rel3 = DemoGraphEdge("PURCHASED", carol, gadget, {"amount": 2500})
    carol.outgoing.append(rel3)
    gadget.incoming.append(rel3)

    # 3-hop traversal: Alice -> Bob -> Carol -> Product
    print(f"Starting Node: {alice.name}")
    curr = alice
    path_names = [curr.name]

    # Hop 1
    edge1 = curr.outgoing[0]
    curr = edge1.end_node
    path_names.append(f"-[:{edge1.rel_type}]-> {curr.name}")

    # Hop 2
    edge2 = curr.outgoing[0]
    curr = edge2.end_node
    path_names.append(f"-[:{edge2.rel_type}]-> {curr.name}")

    # Hop 3
    edge3 = curr.outgoing[0]
    curr = edge3.end_node
    path_names.append(f"-[:{edge3.rel_type}]-> {curr.name} ({curr.label})")

    print(f"Traversal Path: {' '.join(path_names)}")
    print("Execution Mechanism: 3 raw memory pointer hops in O(1) time per relationship.")
    print("In RDBMS: Would have required 4 table scans and 3 foreign key B-Tree index lookups!")


def demo_fraud_cycle_detection() -> None:
    print("\n" + "=" * 75)
    print("    2. FRAUD DETECTION: CIRCULAR MONEY-LAUNDERING RING")
    print("=" * 75)

    # Accounts in a cyclic transfer ring
    # Acc_A -> Acc_B -> Acc_C -> Acc_D -> Acc_A
    transfers = {
        "Acc_A": ["Acc_B"],
        "Acc_B": ["Acc_C"],
        "Acc_C": ["Acc_D"],
        "Acc_D": ["Acc_A"],  # Cycle closure!
        "Acc_Safe": ["Acc_Store"],
    }

    # Detect cycles using DFS path exploration
    def find_cycles(start_node: str) -> list[list[str]]:
        cycles = []
        queue = deque([[start_node]])

        while queue:
            path = queue.popleft()
            last = path[-1]

            for neighbor in transfers.get(last, []):
                if neighbor == start_node and len(path) >= 3:
                    cycles.append(path + [neighbor])
                elif neighbor not in path and len(path) < 6:
                    queue.append(path + [neighbor])

        return cycles

    detected = find_cycles("Acc_A")
    print("Investigating transfers originating from 'Acc_A':")
    for cycle in detected:
        print(f"  [ALERT] Fraud Ring Detected! Closed cycle: {' -> '.join(cycle)}")


def main() -> None:
    demo_index_free_adjacency()
    demo_fraud_cycle_detection()


if __name__ == "__main__":
    main()
