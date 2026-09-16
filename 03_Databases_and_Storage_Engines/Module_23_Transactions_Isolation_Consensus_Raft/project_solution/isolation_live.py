"""Module 23: Real Multi-Connection ANSI SQL Isolation & Deadlocks Client (Track B).

Interacts directly with PostgreSQL via psycopg2 to demonstrate:
1. READ COMMITTED vs REPEATABLE READ snapshot boundaries preventing/allowing non-repeatable reads.
2. Phantom Reads prevented under PostgreSQL REPEATABLE READ (predicate locks).
3. Classic Write Skew anomaly reproduced under REPEATABLE READ.
4. SERIALIZABLE isolation detecting Write Skew and throwing 40001 (could not serialize access).
5. Deadlock detection induced by opposite-order row locking throwing 40P01 (deadlock detected).
"""

from __future__ import annotations

import os


try:
    import psycopg2
    import psycopg2.extensions
except ImportError:
    psycopg2 = None  # type: ignore


class IsolationLiveClient:
    """Production client testing concurrent transactions across SQL isolation levels."""

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

    def get_connection(self, isolation_level: str = "READ COMMITTED"):
        conn = psycopg2.connect(**self.conn_params)
        levels = {
            "READ UNCOMMITTED": psycopg2.extensions.ISOLATION_LEVEL_READ_UNCOMMITTED,
            "READ COMMITTED": psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
            "REPEATABLE READ": psycopg2.extensions.ISOLATION_LEVEL_REPEATABLE_READ,
            "SERIALIZABLE": psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        }
        conn.set_isolation_level(levels[isolation_level])
        return conn

    def ping(self) -> bool:
        try:
            conn = self.get_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                val = cur.fetchone()[0]
            conn.close()
            return val == 1
        except Exception:
            return False

    def setup_bank_accounts(self, table_name: str = "iso_bank_accounts") -> None:
        conn = self.get_connection()
        with conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INT PRIMARY KEY,
                    holder TEXT NOT NULL,
                    balance NUMERIC(10, 2) NOT NULL
                );
            """)
            conn.commit()
        conn.close()

    def setup_oncall_doctors(self, table_name: str = "iso_doctors") -> None:
        """Classic write skew table: at least one doctor must be on-call at all times."""
        conn = self.get_connection()
        with conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INT PRIMARY KEY,
                    name TEXT NOT NULL,
                    on_call BOOLEAN NOT NULL
                );
            """)
            conn.commit()
        conn.close()
