"""Module 22: Real PostgreSQL Query Optimizer & EXPLAIN (ANALYZE, BUFFERS) (Track B).

Interacts directly with PostgreSQL to demonstrate:
1. Estimate vs actual row divergence in execution plans.
2. Running ANALYZE to update pg_statistic and repair bad cardinality estimates.
3. Forcing planner join flips (Nested Loop -> Hash Join / Merge Join) via enable_nestloop.
4. Index-Only Scans with visibility map requirements (avoiding Heap Fetch).
5. Cost-Based Optimizer costing formulas (seq_page_cost vs random_page_cost).
"""

from __future__ import annotations

import os


try:
    import psycopg2
except ImportError:
    psycopg2 = None  # type: ignore


class ExplainLiveClient:
    """Production PostgreSQL query optimizer analyzer."""

    def __init__(
        self,
        dbname: str = "coursedb",
        user: str = "postgres",
        password: str = "coursepw",
        host: str = os.environ.get("COURSE_DB_HOST", "localhost"),
        port: int = int(os.environ.get("COURSE_PG_PORT", "15432")),
    ):
        if psycopg2 is None:
            raise RuntimeError("psycopg2 is not installed. Install with: pip install psycopg2-binary")
        self.conn_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
        }

    def get_connection(self):
        return psycopg2.connect(**self.conn_params)

    def ping(self) -> bool:
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1;")
                    return cur.fetchone()[0] == 1
        except Exception:
            return False

    def setup_optimizer_benchmark_tables(self) -> None:
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS opt_departments (
                        dept_id INT PRIMARY KEY,
                        name TEXT NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS opt_employees (
                        emp_id INT PRIMARY KEY,
                        dept_id INT NOT NULL,
                        name TEXT NOT NULL,
                        salary NUMERIC(10, 2) NOT NULL
                    );
                """)

    def run_maintenance(self, statement: str) -> None:
        """Run VACUUM / ANALYZE, which PostgreSQL forbids inside a transaction.

        psycopg2 opens an implicit transaction on the first statement, so
        `cur.execute("VACUUM")` raises `ActiveSqlTransaction`. Maintenance
        commands need autocommit - this is the standard escape hatch, and it is
        the one thing about VACUUM that surprises everyone once.
        """
        conn = psycopg2.connect(**self.conn_params)
        try:
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            with conn.cursor() as cur:
                cur.execute(statement)
        finally:
            conn.close()

    def get_explain_plan(self, sql: str, analyze: bool = False, buffers: bool = False) -> str:
        options = []
        if analyze:
            options.append("ANALYZE")
        if buffers:
            options.append("BUFFERS")
        prefix = f"EXPLAIN ({', '.join(options)}) " if options else "EXPLAIN "

        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(prefix + sql)
                rows = cur.fetchall()
                return "\n".join(r[0] for r in rows)

    def toggle_planner_setting(self, setting_name: str, enabled: bool) -> None:
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                val = "on" if enabled else "off"
                cur.execute(f"SET {setting_name} = {val};")
