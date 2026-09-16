"""Tests for Module 17: Real DuckDB Vectorized Columnar OLAP & Reconciliation (Track B)."""

from __future__ import annotations

from pathlib import Path
import pytest
from duckdb_live import DuckDBLiveEngine
from columnar_engine import ColumnarTable

def _duckdb_is_available() -> bool:
    """Probe without importing - find_spec avoids the import side effects."""
    import importlib.util

    return importlib.util.find_spec("duckdb") is not None

skip_if_no_duckdb = pytest.mark.skipif(
    not _duckdb_is_available(),
    reason="duckdb package not available. Install with: pip install duckdb"
)

pytestmark = [skip_if_no_duckdb]


def test_duckdb_live_basic_vectorized_query():
    engine = DuckDBLiveEngine()
    rows = engine.query("SELECT 1 AS num, 'duckdb' AS name")
    assert len(rows) == 1
    assert rows[0] == (1, "duckdb")


def test_duckdb_direct_parquet_query(tmp_path: Path):
    engine = DuckDBLiveEngine()
    parquet_file = tmp_path / "telemetry.parquet"

    # Create dataset
    engine.create_parquet_dataset(parquet_file, row_count=10_000)
    assert parquet_file.exists()
    assert parquet_file.stat().st_size > 0

    # Query directly from disk without table load
    results = engine.query_parquet_direct(parquet_file, min_price=800.0)
    assert len(results) > 0
    # Each row: (category_id, count, avg_price)
    for cat_id, count, avg_price in results:
        assert 0 <= cat_id < 10
        assert count > 0
        assert avg_price >= 800.0


def test_duckdb_explain_and_explain_analyze():
    engine = DuckDBLiveEngine()
    plan = engine.explain_query("SELECT SUM(range) FROM range(1000) WHERE range > 500", analyze=True)
    assert "SCAN" in plan or "AGGREGATE" in plan or "FILTER" in plan or "Total Time" in plan


def test_duckdb_analytical_window_functions():
    engine = DuckDBLiveEngine()
    results = engine.execute_window_analytics()
    assert len(results) == 30
    # Column format: (day_idx, dept_id, revenue, running_total, moving_avg_3day)
    day0 = results[0]
    assert day0[2] == day0[3]  # Initial day running total equals daily revenue


def test_duckdb_read_csv_auto_sniffing(tmp_path: Path):
    engine = DuckDBLiveEngine()
    csv_file = tmp_path / "orders.csv"
    csv_file.write_text(
        "order_id,customer,amount,is_shipped\n"
        "101,Acme Corp,1499.50,true\n"
        "102,Beta LLC,890.00,false\n"
        "103,Gamma Inc,3200.75,true\n",
        encoding="utf-8"
    )

    rows = engine.query_csv_auto(csv_file)
    assert len(rows) == 3
    assert rows[0][0] == 101
    assert rows[0][1] == "Acme Corp"
    assert rows[0][2] == 1499.50
    assert rows[0][3] is True


def test_duckdb_complex_aggregation_grouping():
    engine = DuckDBLiveEngine()
    sql = """
        WITH data AS (
            SELECT range AS id, (range % 4) AS grp, (range * 1.5) AS val
            FROM range(1000)
        )
        SELECT grp, COUNT(*) AS cnt, MIN(val) AS min_v, MAX(val) AS max_v, SUM(val) AS sum_v
        FROM data
        GROUP BY grp
        ORDER BY grp
    """
    rows = engine.query(sql)
    assert len(rows) == 4
    for r in rows:
        assert r[1] == 250  # 1000 / 4


@pytest.mark.perf
def test_duckdb_columnar_scan_projection_benchmark():
    engine = DuckDBLiveEngine()
    res = engine.benchmark_columnar_vs_row_scan(n_rows=50_000)
    assert res["rows"] == 50_000
    assert res["single_column_time_s"] > 0
    assert res["all_columns_time_s"] > 0


def test_track_a_columnar_model_matches_duckdb_reconciliation():
    """Track A <-> Track B: Handbuilt ColumnarTable model vs real DuckDB vectorized execution."""
    engine = DuckDBLiveEngine()
    schema = ["id", "score", "revenue"]
    test_rows = [
        {"id": 1, "score": 85, "revenue": 120.0},
        {"id": 2, "score": 40, "revenue": 50.0},
        {"id": 3, "score": 95, "revenue": 300.0},
        {"id": 4, "score": 60, "revenue": 80.0},
        {"id": 5, "score": 90, "revenue": 250.0},
    ]

    schema = {"id": "int", "score": "int", "revenue": "float"}
    model_table = ColumnarTable(schema=schema, row_group_size=2)
    model_table.append_rows(test_rows)
    # Model predicate: score >= 60 -> sum revenue
    model_sum = model_table.aggregate("revenue", "SUM", filter_predicate=("score", ">=", 60))

    # Real DuckDB
    engine.conn.execute("""
        CREATE OR REPLACE TABLE reconcile_bench (
            id INT, score INT, revenue DOUBLE
        )
    """)
    for r in test_rows:
        engine.conn.execute("INSERT INTO reconcile_bench VALUES (?, ?, ?)", [r["id"], r["score"], r["revenue"]])

    duckdb_sum = engine.query("SELECT SUM(revenue) FROM reconcile_bench WHERE score >= 60")[0][0]

    # Reconcile: (85 -> 120) + (95 -> 300) + (60 -> 80) + (90 -> 250) = 750.0
    assert model_sum == duckdb_sum == 750.0
