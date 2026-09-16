"""Module 05 Starter: PostgreSQL MVCC & Query Cost Estimator Engine.

TODO for Student:
Implement:
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
        raise NotImplementedError("Implement PostgreSQL MVCC snapshot visibility rules")


class MVCCTable:
    """Simulates an MVCC heap table with update versioning and dead-tuple vacuuming."""

    def __init__(self, table_name: str) -> None:
        self.table_name = table_name
        self.tuples: list[HeapTuple] = []

    def insert(self, tuple_id: str, data: dict[str, Any], xid: int) -> None:
        """Appends a new live tuple version with xmin=xid, xmax=0."""
        raise NotImplementedError("Implement tuple insertion")

    def update(self, tuple_id: str, new_data: dict[str, Any], xid: int) -> bool:
        """Sets xmax=xid on current active version and inserts new version with xmin=xid."""
        raise NotImplementedError("Implement non-overwriting MVCC update")

    def select(self, snapshot: Snapshot) -> list[dict[str, Any]]:
        """Returns all tuples visible under the given snapshot."""
        raise NotImplementedError("Filter tuples using snapshot.is_visible()")

    def vacuum(self, oldest_active_xid: int) -> int:
        """Reclaims dead tuples whose xmax is older than oldest_active_xid.

        Returns the number of reclaimed dead tuples.
        """
        raise NotImplementedError("Implement VACUUM dead-tuple reclamation")


class QueryCostEstimator:
    """Calculates query execution cost for Sequential Scan vs Index Scan."""

    def __init__(
        self,
        seq_page_cost: float = 1.0,
        random_page_cost: float = 4.0,
        cpu_tuple_cost: float = 0.01,
        cpu_operator_cost: float = 0.0025,
    ) -> None:
        self.seq_page_cost = seq_page_cost
        self.random_page_cost = random_page_cost
        self.cpu_tuple_cost = cpu_tuple_cost
        self.cpu_operator_cost = cpu_operator_cost

    def estimate_seq_scan_cost(self, table_pages: int, total_tuples: int) -> float:
        """Cost = (table_pages * seq_page_cost) + (total_tuples * (cpu_tuple_cost + cpu_operator_cost))."""
        raise NotImplementedError("Calculate sequential scan cost")

    def estimate_index_scan_cost(
        self,
        total_tuples: int,
        selectivity: float,
        index_tree_depth: int = 4,
    ) -> float:
        """Estimates B-Tree index scan cost using random page lookups."""
        raise NotImplementedError("Calculate index scan cost")

    def select_cheapest_plan(self, table_pages: int, total_tuples: int, selectivity: float) -> str:
        """Returns 'Seq Scan' or 'Index Scan' depending on which has lower cost."""
        raise NotImplementedError("Compare plans and return winning plan name")
