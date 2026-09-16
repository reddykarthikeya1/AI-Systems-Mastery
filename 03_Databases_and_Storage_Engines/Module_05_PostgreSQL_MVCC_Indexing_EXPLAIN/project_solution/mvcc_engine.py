"""Module 05: PostgreSQL MVCC & Query Cost Estimator Engine Reference Solution.

Implements:
1. Heap tuple visibility logic across transaction snapshots.
2. An in-memory MVCC Table that simulates non-blocking concurrent UPDATEs.
3. A VACUUM garbage collection routine that purges dead tuples.
4. A Query Plan Cost Estimator computing Seq Scan vs Index Scan crossover point.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class HeapTuple:
    tuple_id: str
    data: dict[str, Any]
    xmin: int
    xmax: int = 0


@dataclass
class Snapshot:
    snapshot_xid: int
    xmin: int  # Any transaction with xid < xmin is known committed
    xmax: int  # Any transaction with xid >= xmax is invisible
    active_xids: set[int] = field(default_factory=set)

    def is_visible(self, t: HeapTuple) -> bool:
        """Evaluates whether heap tuple is visible to this snapshot."""
        # 1. Did creator transaction start after this snapshot, or is it currently active?
        if t.xmin >= self.xmax or t.xmin in self.active_xids:
            return False

        # 2. Was it created by an uncommitted transaction? (handled above)
        # 3. Was it deleted/superseded by another transaction?
        if t.xmax != 0:
            # If deleted by a transaction that committed before this snapshot, it's invisible
            if t.xmax < self.xmax and t.xmax not in self.active_xids:
                return False

        return True


class MVCCTable:
    """Simulates an MVCC heap table with update versioning and dead-tuple vacuuming."""

    def __init__(self, table_name: str) -> None:
        self.table_name = table_name
        self.tuples: list[HeapTuple] = []

    def insert(self, tuple_id: str, data: dict[str, Any], xid: int) -> None:
        """Appends a new live tuple version with xmin=xid, xmax=0."""
        self.tuples.append(HeapTuple(tuple_id=tuple_id, data=data, xmin=xid, xmax=0))

    def update(self, tuple_id: str, new_data: dict[str, Any], xid: int) -> bool:
        """Sets xmax=xid on current active version and inserts new version with xmin=xid."""
        target: HeapTuple | None = None
        for t in reversed(self.tuples):
            if t.tuple_id == tuple_id and t.xmax == 0:
                target = t
                break

        if not target:
            return False

        target.xmax = xid
        self.tuples.append(HeapTuple(tuple_id=tuple_id, data=new_data, xmin=xid, xmax=0))
        return True

    def delete(self, tuple_id: str, xid: int) -> bool:
        """Sets xmax=xid on current active version without inserting a new tuple."""
        for t in reversed(self.tuples):
            if t.tuple_id == tuple_id and t.xmax == 0:
                t.xmax = xid
                return True
        return False

    def select(self, snapshot: Snapshot) -> list[dict[str, Any]]:
        """Returns all tuples visible under the given snapshot."""
        results = []
        for t in self.tuples:
            if snapshot.is_visible(t):
                results.append(dict(t.data))
        return results

    def vacuum(self, oldest_active_xid: int) -> int:
        """Reclaims dead tuples whose xmax is older than oldest_active_xid.

        Returns the number of reclaimed dead tuples.
        """
        retained: list[HeapTuple] = []
        dead_count = 0

        for t in self.tuples:
            # A tuple is eligible for vacuum cleanup if it has been deleted/superseded
            # and the deleting transaction is older than the oldest running active snapshot
            if t.xmax != 0 and t.xmax < oldest_active_xid:
                dead_count += 1
            else:
                retained.append(t)

        self.tuples = retained
        return dead_count


class QueryCostEstimator:
    """Calculates query execution cost for Sequential Scan vs Index Scan."""

    def __init__(
        self,
        seq_page_cost: float = 1.0,
        random_page_cost: float = 4.0,
        cpu_tuple_cost: float = 0.01,
        cpu_operator_cost: float = 0.0025,
        cpu_index_tuple_cost: float = 0.005,
    ) -> None:
        self.seq_page_cost = seq_page_cost
        self.random_page_cost = random_page_cost
        self.cpu_tuple_cost = cpu_tuple_cost
        self.cpu_operator_cost = cpu_operator_cost
        self.cpu_index_tuple_cost = cpu_index_tuple_cost

    def estimate_seq_scan_cost(self, table_pages: int, total_tuples: int) -> float:
        """Cost = (table_pages * seq_page_cost) + (total_tuples * (cpu_tuple_cost + cpu_operator_cost))."""
        io_cost = table_pages * self.seq_page_cost
        cpu_cost = total_tuples * (self.cpu_tuple_cost + self.cpu_operator_cost)
        return round(io_cost + cpu_cost, 2)

    def estimate_index_scan_cost(
        self,
        total_tuples: int,
        selectivity: float,
        index_tree_depth: int = 4,
    ) -> float:
        """Estimates B-Tree index scan cost using random page lookups."""
        matching_rows = total_tuples * selectivity
        # Root-to-leaf traversal pages + random page cost per matching tuple
        index_pages_read = index_tree_depth + (matching_rows * 0.1)
        io_cost = (index_pages_read * self.random_page_cost) + (matching_rows * self.random_page_cost)
        cpu_cost = matching_rows * (self.cpu_index_tuple_cost + self.cpu_tuple_cost)
        return round(io_cost + cpu_cost, 2)

    def select_cheapest_plan(self, table_pages: int, total_tuples: int, selectivity: float) -> str:
        """Returns 'Seq Scan' or 'Index Scan' depending on which has lower cost."""
        seq_cost = self.estimate_seq_scan_cost(table_pages, total_tuples)
        idx_cost = self.estimate_index_scan_cost(total_tuples, selectivity)
        return "Index Scan" if idx_cost < seq_cost else "Seq Scan"
