"""Tests for Module 02 Real Modern SQL Mastery (Track B)."""

from __future__ import annotations

from sql_live import SqlLiveEngine


def test_recursive_cte_management_tree() -> None:
    engine = SqlLiveEngine()
    engine.seed_data()

    tree = engine.get_management_hierarchy(root_emp_id=1)
    assert len(tree) == 7

    # Root Alice CEO
    assert tree[0]["name"] == "Alice CEO"
    assert tree[0]["level"] == 0

    # Level 1 VPs
    level_1_names = {r["name"] for r in tree if r["level"] == 1}
    assert level_1_names == {"Bob VP Eng", "Carol VP Sales"}

    # Level 3 Frank & Eve
    level_3_reports = [r for r in tree if r["level"] == 3]
    assert len(level_3_reports) == 2
    paths = [r["path"] for r in level_3_reports]
    assert any("Alice CEO -> Bob VP Eng -> Dave Lead Dev -> Eve Senior Dev" in p for p in paths)


def test_window_functions_running_total_and_lags() -> None:
    engine = SqlLiveEngine()
    engine.seed_data()

    rows = engine.compute_moving_averages_and_rankings()
    assert len(rows) == 8

    north_rows = [r for r in rows if r["region"] == "North"]
    # 2026-01-01: 1200
    assert north_rows[0]["running_total"] == 1200.0
    assert north_rows[0]["prev_day_amount"] is None
    # 2026-01-02: 1200 + 1500 = 2700
    assert north_rows[1]["running_total"] == 2700.0
    assert north_rows[1]["prev_day_amount"] == 1200.0
    # 2026-01-03: 2700 + 1100 = 3800, 3-day avg = (1200+1500+1100)/3 = 1266.66...
    assert north_rows[2]["running_total"] == 3800.0
    assert round(north_rows[2]["moving_avg_3day"], 2) == round(3800 / 3, 2)


def test_explain_query_plan_verification() -> None:
    engine = SqlLiveEngine()
    engine.seed_data()

    plan = engine.explain_query_plan("SELECT * FROM employees WHERE emp_id = 4")
    assert len(plan) > 0
    assert any("SEARCH" in p or "SCAN" in p for p in plan)
