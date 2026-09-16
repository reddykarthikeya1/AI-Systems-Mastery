"""Module 05: Real PostgreSQL MVCC, Indexing & EXPLAIN (ANALYZE, BUFFERS) (Track B).

Interacts directly with PostgreSQL via psycopg2 to demonstrate:
1. Multi-Version Concurrency Control (MVCC): Two concurrent connections demonstrating snapshot isolation.
2. Hidden system columns (xmin, xmax, ctid) tracking row version lifecycle and visibility.
3. Deliberate table bloat generation through mass updates.
4. Dead tuple inspection via pg_stat_user_tables (n_dead_tup, n_live_tup).
5. VACUUM (VERBOSE, ANALYZE) reclaiming bloat and updating statistics.
6. Execution profiling via EXPLAIN (ANALYZE, BUFFERS) inspecting shared hit blocks.
"""

from __future__ import annotations

import os

from typing import Any

try:
    import psycopg2
    import psycopg2.extensions
except ImportError:
    psycopg2 = None  # type: ignore


class MVCCLiveClient:
    """Production PostgreSQL client demonstrating MVCC and table maintenance."""

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

    def setup_accounts_table(self, table_name: str = "mvcc_accounts") -> None:
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        id INT PRIMARY KEY,
                        owner TEXT NOT NULL,
                        balance NUMERIC(12, 2) NOT NULL
                    );
                """)

    def inspect_tuple_headers(self, table_name: str, row_id: int) -> dict[str, Any]:
        """Reads PostgreSQL hidden MVCC system columns: xmin, xmax, ctid."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT xmin::text, xmax::text, ctid::text, id, owner, balance
                    FROM {table_name}
                    WHERE id = %s;
                """, (row_id,))
                row = cur.fetchone()
                if not row:
                    return {}
                return {
                    "xmin": row[0],
                    "xmax": row[1],
                    "ctid": row[2],
                    "id": row[3],
                    "owner": row[4],
                    "balance": float(row[5]),
                }

    def induce_row_bloat(self, table_name: str, row_id: int, updates_count: int = 100) -> None:
        """Repeatedly updates a row in separate transactions to generate dead tuples."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                for i in range(updates_count):
                    cur.execute(f"UPDATE {table_name} SET balance = balance + 1.0 WHERE id = %s;", (row_id,))
                    conn.commit()

    def inspect_dead_tuples(self, table_name: str) -> dict[str, int]:
        """Inspects dead vs live tuple count from pg_stat_user_tables."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT n_live_tup, n_dead_tup
                    FROM pg_stat_user_tables
                    WHERE relname = %s;
                """, (table_name,))
                row = cur.fetchone()
                if not row:
                    return {"live_tuples": 0, "dead_tuples": 0}
                return {"live_tuples": row[0], "dead_tuples": row[1]}

    def run_vacuum(self, table_name: str, verbose: bool = True) -> None:
        """Executes VACUUM outside a transaction block."""
        conn = self.get_connection()
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute(f"VACUUM (VERBOSE, ANALYZE) {table_name};")
        conn.close()

    def explain_analyze_buffers(self, sql: str) -> str:
        """Executes EXPLAIN (ANALYZE, BUFFERS, COSTS) to view shared buffer cache hits."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"EXPLAIN (ANALYZE, BUFFERS) {sql};")
                rows = cur.fetchall()
                return "\n".join(r[0] for r in rows)
