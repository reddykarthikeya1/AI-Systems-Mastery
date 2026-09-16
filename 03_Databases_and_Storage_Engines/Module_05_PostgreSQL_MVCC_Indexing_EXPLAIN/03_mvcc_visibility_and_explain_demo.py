"""Module 05: PostgreSQL MVCC Visibility & Query Cost Model Demo.

Demonstrates:
1. Heap tuple versioning with t_xmin and t_xmax.
2. Snapshot visibility isolation across concurrent transactions.
3. Query Planner cost calculation comparing Sequential Scan vs Index Scan.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HeapTuple:
    tuple_id: int
    data: dict[str, int | str]
    xmin: int
    xmax: int = 0  # 0 indicates live/active


@dataclass
class TransactionSnapshot:
    snapshot_xid: int
    xmin: int  # Earliest still-active transaction
    xmax: int  # First unassigned transaction (any xid >= xmax is invisible)
    active_xids: set[int]

    def is_visible(self, t: HeapTuple) -> bool:
        """Evaluates whether heap tuple is visible to this snapshot."""
        # 1. Did creator transaction abort or not commit? (xmin >= xmax or in active list)
        if t.xmin >= self.xmax or t.xmin in self.active_xids:
            return False

        # 2. Was it deleted/superseded by an already-committed transaction before snapshot?
        if t.xmax != 0:
            if t.xmax < self.xmax and t.xmax not in self.active_xids:
                return False  # Deleted by an earlier committed transaction

        return True


def demo_mvcc_snapshots() -> None:
    print("=" * 75)
    print("       1. POSTGRESQL MVCC TUPLE VISIBILITY DEMO")
    print("=" * 75)

    # Simulation timeline:
    # Tx 100: Inserts Alice (balance: 100)
    # Tx 105: Starts long-running analytics query (Snapshot: xmin=105, xmax=106, active={})
    # Tx 110: Updates Alice (balance: 150) -> xmax of v1 becomes 110, inserts v2 with xmin=110
    # Tx 110: Commits
    # Tx 115: Starts (Snapshot: xmin=115, xmax=116, active={})

    v1 = HeapTuple(tuple_id=1, data={"name": "Alice", "balance": 100}, xmin=100, xmax=110)
    v2 = HeapTuple(tuple_id=1, data={"name": "Alice", "balance": 150}, xmin=110, xmax=0)

    # Long-running reader snapshot taken before Tx 110 committed
    snap_reader_105 = TransactionSnapshot(snapshot_xid=105, xmin=100, xmax=106, active_xids=set())

    # Newer reader snapshot taken after Tx 110 committed
    snap_reader_115 = TransactionSnapshot(snapshot_xid=115, xmin=111, xmax=116, active_xids=set())

    print("State: Tx 100 created Alice ($100), Tx 110 updated Alice ($150).")
    print("\nEvaluating Query: SELECT balance FROM accounts WHERE name = 'Alice'")
    print(f"  -> Reader Tx 105 sees Version 1 (Balance $100): {snap_reader_105.is_visible(v1)}")
    print(f"  -> Reader Tx 105 sees Version 2 (Balance $150): {snap_reader_105.is_visible(v2)}")
    print("  => Result for Tx 105: Balance = $100 (Isolated from uncommitted/future writes!)")

    print(f"\n  -> Reader Tx 115 sees Version 1 (Balance $100): {snap_reader_115.is_visible(v1)}")
    print(f"  -> Reader Tx 115 sees Version 2 (Balance $150): {snap_reader_115.is_visible(v2)}")
    print("  => Result for Tx 115: Balance = $150 (Sees updated committed data!)")


def demo_query_planner_cost_model() -> None:
    print("\n" + "=" * 75)
    print("       2. QUERY PLANNER COST MODEL (SEQ SCAN vs B-TREE INDEX)")
    print("=" * 75)

    # PostgreSQL default cost parameters
    seq_page_cost = 1.0
    random_page_cost = 4.0
    cpu_tuple_cost = 0.01
    cpu_index_tuple_cost = 0.005
    cpu_operator_cost = 0.0025

    table_pages = 10_000       # 80 MB table (8KB pages)
    total_tuples = 1_000_000   # 1 Million rows

    # Cost of Sequential Scan:
    # cost = (table_pages * seq_page_cost) + (total_tuples * (cpu_tuple_cost + cpu_operator_cost))
    seq_scan_cost = (table_pages * seq_page_cost) + (total_tuples * (cpu_tuple_cost + cpu_operator_cost))

    print(f"Table Size : {table_pages:,} pages | Rows : {total_tuples:,}")
    print(f"Sequential Scan Estimated Cost : {seq_scan_cost:,.2f} units\n")

    print(f"{'Selectivity (% Matching)':<25} | {'Index Scan Cost':<20} | {'Cheapest Choice':<18}")
    print("-" * 75)

    for selectivity in [0.0001, 0.001, 0.01, 0.05, 0.10, 0.25]:
        matching_rows = total_tuples * selectivity
        # B-Tree root-to-leaf traversal = ~4 page reads + random page cost per matching heap tuple
        index_pages_read = 4 + (matching_rows * 0.1)
        index_cost = (
            (index_pages_read * random_page_cost)
            + (matching_rows * random_page_cost)  # random access into heap page for each tuple
            + (matching_rows * (cpu_index_tuple_cost + cpu_tuple_cost))
        )
        winner = "B-Tree Index" if index_cost < seq_scan_cost else "Sequential Scan"
        print(f"{selectivity * 100:<25.2f}% | {index_cost:<20,.2f} | {winner:<18}")

    print("=" * 75)
    print("Key Insight: Above ~10-15% selectivity, PostgreSQL switches to Sequential Scan")
    print("because random disk I/O (random_page_cost=4.0) becomes slower than streaming disk blocks!")


def main() -> None:
    demo_mvcc_snapshots()
    demo_query_planner_cost_model()


if __name__ == "__main__":
    main()
