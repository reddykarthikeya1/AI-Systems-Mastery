"""Problem 01 — Cost Based Join Order

Topic: 22 Query Optimization CBO Index Tuning
Target: Production-grade implementation

Find optimal join order of tables using cost estimation.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def cost_based_join_order(table_sizes: dict[str, int], join_selectivities: dict[tuple[str, str], float]) -> tuple[list[str], float]:
    """Compute optimal left-deep join order for all tables minimizing total intermediate tuples.
    Returns (best_order_list, min_cost).
    """
    raise NotImplementedError("Implement cost_based_join_order")
