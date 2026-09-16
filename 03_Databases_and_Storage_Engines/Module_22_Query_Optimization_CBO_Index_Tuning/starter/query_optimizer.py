"""Module 22: Query Optimization, Cost-Based Optimizer & Physical Joins (Starter).

This template defines the architecture of database query optimization:
1. TableStatistics and catalog metadata management.
2. CostEstimator implementing selectivity estimation and the CBO cost model.
3. Access path selection (Index Scan vs Sequential Scan tipping point).
4. Physical join implementations: Nested Loop Join, Hash Join, and Sort-Merge Join.
"""

from __future__ import annotations

from typing import Any, Callable


class TableStatistics:
    """Catalog statistics used by the CBO for cardinality and selectivity estimation."""

    def __init__(
        self,
        table_name: str,
        total_pages: int,
        total_tuples: int,
        distinct_counts: dict[str, int] | None = None,
        mcv_frequencies: dict[str, dict[Any, float]] | None = None,
    ) -> None:
        self.table_name = table_name
        self.total_pages = total_pages
        self.total_tuples = total_tuples
        self.distinct_counts = distinct_counts or {}
        self.mcv_frequencies = mcv_frequencies or {}


class CostEstimator:
    """Cost-Based Optimizer model calculating physical plan costs."""

    def __init__(
        self,
        seq_page_cost: float = 1.0,
        random_page_cost: float = 4.0,
        cpu_tuple_cost: float = 0.01,
        cpu_operator_cost: float = 0.0025,
    ) -> None:
        raise NotImplementedError("Initialize CBO cost constants")

    def estimate_selectivity(self, stats: TableStatistics, col: str, op: str, value: Any) -> float:
        """Estimate predicate selectivity using MCV frequencies or uniform distribution (1 / NDV)."""
        raise NotImplementedError("Implement selectivity estimation")

    def estimate_seq_scan_cost(self, stats: TableStatistics) -> float:
        """Calculate total cost for sequential table scan."""
        raise NotImplementedError("Calculate sequential scan cost")

    def estimate_index_scan_cost(self, stats: TableStatistics, selectivity: float) -> float:
        """Calculate total cost for unclustered index scan based on random I/O and selectivity."""
        raise NotImplementedError("Calculate index scan cost")

    def choose_scan_path(
        self,
        stats: TableStatistics,
        col: str,
        op: str,
        value: Any,
    ) -> tuple[str, float]:
        """Compare Index Scan vs Sequential Scan cost, returning ('INDEX_SCAN' | 'SEQ_SCAN', best_cost)."""
        raise NotImplementedError("Select optimal access path")


class PhysicalJoins:
    """Physical join execution algorithms."""

    @staticmethod
    def nested_loop_join(
        outer: list[dict[str, Any]],
        inner: list[dict[str, Any]],
        predicate: Callable[[dict[str, Any], dict[str, Any]], bool],
    ) -> list[dict[str, Any]]:
        """Execute Nested Loop Join evaluating predicate across all outer x inner pairs."""
        raise NotImplementedError("Implement nested loop join")

    @staticmethod
    def hash_join(
        left: list[dict[str, Any]],
        right: list[dict[str, Any]],
        left_key: str,
        right_key: str,
    ) -> list[dict[str, Any]]:
        """Execute in-memory Hash Join (Build smaller input into hash table, probe larger)."""
        raise NotImplementedError("Implement hash join")

    @staticmethod
    def sort_merge_join(
        left: list[dict[str, Any]],
        right: list[dict[str, Any]],
        left_key: str,
        right_key: str,
    ) -> list[dict[str, Any]]:
        """Execute Sort-Merge Join (Sort both relations on keys, scan with dual pointers)."""
        raise NotImplementedError("Implement sort-merge join")
