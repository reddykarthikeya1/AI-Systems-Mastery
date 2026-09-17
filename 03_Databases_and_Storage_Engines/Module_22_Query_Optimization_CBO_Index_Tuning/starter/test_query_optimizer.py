"""Module 22 Test Suite: Query Optimization, Cost-Based Optimizer & Physical Joins."""

from __future__ import annotations

from query_optimizer import CostEstimator, PhysicalJoins, TableStatistics


def test_selectivity_estimation_mcv_and_ndv() -> None:
    stats = TableStatistics(
        table_name="users",
        total_pages=1000,
        total_tuples=100_000,
        distinct_counts={"department": 10, "gender": 2},
        mcv_frequencies={"country": {"USA": 0.65, "CAN": 0.20}},
    )
    estimator = CostEstimator()

    # MCV matches exact frequency
    assert estimator.estimate_selectivity(stats, "country", "=", "USA") == 0.65
    assert estimator.estimate_selectivity(stats, "country", "=", "CAN") == 0.20

    # Uniform distribution: 1 / NDV
    assert estimator.estimate_selectivity(stats, "department", "=", "Engineering") == 0.10
    assert estimator.estimate_selectivity(stats, "gender", "=", "F") == 0.50


def test_cbo_access_path_tipping_point() -> None:
    stats = TableStatistics(
        table_name="transactions",
        total_pages=5_000,
        total_tuples=500_000,
        distinct_counts={"account_id": 50_000, "status": 2},
        mcv_frequencies={"status": {"COMPLETED": 0.85, "FAILED": 0.15}},
    )
    estimator = CostEstimator()

    # Highly selective predicate: account_id = 42 (Selectivity = 1 / 50000 = 0.00002)
    path_selective, cost_selective = estimator.choose_scan_path(stats, "account_id", "=", 42)
    assert path_selective == "INDEX_SCAN"
    assert cost_selective < estimator.estimate_seq_scan_cost(stats)

    # Low selectivity / high cardinality predicate: status = 'COMPLETED' (85% of table)
    # Tipping point triggered: Sequential scan is chosen to avoid massive random I/O!
    path_non_selective, cost_non_selective = estimator.choose_scan_path(stats, "status", "=", "COMPLETED")
    assert path_non_selective == "SEQ_SCAN"
    assert cost_non_selective == estimator.estimate_seq_scan_cost(stats)


def test_nested_loop_join() -> None:
    outer = [{"id": 1, "tier": "gold"}, {"id": 2, "tier": "bronze"}]
    inner = [{"user_id": 1, "promo": "50%_OFF"}, {"user_id": 2, "promo": "NO_DISCOUNT"}]

    # Arbitrary lambda predicate
    results = PhysicalJoins.nested_loop_join(
        outer, inner, predicate=lambda r, s: r["id"] == s["user_id"] and r["tier"] == "gold"
    )

    assert len(results) == 1
    assert results[0]["id"] == 1
    assert results[0]["promo"] == "50%_OFF"


def test_hash_join_build_probe() -> None:
    customers = [{"cid": 10, "name": "Alice"}, {"cid": 20, "name": "Bob"}]
    orders = [
        {"order_id": 101, "cust_id": 10, "amount": 50},
        {"order_id": 102, "cust_id": 10, "amount": 90},
        {"order_id": 103, "cust_id": 20, "amount": 25},
        {"order_id": 104, "cust_id": 99, "amount": 999},  # Unmatched
    ]

    matches = PhysicalJoins.hash_join(customers, orders, left_key="cid", right_key="cust_id")
    assert len(matches) == 3

    # Alice has 2 orders, Bob has 1
    alice_orders = [m for m in matches if m["name"] == "Alice"]
    assert len(alice_orders) == 2
    assert {o["order_id"] for o in alice_orders} == {101, 102}


def test_sort_merge_join_with_duplicates() -> None:
    left = [{"k": 1, "l_val": "L1a"}, {"k": 1, "l_val": "L1b"}, {"k": 2, "l_val": "L2"}]
    right = [{"k": 1, "r_val": "R1a"}, {"k": 1, "r_val": "R1b"}, {"k": 3, "r_val": "R3"}]

    matches = PhysicalJoins.sort_merge_join(left, right, left_key="k", right_key="k")

    # 2 matching keys on left x 2 matching keys on right = 4 joined rows for k=1
    assert len(matches) == 4
    for m in matches:
        assert m["k"] == 1
