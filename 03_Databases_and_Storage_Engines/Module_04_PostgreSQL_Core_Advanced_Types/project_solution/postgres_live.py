"""Module 04: Real PostgreSQL Core & Advanced Types Client (Track B).

Interacts directly with PostgreSQL via psycopg2 to demonstrate:
1. Native JSONB storage, containment query operator (@>), and key extraction (->>).
2. GIN indexing on JSONB documents and its execution plan impact.
3. PostgreSQL Range types (tsrange, numrange) and EXCLUDE USING gist constraints.
4. Native 1D and 2D arrays with ARRAY[] constructors and ANY() membership queries.
5. Storage TOAST threshold inspection via pg_column_size() on large text/bytea fields.
"""

from __future__ import annotations

import os

from typing import Any

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    psycopg2 = None  # type: ignore


class PostgresLiveClient:
    """Production PostgreSQL driver wrapper for advanced type features."""

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

    def setup_jsonb_catalog(self, table_name: str = "products_catalog") -> None:
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    DROP TABLE IF EXISTS {table_name} CASCADE;
                    """)
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        id SERIAL PRIMARY KEY,
                        title TEXT NOT NULL,
                        metadata JSONB NOT NULL
                    );
                    CREATE INDEX IF NOT EXISTS idx_{table_name}_gin_meta ON {table_name} USING GIN (metadata);
                """)

    def insert_jsonb_product(self, table_name: str, title: str, metadata: dict[str, Any]) -> int:
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"INSERT INTO {table_name} (title, metadata) VALUES (%s, %s) RETURNING id;",
                    (title, psycopg2.extras.Json(metadata)),
                )
                return cur.fetchone()[0]

    def query_jsonb_containment(self, table_name: str, criteria: dict[str, Any]) -> list[tuple[Any, ...]]:
        """Uses PostgreSQL @> containment operator with GIN index acceleration."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT id, title, metadata FROM {table_name} WHERE metadata @> %s;",
                    (psycopg2.extras.Json(criteria),),
                )
                return cur.fetchall()

    def setup_range_exclusion_table(self, table_name: str = "room_reservations") -> None:
        """Uses btree_gist extension and EXCLUDE constraint to reject overlapping booking intervals."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS btree_gist;")
                cur.execute(f"""
                    DROP TABLE IF EXISTS {table_name} CASCADE;
                    """)
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        id SERIAL PRIMARY KEY,
                        room_id INT NOT NULL,
                        during TSRANGE NOT NULL,
                        EXCLUDE USING gist (room_id WITH =, during WITH &&)
                    );
                """)

    def inspect_toast_sizes(self, small_text: str, large_text: str) -> dict[str, int]:
        """Compares in-page tuple size vs TOAST compression using pg_column_size()."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        pg_column_size(%s) AS small_size,
                        pg_column_size(%s) AS large_size;
                """, (small_text, large_text))
                row = cur.fetchone()
                return {"small_bytes": row[0], "large_bytes": row[1]}
