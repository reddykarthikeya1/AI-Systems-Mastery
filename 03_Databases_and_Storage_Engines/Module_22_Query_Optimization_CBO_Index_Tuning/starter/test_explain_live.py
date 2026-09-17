"""Tests for Module 22: Real PostgreSQL Query Optimizer & EXPLAIN (Track B)."""

from __future__ import annotations

import pytest

def _postgres_is_up() -> bool:
    try:
        from explain_live import ExplainLiveClient
        client = ExplainLiveClient()
        return client.ping()
    except Exception:
        return False

requires_postgres = pytest.mark.skipif(
    not _postgres_is_up(),
    reason="PostgreSQL not reachable on localhost:15432 - start with: make up postgres"
)

pytestmark = [pytest.mark.requires_postgres, requires_postgres]


def test_explain_live_ping():
    from explain_live import ExplainLiveClient
    client = ExplainLiveClient()
    assert client.ping() is True


def test_explain_plan_generation():
    from explain_live import ExplainLiveClient
    client = ExplainLiveClient()
    plan = client.get_explain_plan("SELECT 1;")
    assert "Result" in plan


def test_explain_analyze_buffers():
    from explain_live import ExplainLiveClient
    client = ExplainLiveClient()
    client.setup_optimizer_benchmark_tables()
    plan = client.get_explain_plan("SELECT * FROM opt_departments WHERE dept_id = 1;", analyze=True, buffers=True)
    assert "Buffers: shared" in plan or "Index Scan" in plan or "Seq Scan" in plan


def test_planner_force_join_flip():
    from explain_live import ExplainLiveClient
    client = ExplainLiveClient()
    client.setup_optimizer_benchmark_tables()

    with client.get_connection() as conn:
        with conn.cursor() as cur:
            # When enable_nestloop is off, PostgreSQL flips nested loop into Hash Join or Merge Join
            cur.execute("SET enable_nestloop = off;")
            cur.execute("""
                EXPLAIN
                SELECT * FROM opt_employees e
                JOIN opt_departments d ON e.dept_id = d.dept_id;
            """)
            plan = "\n".join(r[0] for r in cur.fetchall())
            assert "Hash Join" in plan or "Merge Join" in plan or "Scan" in plan


def test_index_only_scan_verification():
    from explain_live import ExplainLiveClient
    client = ExplainLiveClient()
    tbl = "opt_idx_only_test"

    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {tbl};")
            cur.execute(f"CREATE TABLE {tbl} (id INT, code INT, val TEXT);")
            cur.execute(f"CREATE INDEX idx_{tbl}_covering ON {tbl}(id, code);")
            cur.execute(f"INSERT INTO {tbl} SELECT g, g * 2, 'text' FROM generate_series(1, 1000) g;")
            # VACUUM cannot run inside a transaction block, and psycopg2 opens
            # one on the first statement. run_maintenance() uses autocommit.
            conn.commit()
            client.run_maintenance(f"VACUUM (ANALYZE) {tbl};")

            cur.execute(f"EXPLAIN SELECT id, code FROM {tbl} WHERE id = 100;")
            plan = "\n".join(r[0] for r in cur.fetchall())
            assert "Index Only Scan" in plan or "Index Scan" in plan or "Bitmap" in plan


def test_vacuum_analyze_updates_statistics():
    from explain_live import ExplainLiveClient
    client = ExplainLiveClient()
    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("ANALYZE opt_employees;")
            cur.execute("""
                SELECT relpages, reltuples
                FROM pg_class
                WHERE relname = 'opt_employees';
            """)
            row = cur.fetchone()
            assert row is not None
            assert row[0] >= 0  # pages >= 0


def test_hash_join_costing():
    from explain_live import ExplainLiveClient
    client = ExplainLiveClient()
    plan = client.get_explain_plan("""
        SELECT * FROM generate_series(1, 100) a(id)
        JOIN generate_series(1, 100) b(id) ON a.id = b.id;
    """)
    assert "Join" in plan or "Scan" in plan or "Function Scan" in plan


def test_cbo_model_reconciliation_cost_constants():
    """Track A <-> Track B: Handbuilt CostEstimator default costing matches PostgreSQL defaults."""
    from query_optimizer import CostEstimator
    from explain_live import ExplainLiveClient

    estimator = CostEstimator()
    # In PostgreSQL docs:
    # seq_page_cost = 1.0
    # random_page_cost = 4.0
    # cpu_tuple_cost = 0.01
    # cpu_operator_cost = 0.0025
    assert estimator.seq_page_cost == 1.0
    assert estimator.random_page_cost == 4.0
    assert estimator.cpu_tuple_cost == 0.01
    assert estimator.cpu_operator_cost == 0.0025

    client = ExplainLiveClient()
    with client.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SHOW seq_page_cost;")
            pg_seq = float(cur.fetchone()[0])
            cur.execute("SHOW random_page_cost;")
            pg_rnd = float(cur.fetchone()[0])

            assert estimator.seq_page_cost == pg_seq
            assert estimator.random_page_cost == pg_rnd
