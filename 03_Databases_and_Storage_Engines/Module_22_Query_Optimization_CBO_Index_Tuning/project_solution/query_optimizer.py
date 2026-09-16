"""Module 22: Query Optimization, Cost-Based Optimizer & Physical Joins (Solution).

This is a pure-Python MODEL of cost-based query optimization (CBO), join ordering, and plan selection, built to make the
mechanism visible. It does not connect to a live database optimizer. For real EXPLAIN plans,
real cost models and real query tuning, see `explain_live.py`.

Implements:
1. TableStatistics: Catalog metadata with NDV and MCV frequency distributions.
2. CostEstimator: CBO cost model and Index Scan vs Sequential Scan access path selection.
3. PhysicalJoins: Nested Loop Join, Hash Join, and Sort-Merge Join algorithms.
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
        self.seq_page_cost = seq_page_cost
        self.random_page_cost = random_page_cost
        self.cpu_tuple_cost = cpu_tuple_cost
        self.cpu_operator_cost = cpu_operator_cost

    def estimate_selectivity(self, stats: TableStatistics, col: str, op: str, value: Any) -> float:
        # 1. Most Common Values (MCV) lookup
        if col in stats.mcv_frequencies and value in stats.mcv_frequencies[col]:
            return stats.mcv_frequencies[col][value]

        # 2. Uniform distribution approximation via NDV
        if op == "=":
            ndv = stats.distinct_counts.get(col, 50)
            return 1.0 / max(1, ndv)
        elif op in (">", "<", ">=", "<="):
            return 0.33  # Standard textbook default 1/3 range selectivity
        return 0.05

    def estimate_seq_scan_cost(self, stats: TableStatistics) -> float:
        io_cost = stats.total_pages * self.seq_page_cost
        cpu_cost = stats.total_tuples * (self.cpu_tuple_cost + self.cpu_operator_cost)
        return round(io_cost + cpu_cost, 4)

    def estimate_index_scan_cost(self, stats: TableStatistics, selectivity: float) -> float:
        matched_tuples = max(1.0, stats.total_tuples * selectivity)
        # Unclustered index: each matched tuple may trigger random page I/O (capped at total pages)
        rand_pages = min(float(stats.total_pages), matched_tuples)
        io_cost = rand_pages * self.random_page_cost
        cpu_cost = matched_tuples * (self.cpu_tuple_cost + self.cpu_operator_cost)
        return round(io_cost + cpu_cost, 4)

    def choose_scan_path(
        self,
        stats: TableStatistics,
        col: str,
        op: str,
        value: Any,
    ) -> tuple[str, float]:
        sel = self.estimate_selectivity(stats, col, op, value)
        seq_cost = self.estimate_seq_scan_cost(stats)
        idx_cost = self.estimate_index_scan_cost(stats, sel)

        if idx_cost < seq_cost:
            return "INDEX_SCAN", idx_cost
        return "SEQ_SCAN", seq_cost


class PhysicalJoins:
    """Physical join execution algorithms."""

    @staticmethod
    def nested_loop_join(
        outer: list[dict[str, Any]],
        inner: list[dict[str, Any]],
        predicate: Callable[[dict[str, Any], dict[str, Any]], bool],
    ) -> list[dict[str, Any]]:
        matches: list[dict[str, Any]] = []
        for r in outer:
            for s in inner:
                if predicate(r, s):
                    matches.append({**r, **s})
        return matches

    @staticmethod
    def hash_join(
        left: list[dict[str, Any]],
        right: list[dict[str, Any]],
        left_key: str,
        right_key: str,
    ) -> list[dict[str, Any]]:
        if not left or not right:
            return []

        # Build phase: choose smaller relation as build side
        if len(left) <= len(right):
            build_rel, probe_rel = left, right
            build_k, probe_k = left_key, right_key
        else:
            build_rel, probe_rel = right, left
            build_k, probe_k = right_key, left_key

        hash_table: dict[Any, list[dict[str, Any]]] = {}
        for row in build_rel:
            k = row.get(build_k)
            if k not in hash_table:
                hash_table[k] = []
            hash_table[k].append(row)

        # Probe phase: stream probe relation
        matches: list[dict[str, Any]] = []
        for row in probe_rel:
            k = row.get(probe_k)
            if k in hash_table:
                for b_row in hash_table[k]:
                    matches.append({**b_row, **row})

        return matches

    @staticmethod
    def sort_merge_join(
        left: list[dict[str, Any]],
        right: list[dict[str, Any]],
        left_key: str,
        right_key: str,
    ) -> list[dict[str, Any]]:
        if not left or not right:
            return []

        s_left = sorted(left, key=lambda x: x[left_key])
        s_right = sorted(right, key=lambda x: x[right_key])

        i, j = 0, 0
        matches: list[dict[str, Any]] = []

        while i < len(s_left) and j < len(s_right):
            l_val = s_left[i][left_key]
            r_val = s_right[j][right_key]

            if l_val == r_val:
                # Find all matching items in right for this key
                right_group: list[dict[str, Any]] = []
                k = j
                while k < len(s_right) and s_right[k][right_key] == l_val:
                    right_group.append(s_right[k])
                    k += 1

                # Match with all consecutive left items having identical key
                while i < len(s_left) and s_left[i][left_key] == l_val:
                    for r_item in right_group:
                        matches.append({**s_left[i], **r_item})
                    i += 1
                j = k
            elif l_val < r_val:
                i += 1
            else:
                j += 1

        return matches
