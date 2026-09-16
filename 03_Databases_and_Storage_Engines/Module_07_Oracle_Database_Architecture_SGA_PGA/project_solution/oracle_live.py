"""Module 07: Real Oracle Database Architecture & SGA/PGA Operations (Track B).

Interacts directly with Oracle Database via python-oracledb to demonstrate:
1. Shared Pool Library Cache statistics (v$librarycache, v$sql).
2. Soft parse vs hard parse execution with bind variables.
3. Database Buffer Cache hit ratio calculation from v$sysstat.
4. SGA component sizing and dynamic SGA parameters from v$sgainfo / v$sgastat.
5. High-Water Mark (HWM) and extent storage allocation queries.
"""

from __future__ import annotations

import os

from typing import Any

try:
    import oracledb
except ImportError:
    oracledb = None  # type: ignore


class OracleLiveClient:
    """Production Oracle client for inspecting SGA/PGA memory structures and execution plans."""

    def __init__(
        self,
        user: str = "system",
        password: str = os.environ.get("COURSE_ORACLE_PASSWORD", "coursepw"),
        dsn: str = "localhost:11521/FREEPDB1",
    ):
        if oracledb is None:
            raise RuntimeError("python-oracledb is not installed. Install with: pip install oracledb")
        self.user = user
        self.password = password
        self.dsn = dsn

    def get_connection(self):
        return oracledb.connect(user=self.user, password=self.password, dsn=self.dsn)

    def ping(self) -> bool:
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1 FROM DUAL")
                    return cur.fetchone()[0] == 1
        except Exception:
            return False

    def query_sga_info(self) -> dict[str, int]:
        """Queries v$sgainfo to inspect Buffer Cache, Shared Pool, and Large Pool allocations."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT name, bytes FROM v$sgainfo")
                return {row[0]: row[1] for row in cur.fetchall()}

    def get_buffer_cache_hit_ratio(self) -> float:
        """Calculates Buffer Cache hit ratio: 1 - (physical reads / (db block gets + consistent gets))."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT name, value FROM v$sysstat 
                    WHERE name IN ('consistent gets', 'db block gets', 'physical reads')
                """)
                stats = {row[0]: row[1] for row in cur.fetchall()}
                logical_reads = stats.get("consistent gets", 0) + stats.get("db block gets", 0)
                phys_reads = stats.get("physical reads", 0)
                if logical_reads == 0:
                    return 1.0
                return round(1.0 - (phys_reads / logical_reads), 4)

    def execute_with_binds(self, sql: str, params_list: list[dict[str, Any]]) -> int:
        """Executes repeated queries with bind variables to guarantee soft parses in the Library Cache."""
        rows_affected = 0
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                for p in params_list:
                    cur.execute(sql, p)
                    rows_affected += cur.rowcount
            conn.commit()
        return rows_affected
